import json
import math
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

import polars as pl

from src.infrastructure.data.polars_loader import CSVPolarsLoader
from src.application.calculators import DataEnricher
from src.application.trackers import TrackerEngine
from src.domain.strategy_models import StrategyDef
from src.engine.strategy_scanner import StrategyScanner
from src.engine.strategy_selector import StrategySelector
from src.engine.strategy_backtester import StrategyBacktester
from src.engine.strategy_reporter import StrategyReporter


# MT5 symbol -> internal name mapping (for deployed strategy exclusion)
MT5_TO_INTERNAL = {
    "EURUSD+": "EURUSD", "GBPUSD+": "GBPUSD", "USDJPY+": "USDJPY",
    "AUDUSD+": "AUDUSD", "GBPJPY+": "GBPJPY", "EURJPY+": "EURJPY",
    "GBPAUD+": "GBPAUD", "XAUUSD+": "XAUUSD", "XAGUSD": "XAGUSD",
    "USOUSD": "WTI", "UKOUSD": "BRENT", "NG-C": "NATGAS",
    "SP500": "SP500", "NAS100": "NASDAQ100", "VIX": "VIX",
}


class StrategyPipeline:

    DURATIONS = [15, 30, 45, 60]

    def __init__(self, data_dir: str, config_path: str, reports_dir: str):
        self.data_dir = data_dir
        self.loader = CSVPolarsLoader(data_dir)
        with open(config_path, "r") as f:
            self.config = json.load(f)
        self.reports_dir = reports_dir
        os.makedirs(reports_dir, exist_ok=True)
        self.reporter = StrategyReporter(reports_dir)

    def run_all(self):
        master_summary = []

        for symbol in self.config:
            print(f"\n{'='*60}")
            print(f"  Processing: {symbol}")
            print(f"{'='*60}")

            try:
                asset_result = self.run_asset(symbol)
                master_summary.append(asset_result)
            except Exception as e:
                print(f"  ERROR processing {symbol}: {e}")
                import traceback
                traceback.print_exc()

        self._write_master_summary(master_summary)
        print(f"\nPipeline complete. Reports in: {self.reports_dir}")

    def run_asset(self, symbol: str) -> Dict:
        cfg = self.config[symbol]

        print(f"  [1/5] Loading and enriching data...")
        df_raw = self.loader.load_data(symbol, "M15")
        df_raw = DataEnricher.enrich_with_rsi(df_raw)
        df_enriched = DataEnricher.enrich_with_daily_context(df_raw, cfg["pd_start"], cfg["pd_end"])

        sessions = cfg.get("sessions", [])

        print(f"  [2/5] Building stats for {len(sessions)} sessions x {len(self.DURATIONS)} durations...")
        stats_by_combo = {}
        combo_meta = []

        for sess in sessions:
            for dur in self.DURATIONS:
                key = f"{sess['name']}_{dur}"
                try:
                    stats_df = self._build_stats(df_enriched, sess["time_start"], dur)
                    if stats_df is not None and stats_df.height > 0:
                        stats_by_combo[key] = stats_df
                        combo_meta.append({
                            "session_name": sess["name"],
                            "time_start": sess["time_start"],
                            "duration": dur,
                        })
                except Exception as e:
                    print(f"[WARN] Building stats {symbol} {sess['name']} {dur}m: {e}")

        if not stats_by_combo:
            print(f"  No valid combos for {symbol}. Skipping.")
            return {"symbol": symbol, "strategies": [], "status": "NO_DATA"}

        print(f"  [3/5] Scanning strategy permutations...")
        all_candidates = StrategyScanner.scan_asset(symbol, stats_by_combo, combo_meta)
        print(f"  Found {len(all_candidates)} viable candidates. Top 5 WR:")
        for c in all_candidates[:5]:
            print(f"    {c['archetype']} {c['session_name']} {c['duration']}m "
                  f"{c.get('context_label', 'BASE')} -> WR={c['win_rate']:.2%} N={c['n_trades']}")

        print(f"  [4/5] Quant team selecting top strategies...")
        selected = StrategySelector.select_top_strategies(all_candidates)
        selection_explanation = StrategySelector.explain_selection(selected, all_candidates)
        print(f"  Selected {len(selected)} strategies.")

        print(f"  [5/5] Running backtests...")
        individual_results = []
        strategy_defs = []
        context_filters = []

        for sel in selected:
            strat = StrategyDef(
                symbol=symbol,
                session_name=sel["session_name"],
                time_start=sel["time_start"],
                duration=sel["duration"],
                archetype=sel["archetype"],
                direction=sel["direction"],
                context_filter=sel.get("context_filter"),
                tp_multiplier=1.5 if "MOMENTUM" in sel["archetype"] else 1.0,
            )
            strategy_defs.append(strat)
            context_filters.append(sel.get("context_filter"))

            key = f"{sel['session_name']}_{sel['duration']}"
            stats_df = stats_by_combo[key]
            result = StrategyBacktester.backtest(strat, stats_df, sel.get("context_filter"))
            individual_results.append(result)

            status = "PASS" if result.passes_filter else "FAIL"
            print(f"    [{status}] {strat.label} -> WR={result.win_rate:.2%} "
                  f"PF={result.profit_factor:.2f} T/Y={result.trades_per_year:.0f} "
                  f"NetR={result.net_r:.1f}")

            filepath = self.reporter.write_strategy_report(result)
            print(f"    Report: {filepath}")

        group_result = StrategyBacktester.backtest_group(
            strategy_defs, stats_by_combo, context_filters
        )
        if group_result.total_trades > 0:
            gs = "PASS" if group_result.passes_filter else "FAIL"
            print(f"  [GROUP {gs}] WR={group_result.win_rate:.2%} "
                  f"PF={group_result.profit_factor:.2f} NetR={group_result.net_r:.1f}")

        summary_path = self.reporter.write_asset_summary(
            symbol, individual_results, group_result,
            selection_explanation, all_candidates
        )
        print(f"  Summary: {summary_path}")

        return {
            "symbol": symbol,
            "strategies": selected,
            "individual_results": individual_results,
            "group_result": group_result,
            "status": "OK",
        }

    def _build_stats(self, df_enriched: pl.DataFrame, time_start: str, duration: int) -> pl.DataFrame:
        df_or = DataEnricher.enrich_with_opening_range(df_enriched, time_start, duration)
        stats_df = TrackerEngine.track_events(df_or, tp_multiplier=1.5)

        agg_cols = [pl.col("or_open").first(), pl.col("pd_or_high").first(), pl.col("pd_or_low").first()]
        for col_name in ["rsi_at_or_close", "rsi_daily_14", "atr_change",
                          "atr_percentile", "or_position_vs_pd", "or_open_vs_pd_close"]:
            if col_name in df_or.columns:
                agg_cols.append(pl.col(col_name).first())

        daily_base = df_or.group_by("trade_date").agg(agg_cols)
        expanded_stats = daily_base.join(stats_df, on="trade_date", how="left")
        expanded_stats = TrackerEngine.track_post_fade_events(df_or, expanded_stats)

        # Add day_of_week
        expanded_stats = expanded_stats.with_columns(
            pl.col("trade_date").cast(pl.Date).dt.weekday().alias("day_of_week")
        )

        # Add OR width percentile booleans (relative to this combo)
        if "or_width" in expanded_stats.columns:
            q25 = expanded_stats.select(pl.col("or_width").quantile(0.25)).item()
            q75 = expanded_stats.select(pl.col("or_width").quantile(0.75)).item()
            if q25 is not None and q75 is not None:
                expanded_stats = expanded_stats.with_columns([
                    (pl.col("or_width") <= q25).alias("or_width_q1"),
                    (pl.col("or_width") >= q75).alias("or_width_q4"),
                ])

        return expanded_stats

    # ─── Discovery Mode ──────────────────────────────────────────

    def run_discovery(self, bot_config_path: str = "src/execution/bot_config.json",
                      min_wr: float = 0.55, min_trades: int = 30):
        """Scan all assets with expanded filters, exclude deployed strategies, report new edges."""

        # Load deployed strategies
        deployed_keys = self._load_deployed_keys(bot_config_path)
        print(f"Deployed strategies to exclude: {len(deployed_keys)}")

        all_discoveries = []
        total_scanned = 0

        for symbol in self.config:
            print(f"\n{'='*60}")
            print(f"  Discovery: {symbol}")
            print(f"{'='*60}")

            try:
                cfg = self.config[symbol]
                df_raw = self.loader.load_data(symbol, "M15")
                df_raw = DataEnricher.enrich_with_rsi(df_raw)
                df_enriched = DataEnricher.enrich_with_daily_context(df_raw, cfg["pd_start"], cfg["pd_end"])

                sessions = cfg.get("sessions", [])
                stats_by_combo = {}
                combo_meta = []

                for sess in sessions:
                    for dur in self.DURATIONS:
                        key = f"{sess['name']}_{dur}"
                        try:
                            stats_df = self._build_stats(df_enriched, sess["time_start"], dur)
                            if stats_df is not None and stats_df.height > 0:
                                stats_by_combo[key] = stats_df
                                combo_meta.append({
                                    "session_name": sess["name"],
                                    "time_start": sess["time_start"],
                                    "duration": dur,
                                })
                        except Exception as e:
                            print(f"[WARN] Discovery stats {symbol} {sess['name']} {dur}m: {e}")

                if not stats_by_combo:
                    continue

                candidates = StrategyScanner.scan_asset(symbol, stats_by_combo, combo_meta)
                total_scanned += len(candidates)

                # Filter: WR >= min_wr, N >= min_trades, not deployed
                for c in candidates:
                    if c["win_rate"] < min_wr or c["n_trades"] < min_trades:
                        continue
                    ckey = self._candidate_key(c)
                    if ckey in deployed_keys:
                        continue

                    # Backtest to get PF
                    strat = StrategyDef(
                        symbol=symbol,
                        session_name=c["session_name"],
                        time_start=c["time_start"],
                        duration=c["duration"],
                        archetype=c["archetype"],
                        direction=c["direction"],
                        context_filter=c.get("context_filter"),
                        tp_multiplier=1.5 if "MOMENTUM" in c["archetype"] else 1.0,
                    )
                    combo_key = f"{c['session_name']}_{c['duration']}"
                    result = StrategyBacktester.backtest(strat, stats_by_combo[combo_key], c.get("context_filter"))

                    if result.profit_factor <= 1.0:
                        continue

                    composite = c["win_rate"] * math.log(max(c["n_trades"], 1)) * result.profit_factor
                    all_discoveries.append({
                        **c,
                        "pf": result.profit_factor,
                        "net_r": result.net_r,
                        "trades_per_year": result.trades_per_year,
                        "max_dd": result.max_drawdown,
                        "composite": composite,
                    })

                n_new = sum(1 for d in all_discoveries if d["symbol"] == symbol)
                print(f"  {symbol}: {len(candidates)} scanned, {n_new} new edges found")

            except Exception as e:
                print(f"  ERROR {symbol}: {e}")
                import traceback
                traceback.print_exc()

        # Sort by composite score
        all_discoveries.sort(key=lambda x: x["composite"], reverse=True)

        # Generate report
        report_path = self.reporter.write_discovery_report(all_discoveries, total_scanned, len(deployed_keys))
        print(f"\n{'='*60}")
        print(f"  DISCOVERY COMPLETE")
        print(f"  Total scanned: {total_scanned}")
        print(f"  New edges found: {len(all_discoveries)}")
        print(f"  Report: {report_path}")
        print(f"{'='*60}")

    def _load_deployed_keys(self, bot_config_path: str) -> set:
        try:
            with open(bot_config_path, "r") as f:
                bot_cfg = json.load(f)
        except FileNotFoundError:
            return set()

        keys = set()
        for entry in bot_cfg.get("portfolio", []):
            sym_mt5 = entry["sym"]
            sym_internal = MT5_TO_INTERNAL.get(sym_mt5, sym_mt5)
            session = entry.get("session", "")
            duration = entry["duration"]
            edge = entry["edge"]
            context = entry.get("context", "BASE")
            keys.add(f"{sym_internal}|{session}|{duration}|{edge}|{context}")
        return keys

    @staticmethod
    def _candidate_key(c: Dict) -> str:
        return f"{c['symbol']}|{c['session_name']}|{c['duration']}|{c['archetype']}|{c.get('context_label', 'BASE')}"

    def _write_master_summary(self, all_results: List[Dict]):
        filepath = os.path.join(self.reports_dir, "MASTER_Strategy_Summary.md")
        md = "# KHA0SYS3 - Master Strategy Selection Report\n\n"
        md += f"**Activos procesados:** {len(all_results)}\n\n"

        md += "## Resumen Global\n\n"
        md += "| Activo | # Estrategias | Mejor WR | Mejor PF | Grupo WR | Grupo PF | Status |\n"
        md += "| --- | --- | --- | --- | --- | --- | --- |\n"

        total_approved = 0
        for r in all_results:
            sym = r["symbol"]
            strats = r.get("individual_results", [])
            group = r.get("group_result")
            n = len(strats)

            if strats:
                best_wr = max(s.win_rate for s in strats)
                best_pf = max(s.profit_factor for s in strats)
                approved = sum(1 for s in strats if s.passes_filter)
                total_approved += approved
            else:
                best_wr = 0
                best_pf = 0
                approved = 0

            g_wr = group.win_rate if group and group.total_trades > 0 else 0
            g_pf = group.profit_factor if group and group.total_trades > 0 else 0

            status = f"{approved}/{n} aprobadas" if n > 0 else "Sin estrategias"
            md += f"| {sym} | {n} | `{best_wr:.1%}` | `{best_pf:.2f}` | "
            md += f"`{g_wr:.1%}` | `{g_pf:.2f}` | {status} |\n"

        md += f"\n**Total estrategias aprobadas:** {total_approved}\n"
        md += "\n---\n*Generado por KHA0SYS3 Strategy Pipeline*\n"

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"\nMaster summary: {filepath}")


if __name__ == "__main__":
    pipeline = StrategyPipeline(
        data_dir="c:/Proyectos/kha0sys3/data",
        config_path="c:/Proyectos/kha0sys3/src/infrastructure/config/asset_config.json",
        reports_dir="c:/Proyectos/kha0sys3/reports/strategies",
    )

    if "--discover" in sys.argv:
        pipeline.run_discovery()
    else:
        pipeline.run_all()
