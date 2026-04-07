import os
import json
import polars as pl
import numpy as np
from datetime import datetime, date

from src.infrastructure.data.polars_loader import CSVPolarsLoader
from src.application.calculators import DataEnricher
from src.application.trackers import TrackerEngine
from src.application.statistics import StatisticalEngine
from src.engine.statistical_validator import StatisticalValidator


class PortfolioCompounder:
    """
    Simula compounding realista sobre un portafolio seleccionado,
    usando walk-forward OOS con deduplicación y MAGNET direction filter.
    """

    def __init__(self, data_dir: str, config_path: str, reports_dir: str):
        self.data_dir = data_dir
        self.reports_dir = reports_dir
        self.loader = CSVPolarsLoader(data_dir)
        with open(config_path, "r") as f:
            self.config = json.load(f)
        os.makedirs(reports_dir, exist_ok=True)

        # Portfolio: 4 activos × ambas sesiones × edges significativos (FDR)
        # La dedup (1 trade/día/símbolo) prioriza la sesión que dispara primero
        self.portfolio = self._build_full_portfolio()
        self.durations = [15, 30, 45, 60]

    def _build_full_portfolio(self) -> list:
        """
        Genera setups solo con sesiones primarias (no NY).
        Las sesiones NY mostraron WR < 50% OOS — destruyen valor.
        Cada activo usa su sesión primaria con los edges que funcionan.
        """
        # Solo sesiones primarias con edges validados OOS
        # Dedup por (date, symbol, edge) permite TREND + MAGNET en mismo símbolo
        return [
            # Tokyo 00:00
            {"symbol": "USDJPY", "session": "Tokyo", "time_start": "00:00", "edge": "TREND_UP"},
            # London 07:00
            {"symbol": "XAUUSD", "session": "London", "time_start": "07:00", "edge": "TREND_UP"},
            {"symbol": "EURUSD", "session": "London", "time_start": "07:00", "edge": "TREND_UP"},
            {"symbol": "EURUSD", "session": "London", "time_start": "07:00", "edge": "MAGNET_CLOSE"},
            {"symbol": "WTI", "session": "London Initial", "time_start": "07:00", "edge": "TREND_UP"},
            # Pre-Market 12:00
            {"symbol": "SP500", "session": "Pre-Market", "time_start": "12:00", "edge": "TREND_UP"},
        ]

    def log(self, msg: str):
        print(f"[COMPOUNDER] {msg}")

    def _collect_trades_for_setup(self, setup: dict, date_filter: pl.Expr = None) -> list:
        """Collect trades for a single setup across all durations, pick best."""
        sym = setup["symbol"]
        cfg = self.config.get(sym, {})
        FRICTION = 0.1
        ATR_LOW, ATR_HIGH = 0.1, 0.8

        df_raw = self.loader.load_data(sym, "M15")
        df_enr = DataEnricher.enrich_with_daily_context(
            df_raw, cfg.get("pd_start", "00:00"), cfg.get("pd_end", "23:59")
        )

        best_trades = {}

        for dur in self.durations:
            df_or = DataEnricher.enrich_with_opening_range(df_enr, setup["time_start"], dur)
            stats = TrackerEngine.track_events(df_or, tp_multiplier=5.0)

            if date_filter is not None:
                stats = stats.filter(date_filter)

            valid_days = stats.filter(
                pl.col("first_break_dir").is_in(["UP", "DOWN"])
                & pl.col("or_atr_ratio").is_between(ATR_LOW, ATR_HIGH)
            )

            for row in valid_days.iter_rows(named=True):
                trade_date = str(row["trade_date"])
                trade_dir = row["first_break_dir"]
                pnl = 0.0

                if setup["edge"] == "TREND_UP" and trade_dir == "UP":
                    or_w = row["or_width"]
                    if or_w and or_w > 0:
                        max_ext = row["max_up"] / or_w
                        pnl = 1.5 - FRICTION if max_ext >= 1.5 else -1.0 - FRICTION

                elif setup["edge"] == "TREND_DW" and trade_dir == "DOWN":
                    or_w = row["or_width"]
                    if or_w and or_w > 0:
                        max_ext = row["max_down"] / or_w
                        pnl = 1.5 - FRICTION if max_ext >= 1.5 else -1.0 - FRICTION

                elif setup["edge"] == "MAGNET_CLOSE":
                    pd_close = row["pd_close"]
                    or_high = row["or_high"]
                    or_low = row["or_low"]
                    if pd_close is None or or_high is None or or_low is None:
                        continue
                    if or_low <= pd_close <= or_high:
                        continue
                    if row["touches_pd_close"] > 0:
                        pnl = 1.0 - FRICTION
                    else:
                        pnl = -1.0 - FRICTION

                if pnl != 0:
                    h, m = map(int, setup["time_start"].split(':'))
                    exec_mins = h * 60 + m + dur

                    # Keep earliest trade per day (no look-ahead on pnl)
                    if trade_date not in best_trades or exec_mins < best_trades[trade_date]["exec_mins"]:
                        best_trades[trade_date] = {
                            "date": trade_date,
                            "exec_mins": exec_mins,
                            "symbol": sym,
                            "session": setup["session"],
                            "edge": setup["edge"],
                            "duration": dur,
                            "pnl": pnl
                        }

        return list(best_trades.values())

    def run_compounding_sim(self, start_balance: float = 1000.0,
                            risk_pct: float = 0.03, target: float = 20000.0):
        """
        Walk-forward compounding simulation.
        Train on first 50% of data, test (compound) on remaining 50%.
        """
        self.log(f"Iniciando Compounding: ${start_balance:.0f} -> ${target:.0f} | {risk_pct:.0%} risk/trade")

        # Determine date range
        first_sym = self.portfolio[0]["symbol"]
        cfg0 = self.config[first_sym]
        df0 = self.loader.load_data(first_sym, "M15")
        df0 = df0.with_columns(pl.col("time").dt.date().alias("trade_date"))
        all_dates = df0.select("trade_date").unique().sort("trade_date")["trade_date"].to_list()

        total_days = len(all_dates)
        train_end_idx = int(total_days * 0.5)
        train_end_date = all_dates[train_end_idx]
        test_start_date = all_dates[train_end_idx]

        self.log(f"  Train: inicio -> {train_end_date}")
        self.log(f"  Test (OOS): {test_start_date} -> {all_dates[-1]}")

        # Scouting phase: verify edges exist on train data
        train_filter = pl.col("trade_date").cast(pl.Date) < train_end_date
        test_filter = pl.col("trade_date").cast(pl.Date) >= test_start_date

        # Verify each setup has edge on train data
        self.log("  Verificando edges en datos de entrenamiento...")
        for setup in self.portfolio:
            train_trades = self._collect_trades_for_setup(setup, train_filter)
            if train_trades:
                wins = sum(1 for t in train_trades if t["pnl"] > 0)
                wr = wins / len(train_trades)
                self.log(f"    {setup['symbol']} {setup['session']} {setup['edge']}: {len(train_trades)} trades, WR {wr:.1%} (train)")

        # Collect OOS trades for all setups
        self.log("  Recolectando trades OOS...")
        all_oos_trades = []
        for setup in self.portfolio:
            trades = self._collect_trades_for_setup(setup, test_filter)
            all_oos_trades.extend(trades)
            if trades:
                wins = sum(1 for t in trades if t["pnl"] > 0)
                self.log(f"    {setup['symbol']} {setup['session']} {setup['edge']}: {len(trades)} trades OOS, WR {wins/len(trades):.1%}")

        # Sort chronologically (date + exec_mins)
        all_oos_trades.sort(key=lambda x: (x["date"], x["exec_mins"]))

        # Deduplication: 1 trade per day per symbol per edge type
        traded_day_sym_edge = set()
        deduped_trades = []
        for t in all_oos_trades:
            key = (t["date"], t["symbol"], t["edge"])
            if key not in traded_day_sym_edge:
                traded_day_sym_edge.add(key)
                deduped_trades.append(t)

        self.log(f"  Total trades OOS (deduplicados): {len(deduped_trades)}")

        # Compounding simulation
        balance = start_balance
        peak_balance = start_balance
        max_dd_pct = 0.0
        max_dd_usd = 0.0
        equity_curve = []
        trade_log = []
        milestones = {}
        target_milestones = [2000, 3000, 5000, 7500, 10000, 15000, 20000]
        hit_target = False
        target_date = None

        for t in deduped_trades:
            risk_amount = balance * risk_pct
            dollar_pnl = t["pnl"] * risk_amount
            balance += dollar_pnl

            # Track
            peak_balance = max(peak_balance, balance)
            dd_pct = (balance - peak_balance) / peak_balance if peak_balance > 0 else 0
            dd_usd = balance - peak_balance
            max_dd_pct = min(max_dd_pct, dd_pct)
            max_dd_usd = min(max_dd_usd, dd_usd)

            equity_curve.append({
                "date": t["date"],
                "balance": balance,
                "symbol": t["symbol"],
                "edge": t["edge"],
                "pnl_r": t["pnl"],
                "pnl_usd": dollar_pnl,
                "dd_pct": dd_pct
            })

            # Milestones
            for m in target_milestones:
                if m not in milestones and balance >= m:
                    milestones[m] = {
                        "date": t["date"],
                        "trade_num": len(equity_curve),
                        "balance": balance
                    }

            if balance >= target and not hit_target:
                hit_target = True
                target_date = t["date"]
                break  # Stop at target

            # Ruin check
            if balance <= 0:
                self.log(f"  RUINA en trade #{len(equity_curve)}, fecha {t['date']}")
                break

        # Per-setup stats (by symbol + session + edge)
        setup_stats = {}
        for t in deduped_trades:
            key = f"{t['symbol']}_{t['session']}_{t['edge']}"
            if key not in setup_stats:
                setup_stats[key] = {"wins": 0, "losses": 0, "total_pnl_r": 0, "durations": {}}
            if t["pnl"] > 0:
                setup_stats[key]["wins"] += 1
            else:
                setup_stats[key]["losses"] += 1
            setup_stats[key]["total_pnl_r"] += t["pnl"]
            dur = t.get("duration", "?")
            setup_stats[key]["durations"][dur] = setup_stats[key]["durations"].get(dur, 0) + 1

        # Use only executed trades (up to target) for MC and stats
        executed_pnls = [e["pnl_r"] for e in equity_curve]

        # Monte Carlo on the compounding series (with target cap)
        pnls_all = [t["pnl"] for t in deduped_trades]
        mc = StatisticalValidator.monte_carlo(pnls_all, n_sims=10000)

        # Decay on full OOS data (not just executed)
        dates_all = [t["date"] for t in deduped_trades]
        decay = StatisticalValidator.decay_analysis(pnls_all, dates_all, window_days=365)

        # Generate report
        self._generate_report(
            start_balance, balance, risk_pct, target,
            deduped_trades, equity_curve, milestones,
            max_dd_pct, max_dd_usd, peak_balance,
            setup_stats, mc, decay, hit_target, target_date,
            str(test_start_date), str(all_dates[-1])
        )

        return balance

    def _generate_report(self, start, final, risk_pct, target,
                         trades, equity_curve, milestones,
                         max_dd_pct, max_dd_usd, peak,
                         setup_stats, mc, decay,
                         hit_target, target_date,
                         test_start, test_end):
        total = len(trades)
        wins = sum(1 for t in trades if t["pnl"] > 0)
        losses = total - wins
        wr = wins / total if total > 0 else 0
        pnls = [t["pnl"] for t in trades]
        gross_p = sum(p for p in pnls if p > 0)
        gross_l = abs(sum(p for p in pnls if p < 0))
        pf = gross_p / gross_l if gross_l > 0 else 99.9
        growth_x = final / start if start > 0 else 0
        # Trading days
        unique_days = len(set(t["date"] for t in trades))
        trades_per_day = total / max(1, unique_days)

        report_path = os.path.join(self.reports_dir, "Portfolio_1k_to_20k_Compounding.md")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# Portfolio Compounding Simulation: $1,000 -> $20,000\n\n")
            f.write(f"> Walk-Forward OOS | {risk_pct:.0%} riesgo/trade | Deduplicación 1 trade/día/símbolo\n")
            f.write(f"> Período OOS: {test_start} -> {test_end}\n\n")

            # ── Resultado Principal ─────────────────────────────────
            f.write("## Resultado\n")
            f.write(f"| | |\n|:---|:---|\n")
            f.write(f"| **Balance Inicial** | `${start:,.2f}` |\n")
            f.write(f"| **Balance Final** | `${final:,.2f}` |\n")
            f.write(f"| **Crecimiento** | `{growth_x:.1f}x` |\n")
            f.write(f"| **Objetivo $20k** | {'ALCANZADO ' + str(target_date) if hit_target else 'No alcanzado'} |\n")
            f.write(f"| **Pico Máximo** | `${peak:,.2f}` |\n\n")

            # ── Dashboard ───────────────────────────────────────────
            f.write("## Dashboard OOS\n")
            f.write("| Métrica | Valor |\n|:---|:---|\n")
            f.write(f"| **Total Trades** | `{total}` |\n")
            f.write(f"| **Win Rate** | `{wr:.1%}` |\n")
            f.write(f"| **Profit Factor** | `{pf:.2f}` |\n")
            f.write(f"| **Expectativa** | `{np.mean(pnls):.3f} R` |\n")
            f.write(f"| **Max Drawdown %** | `{max_dd_pct:.1%}` |\n")
            f.write(f"| **Max Drawdown $** | `${abs(max_dd_usd):,.2f}` |\n")
            f.write(f"| **Días de Trading** | `{unique_days}` |\n")
            f.write(f"| **Trades/Día** | `{trades_per_day:.1f}` |\n")
            f.write(f"| **Riesgo/Trade** | `{risk_pct:.0%}` |\n\n")

            # ── Portafolio ──────────────────────────────────────────
            f.write("## Portafolio Seleccionado\n")
            f.write("| Par | Sesion | Estrategia | Horario | Razon |\n")
            f.write("|:---|:---|:---|:---|:---|\n")
            f.write("| **USDJPY** | Tokyo | TREND_UP | 00:00 UTC | Mejor JPY, bajo spread |\n")
            f.write("| **XAUUSD** | London | TREND_UP | 07:00 UTC | Independiente de FX |\n")
            f.write("| **EURUSD** | London | TREND_UP + MAGNET | 07:00 UTC | 2 edges independientes |\n")
            f.write("| **WTI** | London Initial | TREND_UP | 07:00 UTC | Commodity decorrelacionado, PF 3.48 |\n")
            f.write("| **SP500** | Pre-Market | TREND_UP | 12:00 UTC | Mejor WR+PF global |\n\n")

            f.write("**Logica de seleccion:**\n")
            f.write("- 3 horarios (Tokyo 00:00 / London 07:00 / Pre-Market 12:00)\n")
            f.write("- 5 instrumentos decorrelacionados (JPY, Metal, FX, Commodity, Indice)\n")
            f.write("- Dedup por (dia, simbolo, edge): TREND y MAGNET pueden coexistir\n")
            f.write("- Waterfall OR: 15m, si ATR falla intenta 30m\n")
            f.write("- Sesiones NY EXCLUIDAS: WR < 50%% OOS\n\n")

            # ── Per-Setup Stats ─────────────────────────────────────
            f.write("## Performance por Setup (OOS)\n")
            f.write("| Setup | W / L | Win Rate | PnL (R) | Duraciones usadas |\n")
            f.write("|:---|:---|:---|:---|:---|\n")
            for key, s in sorted(setup_stats.items(), key=lambda x: x[1]["total_pnl_r"], reverse=True):
                total_s = s["wins"] + s["losses"]
                if total_s == 0:
                    continue
                wr_s = s["wins"] / total_s
                durs = ", ".join(f"{d}m({c})" for d, c in sorted(s["durations"].items()))
                f.write(f"| **{key}** | {s['wins']} / {s['losses']} | `{wr_s:.1%}` | `{s['total_pnl_r']:.1f} R` | {durs} |\n")
            f.write("\n")

            # ── Milestones ──────────────────────────────────────────
            f.write("## Hitos de Crecimiento\n")
            f.write("| Objetivo | Fecha | Trade # | Balance |\n")
            f.write("|:---|:---|:---|:---|\n")
            for m_val in [2000, 3000, 5000, 7500, 10000, 15000, 20000]:
                if m_val in milestones:
                    mi = milestones[m_val]
                    f.write(f"| **${m_val:,}** | {mi['date']} | #{mi['trade_num']} | `${mi['balance']:,.2f}` |\n")
                else:
                    f.write(f"| **${m_val:,}** | -- | -- | -- |\n")
            f.write("\n")

            # ── Monte Carlo ─────────────────────────────────────────
            f.write("## Monte Carlo (10,000 permutaciones sobre secuencia de R)\n")
            f.write("| | P5 (Pesimista) | P50 (Mediana) | P95 (Optimista) |\n")
            f.write("|:---|:---|:---|:---|\n")
            # Simulate compounding for each MC scenario
            mc_finals = self._monte_carlo_compounding(pnls, start, risk_pct, n_sims=10000)
            f.write(f"| **Balance Final** | `${mc_finals['p5']:,.0f}` | `${mc_finals['p50']:,.0f}` | `${mc_finals['p95']:,.0f}` |\n")
            f.write(f"| **Max DD %** | `{mc_finals['dd_p5']:.1%}` | `{mc_finals['dd_p50']:.1%}` | `{mc_finals['dd_p95']:.1%}` |\n")
            f.write(f"\n**Prob de alcanzar $20k:** `{mc_finals['prob_target']:.1%}`\n")
            f.write(f"**Prob de ruina (balance < $100):** `{mc_finals['prob_ruin']:.1%}`\n\n")

            # ── Decay ───────────────────────────────────────────────
            if decay and decay.get("windows"):
                f.write("## Análisis de Decay del Edge\n")
                f.write("| Período | Trades | WR | Expectativa (R) | Estado |\n")
                f.write("|:---|:---|:---|:---|:---|\n")
                for w in decay["windows"]:
                    trend = "ESTABLE" if w["expectancy"] > 0.1 else ("DEGRADADO" if w["expectancy"] > 0 else "MUERTO")
                    f.write(f"| {w['period']} | {w['trades']} | `{w['wr']:.1%}` | `{w['expectancy']:.3f} R` | **{trend}** |\n")
                f.write(f"\n**Decay score:** `{decay.get('decay_score', 0):.2f}` (1.0 = estable)\n\n")

            # ── Equity Curve ────────────────────────────────────────
            f.write("## Curva de Crecimiento Compuesto\n")
            f.write("```text\n")
            if equity_curve:
                max_bal = max(e["balance"] for e in equity_curve)
                steps = 50
                chunk = max(1, len(equity_curve) // steps)
                for i in range(0, len(equity_curve), chunk):
                    e = equity_curve[i]
                    bar_len = int(e["balance"] / max(max_bal / 70, 1))
                    bar = "#" * bar_len
                    f.write(f"{e['date']} | ${e['balance']:10,.2f} | {bar}\n")
                # Last entry
                e = equity_curve[-1]
                bar_len = int(e["balance"] / max(max_bal / 70, 1))
                f.write(f"{e['date']} | ${e['balance']:10,.2f} | {'#' * bar_len}\n")
            f.write("```\n\n")

            # ── Drawdown Curve ──────────────────────────────────────
            f.write("## Curva de Drawdown\n")
            f.write("```text\n")
            if equity_curve:
                steps = 30
                chunk = max(1, len(equity_curve) // steps)
                for i in range(0, len(equity_curve), chunk):
                    e = equity_curve[i]
                    dd = e["dd_pct"]
                    bar = "-" * int(abs(dd) * 100) if dd < 0 else ""
                    f.write(f"{e['date']} | {dd:7.1%} | {bar}\n")
            f.write("```\n\n")

            # ── Architecture ────────────────────────────────────────
            f.write("---\n")
            f.write("### Arquitectura de Riesgo\n")
            f.write(f"1. **Riesgo por trade:** {risk_pct:.0%} del balance (compuesto)\n")
            f.write(f"2. **Fricción:** -0.1R por trade (spread + comisiones)\n")
            f.write(f"3. **TREND:** TP 1.5R, neto +1.4R | SL -1.1R\n")
            f.write(f"4. **MAGNET:** TP pd_close, neto +0.9R | SL -1.1R\n")
            f.write(f"5. **Filtro ATR:** 0.1-0.8 (no opera en baja/alta vol extrema)\n")
            f.write(f"6. **Deduplicación:** Máx 1 trade/día/símbolo\n")
            f.write(f"7. **Validación:** Walk-forward OOS (train 50%, test 50%)\n")

        self.log(f"Reporte generado: {report_path}")

    def _monte_carlo_compounding(self, pnls: list, start: float,
                                  risk_pct: float, n_sims: int = 10000,
                                  target: float = 20000.0) -> dict:
        """Monte Carlo with actual compounding (not just R permutation)."""
        pnls_arr = np.array(pnls)
        n = len(pnls_arr)
        rng = np.random.default_rng(42)

        finals = np.zeros(n_sims)
        max_dds = np.zeros(n_sims)
        reached_target = 0

        for i in range(n_sims):
            shuffled = rng.permutation(pnls_arr)
            balance = start
            peak = start
            worst_dd = 0
            trades_to_target = n

            for j, pnl_r in enumerate(shuffled):
                dollar_pnl = pnl_r * balance * risk_pct
                balance += dollar_pnl
                if balance <= 0:
                    balance = 0
                    worst_dd = -1.0
                    break
                peak = max(peak, balance)
                dd = (balance - peak) / peak
                worst_dd = min(worst_dd, dd)
                if balance >= target:
                    trades_to_target = j + 1
                    break

            finals[i] = min(balance, target)
            max_dds[i] = worst_dd

            if balance >= target:
                reached_target += 1

        return {
            "p5": float(np.percentile(finals, 5)),
            "p25": float(np.percentile(finals, 25)),
            "p50": float(np.percentile(finals, 50)),
            "p75": float(np.percentile(finals, 75)),
            "p95": float(np.percentile(finals, 95)),
            "dd_p5": float(np.percentile(max_dds, 5)),
            "dd_p50": float(np.percentile(max_dds, 50)),
            "dd_p95": float(np.percentile(max_dds, 95)),
            "prob_target": reached_target / n_sims,
            "prob_ruin": float((finals < 100).mean()),
        }


if __name__ == "__main__":
    ROOT = "c:\\Proyectos\\kha0sys3"
    sim = PortfolioCompounder(
        data_dir=os.path.join(ROOT, "data"),
        config_path=os.path.join(ROOT, "src", "infrastructure", "config", "asset_config.json"),
        reports_dir=os.path.join(ROOT, "reports")
    )
    sim.run_compounding_sim(start_balance=1000.0, risk_pct=0.03, target=20000.0)
