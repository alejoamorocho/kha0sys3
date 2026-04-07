import os
import json
import polars as pl
import numpy as np
from datetime import datetime, date

from src.infrastructure.data.polars_loader import CSVPolarsLoader
from src.application.calculators import DataEnricher
from src.application.trackers import TrackerEngine
from src.application.statistics import StatisticalEngine
from src.engine.report_generator import ReportGenerator
from src.engine.statistical_validator import StatisticalValidator


class AlphaPortfolioSimulator:
    def __init__(self, data_dir: str, config_path: str, reports_dir: str):
        self.data_dir = data_dir
        self.reports_dir = reports_dir
        self.loader = CSVPolarsLoader(data_dir)
        self.rg = ReportGenerator(data_dir, config_path, reports_dir)
        with open(config_path, "r") as f:
            self.config = json.load(f)
        os.makedirs(reports_dir, exist_ok=True)

        self.global_ledger = []
        self.setup_results = []
        self.total_days_scanned = 0
        self.atr_filtered_out = 0
        self.validation_results = {}

    def log(self, msg: str):
        print(f"[ALPHA_SIM] {msg}")

    # ── Data cache ──────────────────────────────────────────────────
    def _load_enriched(self, sym: str, cfg: dict) -> pl.DataFrame:
        df_raw = self.loader.load_data(sym, "M15")
        return DataEnricher.enrich_with_daily_context(
            df_raw, cfg.get("pd_start", "00:00"), cfg.get("pd_end", "23:59")
        )

    # ── Walk-Forward Scouting ───────────────────────────────────────
    def run_scouting(self, df_enr: pl.DataFrame = None, sym: str = None,
                     cfg: dict = None, date_filter: pl.Expr = None):
        """
        Scans for edges > 65%. When date_filter is provided, only uses
        data matching that filter (for walk-forward train windows).
        If called without arguments, scans all assets (legacy mode).
        """
        if df_enr is not None and sym is not None:
            return self._scout_single(df_enr, sym, cfg, date_filter)

        self.log("Iniciando Scouting Masivo...")
        self.qualified_setups = []
        for sym, cfg in self.config.items():
            try:
                df_enr = self._load_enriched(sym, cfg)
                setups = self._scout_single(df_enr, sym, cfg, date_filter)
                self.qualified_setups.extend(setups)
            except Exception as e:
                self.log(f"Error cargando {sym}: {e}")
        self.log(f"Scouting finalizado. {len(self.qualified_setups)} setups calificados.")

    def _scout_single(self, df_enr: pl.DataFrame, sym: str, cfg: dict,
                       date_filter: pl.Expr = None) -> list:
        durations = [15, 30, 45, 60]
        setups = []

        if date_filter is not None:
            df_enr = df_enr.filter(date_filter)

        sessions = cfg.get("sessions", [])
        for sess in sessions:
            for d in durations:
                try:
                    metrics = self.rg._evaluate_combo(df_enr, sess["time_start"], d)
                    if "error" in metrics:
                        continue

                    p_up = metrics['extensions']['UP']['up_gt_1.5_or']
                    p_dw = metrics['extensions']['DOWN']['down_gt_1.5_or']
                    p_pdc = metrics['pd_interactions']['p_touch_pd_close']

                    if p_up >= 0.65:
                        setups.append({
                            "symbol": sym, "session": sess["name"],
                            "time_start": sess["time_start"],
                            "duration": d, "edge_type": "TREND_UP", "prob": p_up
                        })
                    if p_dw >= 0.65:
                        setups.append({
                            "symbol": sym, "session": sess["name"],
                            "time_start": sess["time_start"],
                            "duration": d, "edge_type": "TREND_DW", "prob": p_dw
                        })
                    if p_pdc >= 0.65:
                        setups.append({
                            "symbol": sym, "session": sess["name"],
                            "time_start": sess["time_start"],
                            "duration": d, "edge_type": "MAGNET_CLOSE", "prob": p_pdc
                        })
                except Exception:
                    pass
        return setups

    # ── Simulation ──────────────────────────────────────────────────
    def run_simulation(self, setups: list = None, date_filter: pl.Expr = None):
        """
        Simulates qualified setups with realistic friction.
        When date_filter is provided, only simulates on matching dates (OOS).
        Enforces 1 trade per day per symbol (deduplication).
        """
        if setups is None:
            setups = self.qualified_setups

        FRICTION_DEFAULT = 0.1
        FRICTION_INDEX = 0.2
        INDEX_SYMBOLS = {"SP500", "NASDAQ100", "VIX"}
        ATR_LOW, ATR_HIGH = 0.1, 0.8
        traded_day_sym = set()

        for setup in setups:
            sym = setup["symbol"]
            cfg = self.config.get(sym, {})
            df_raw = self.loader.load_data(sym, "M15")
            df_enr = DataEnricher.enrich_with_daily_context(
                df_raw, cfg.get("pd_start", "00:00"), cfg.get("pd_end", "23:59")
            )
            df_or = DataEnricher.enrich_with_opening_range(
                df_enr, setup["time_start"], setup["duration"]
            )

            stats = TrackerEngine.track_events(df_or, tp_multiplier=5.0)

            if date_filter is not None:
                stats = stats.filter(date_filter)

            self.total_days_scanned += stats.height

            valid_days = stats.filter(
                pl.col("first_break_dir").is_in(["UP", "DOWN"])
                & pl.col("or_atr_ratio").is_between(ATR_LOW, ATR_HIGH)
            )

            self.atr_filtered_out += (stats.height - valid_days.height)

            setup_ledger = []
            for row in valid_days.iter_rows(named=True):
                trade_date = row["trade_date"]
                day_key = (str(trade_date), sym)

                # Deduplication: 1 trade per day per symbol
                if day_key in traded_day_sym:
                    continue
                traded_day_sym.add(day_key)

                trade_dir = row["first_break_dir"]
                pnl = 0.0
                friction = FRICTION_INDEX if sym in INDEX_SYMBOLS else FRICTION_DEFAULT

                if setup["edge_type"] == "TREND_UP" and trade_dir == "UP":
                    max_ext = row["max_up"] / row["or_width"] if row["or_width"] > 0 else 0
                    pnl = 1.5 - friction if max_ext >= 1.5 else -1.0 - friction

                elif setup["edge_type"] == "TREND_DW" and trade_dir == "DOWN":
                    max_ext = row["max_down"] / row["or_width"] if row["or_width"] > 0 else 0
                    pnl = 1.5 - friction if max_ext >= 1.5 else -1.0 - friction

                elif setup["edge_type"] == "MAGNET_CLOSE":
                    pd_close = row["pd_close"]
                    or_high = row["or_high"]
                    or_low = row["or_low"]

                    if pd_close is None or or_high is None or or_low is None:
                        continue
                    if or_low <= pd_close <= or_high:
                        continue

                    # Determine magnet direction and check SL chronology
                    if pd_close > or_high:
                        # BUY direction: entry at or_high, SL at or_low
                        time_entry = row["time_entry_up"]
                        time_sl = row["time_sl_up"]
                    else:
                        # SELL direction: entry at or_low, SL at or_high
                        time_entry = row["time_entry_down"]
                        time_sl = row["time_sl_down"]

                    # Must have entry (breakout in magnet direction)
                    if time_entry is None:
                        continue

                    # Check if SL was hit before pd_close was touched
                    if row["touches_pd_close"] > 0:
                        if time_sl is not None and time_sl <= time_entry:
                            pnl = -1.0 - friction
                        else:
                            pnl = 1.0 - friction
                    else:
                        pnl = -1.0 - friction

                if pnl != 0:
                    self.global_ledger.append({
                        "date": trade_date,
                        "symbol": sym,
                        "session": setup["session"],
                        "type": setup["edge_type"],
                        "pnl": pnl
                    })
                    setup_ledger.append(pnl)

            if setup_ledger:
                pnls = np.array(setup_ledger)
                wins = pnls[pnls > 0]
                losses = pnls[pnls < 0]
                win_rate = len(wins) / len(pnls)
                gross_profit = wins.sum()
                gross_loss = abs(losses.sum())
                pf = gross_profit / gross_loss if gross_loss > 0 else 99.9
                equity = np.cumsum(pnls)
                peak = np.maximum.accumulate(equity)
                max_dd = (equity - peak).min() if len(equity) > 0 else 0

                self.setup_results.append({
                    **setup,
                    "trades": len(pnls),
                    "wins": len(wins),
                    "losses": len(losses),
                    "wr": win_rate,
                    "pf": pf,
                    "max_dd": max_dd,
                    "net_pnl": equity[-1]
                })

    # ── Walk-Forward Engine ─────────────────────────────────────────
    def run_walk_forward(self, n_folds: int = 5):
        """
        Expanding-window walk-forward validation.
        Discovers edges on train window, validates on test window.
        Only edges surviving multiple folds are considered robust.
        """
        self.log("Iniciando Walk-Forward Validation...")

        # Determine date range from first asset
        first_sym = list(self.config.keys())[0]
        cfg0 = self.config[first_sym]
        df0 = self._load_enriched(first_sym, cfg0)
        all_dates = df0.select(pl.col("trade_date").cast(pl.Date)).unique().sort("trade_date")
        dates_list = all_dates["trade_date"].to_list()

        total_days = len(dates_list)
        min_train = int(total_days * 0.5)
        fold_size = (total_days - min_train) // n_folds

        fold_results = []
        all_oos_ledger = []
        edge_survival = {}

        for fold in range(n_folds):
            train_end_idx = min_train + fold * fold_size
            test_end_idx = min(train_end_idx + fold_size, total_days)

            if train_end_idx >= total_days or test_end_idx <= train_end_idx:
                break

            train_end_date = dates_list[train_end_idx]
            test_start_date = dates_list[train_end_idx]
            test_end_date = dates_list[test_end_idx - 1]

            self.log(f"  Fold {fold+1}: Train <= {train_end_date} | Test {test_start_date} -> {test_end_date}")

            train_filter = pl.col("trade_date").cast(pl.Date) < train_end_date
            test_filter = (
                (pl.col("trade_date").cast(pl.Date) >= test_start_date)
                & (pl.col("trade_date").cast(pl.Date) <= test_end_date)
            )

            # Scout on train data
            fold_setups = []
            for sym, cfg in self.config.items():
                try:
                    df_enr = self._load_enriched(sym, cfg)
                    setups = self._scout_single(df_enr, sym, cfg, train_filter)
                    fold_setups.extend(setups)
                except Exception:
                    continue

            # Track edge survival across folds
            for s in fold_setups:
                key = (s["symbol"], s["session"], s["duration"], s["edge_type"])
                edge_survival.setdefault(key, 0)
                edge_survival[key] += 1

            # Simulate on test data (OOS)
            self._reset_sim_state()
            self.run_simulation(fold_setups, date_filter=test_filter)

            fold_pnls = [t["pnl"] for t in self.global_ledger]
            all_oos_ledger.extend(self.global_ledger)

            fold_results.append({
                "fold": fold + 1,
                "train_end": str(train_end_date),
                "test_range": f"{test_start_date} -> {test_end_date}",
                "setups_found": len(fold_setups),
                "oos_trades": len(fold_pnls),
                "oos_pnl": sum(fold_pnls),
                "oos_wr": len([p for p in fold_pnls if p > 0]) / max(1, len(fold_pnls))
            })

        # Robust edges = survived in >= 60% of folds
        robust_threshold = max(1, int(n_folds * 0.6))
        robust_edges = {k: v for k, v in edge_survival.items() if v >= robust_threshold}

        self.validation_results["walk_forward"] = {
            "folds": fold_results,
            "edge_survival": {str(k): v for k, v in edge_survival.items()},
            "robust_edges": {str(k): v for k, v in robust_edges.items()},
            "robust_count": len(robust_edges),
            "total_tested": len(edge_survival)
        }

        # Final OOS simulation with only robust edges
        self.log(f"  {len(robust_edges)}/{len(edge_survival)} edges sobrevivieron walk-forward.")
        self._reset_sim_state()
        self.global_ledger = all_oos_ledger
        self.setup_results = []

        # Rebuild setup_results from OOS ledger
        self._rebuild_results_from_ledger()

        return fold_results

    def _reset_sim_state(self):
        self.global_ledger = []
        self.setup_results = []
        self.total_days_scanned = 0
        self.atr_filtered_out = 0

    def _rebuild_results_from_ledger(self):
        """Rebuild setup_results from global_ledger grouped by setup key."""
        if not self.global_ledger:
            return
        df = pl.DataFrame(self.global_ledger)
        groups = df.group_by(["symbol", "session", "type"]).agg([
            pl.col("pnl").count().alias("trades"),
            pl.col("pnl").filter(pl.col("pnl") > 0).count().alias("wins"),
            pl.col("pnl").filter(pl.col("pnl") < 0).count().alias("losses"),
            pl.col("pnl").sum().alias("net_pnl"),
            pl.col("pnl").filter(pl.col("pnl") > 0).sum().alias("gross_profit"),
            pl.col("pnl").filter(pl.col("pnl") < 0).sum().abs().alias("gross_loss"),
        ])
        for row in groups.iter_rows(named=True):
            wr = row["wins"] / max(1, row["trades"])
            pf = row["gross_profit"] / max(0.01, row["gross_loss"]) if row["gross_loss"] else 99.9
            self.setup_results.append({
                "symbol": row["symbol"],
                "session": row["session"],
                "edge_type": row["type"],
                "duration": 0,
                "prob": wr,
                "trades": row["trades"],
                "wins": row["wins"],
                "losses": row["losses"],
                "wr": wr,
                "pf": pf,
                "max_dd": 0,
                "net_pnl": row["net_pnl"]
            })

    # ── Validation Suite ────────────────────────────────────────────
    def run_validations(self):
        """Run Monte Carlo, multiple testing correction, and decay analysis."""
        if not self.global_ledger:
            self.log("No hay trades para validar.")
            return

        pnls = [t["pnl"] for t in self.global_ledger]
        dates = [t["date"] for t in self.global_ledger]

        # Monte Carlo
        self.log("Ejecutando Monte Carlo (10,000 permutaciones)...")
        mc = StatisticalValidator.monte_carlo(pnls, n_sims=10000)
        self.validation_results["monte_carlo"] = mc

        # Multiple Testing Correction
        self.log("Aplicando corrección FDR (Benjamini-Hochberg)...")
        setup_probs = []
        for r in self.setup_results:
            setup_probs.append({
                "label": f"{r['symbol']}_{r['session']}_{r['edge_type']}",
                "wins": r["wins"],
                "trades": r["trades"],
                "observed_wr": r["wr"]
            })
        fdr = StatisticalValidator.multiple_testing_correction(setup_probs)
        self.validation_results["fdr"] = fdr

        # Decay Analysis
        self.log("Analizando decay del edge (ventanas de 1 año)...")
        decay = StatisticalValidator.decay_analysis(pnls, dates)
        self.validation_results["decay"] = decay

    # ── Report Generation ───────────────────────────────────────────
    def generate_report(self):
        if not self.global_ledger:
            self.log("No hay trades para reportar.")
            return

        df_ledger = pl.DataFrame(self.global_ledger).sort("date")
        df_ledger = df_ledger.with_columns(pl.col("pnl").cum_sum().alias("cum_pnl"))

        total_pnl = df_ledger["pnl"].sum()
        total_trades = df_ledger.height
        total_wins = df_ledger.filter(pl.col("pnl") > 0).height
        total_losses = df_ledger.filter(pl.col("pnl") < 0).height
        win_rate = total_wins / total_trades
        gross_p = df_ledger.filter(pl.col("pnl") > 0)["pnl"].sum()
        gross_l = abs(df_ledger.filter(pl.col("pnl") < 0)["pnl"].sum())
        pf = gross_p / gross_l if gross_l > 0 else 99.9

        peak = df_ledger["cum_pnl"].cum_max()
        drawdown = df_ledger["cum_pnl"] - peak
        max_dd = drawdown.min()

        report_path = os.path.join(self.reports_dir, "Portfolio_Alpha_Simulation_Report.md")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# Portfolio Alpha Simulation Report (Walk-Forward OOS)\n\n")
            f.write("> Resultados Out-of-Sample con walk-forward validation, Monte Carlo, corrección FDR y análisis de decay.\n")
            f.write("> Deduplicación: máx 1 trade/día/símbolo. MAGNET_CLOSE filtra pd_close dentro del OR.\n\n")

            # ── Dashboard ───────────────────────────────────────────
            f.write("## Dashboard de Gestión de Riesgo\n")
            f.write("| Métrica | Valor | Descripción |\n")
            f.write("|:---|:---|:---|\n")
            f.write(f"| **PnL Total Neto (OOS)** | `{total_pnl:.2f} R` | Resultado Out-of-Sample después de fricción. |\n")
            f.write(f"| **Win Rate Global** | `{win_rate:.2%}` | Probabilidad de acierto OOS. |\n")
            f.write(f"| **Profit Factor** | `{pf:.2f}` | Ganancia Bruta / Pérdida Bruta. |\n")
            f.write(f"| **Expectativa (R)** | `{total_pnl/total_trades:.3f} R` | Media por trade OOS. |\n")
            f.write(f"| **Máximo Drawdown** | `{max_dd:.2f} R` | Mayor caída desde pico de equidad. |\n")
            f.write(f"| **Total Trades (OOS)** | `{total_trades}` | Trades ejecutados fuera de muestra. |\n\n")

            # ── Walk-Forward Results ────────────────────────────────
            wf = self.validation_results.get("walk_forward", {})
            if wf:
                f.write("## Walk-Forward Validation\n")
                f.write(f"**Edges robustos:** {wf.get('robust_count', 0)}/{wf.get('total_tested', 0)} ")
                f.write(f"(sobrevivieron >= 60% de los folds)\n\n")
                f.write("| Fold | Train hasta | Test | Setups | Trades OOS | PnL OOS | WR OOS |\n")
                f.write("|:---|:---|:---|:---|:---|:---|:---|\n")
                for fold in wf.get("folds", []):
                    f.write(f"| {fold['fold']} | {fold['train_end']} | {fold['test_range']} | "
                            f"{fold['setups_found']} | {fold['oos_trades']} | "
                            f"`{fold['oos_pnl']:.1f} R` | `{fold['oos_wr']:.1%}` |\n")
                f.write("\n")

            # ── Monte Carlo ─────────────────────────────────────────
            mc = self.validation_results.get("monte_carlo", {})
            if mc:
                f.write("## Monte Carlo Simulation (10,000 permutaciones)\n")
                f.write("| Métrica | P5 (Pesimista) | P50 (Mediana) | P95 (Optimista) |\n")
                f.write("|:---|:---|:---|:---|\n")
                f.write(f"| **PnL Final** | `{mc['pnl_p5']:.1f} R` | `{mc['pnl_p50']:.1f} R` | `{mc['pnl_p95']:.1f} R` |\n")
                f.write(f"| **Max Drawdown** | `{mc['dd_p5']:.1f} R` | `{mc['dd_p50']:.1f} R` | `{mc['dd_p95']:.1f} R` |\n")
                f.write(f"\n**Probabilidad de ruina (PnL < 0):** `{mc['prob_ruin']:.1%}`\n\n")

            # ── FDR ─────────────────────────────────────────────────
            fdr = self.validation_results.get("fdr", {})
            if fdr:
                f.write("## Corrección por Multiple Testing (Benjamini-Hochberg FDR)\n")
                f.write(f"**Setups testeados:** {fdr['total_tested']} | ")
                f.write(f"**Significativos post-FDR (alpha=0.05):** {fdr['significant_count']}\n\n")
                if fdr.get("significant_setups"):
                    f.write("| Setup | WR Observado | p-value | p-adj (FDR) | Significativo |\n")
                    f.write("|:---|:---|:---|:---|:---|\n")
                    for s in fdr["significant_setups"][:30]:
                        f.write(f"| {s['label']} | `{s['observed_wr']:.1%}` | "
                                f"`{s['p_value']:.4f}` | `{s['p_adj']:.4f}` | {'Si' if s['significant'] else 'No'} |\n")
                    f.write("\n")

            # ── Decay Analysis ──────────────────────────────────────
            decay = self.validation_results.get("decay", {})
            if decay and decay.get("windows"):
                f.write("## Análisis de Decay del Edge\n")
                f.write("| Período | Trades | WR | PnL (R) | Expectativa | Trend |\n")
                f.write("|:---|:---|:---|:---|:---|:---|\n")
                for w in decay["windows"]:
                    trend = "ESTABLE" if w["expectancy"] > 0.1 else ("DEGRADADO" if w["expectancy"] > 0 else "MUERTO")
                    f.write(f"| {w['period']} | {w['trades']} | `{w['wr']:.1%}` | "
                            f"`{w['pnl']:.1f} R` | `{w['expectancy']:.3f} R` | **{trend}** |\n")
                f.write(f"\n**Decay score:** `{decay.get('decay_score', 0):.2f}` ")
                f.write(f"(1.0 = perfectamente estable, <0.5 = degradación severa)\n\n")

            # ── Setup Breakdown ─────────────────────────────────────
            f.write("## Desglose por Alpha Generator (OOS)\n")
            f.write("| Instrumento | Sesión | Edge | W / L | Win Rate | PF | Net PnL (R) |\n")
            f.write("|:---|:---|:---|:---|:---|:---|:---|\n")
            for r in sorted(self.setup_results, key=lambda x: x['net_pnl'], reverse=True):
                if r['net_pnl'] <= 0:
                    continue
                f.write(f"| **{r['symbol']}** | {r['session']} | `{r['edge_type']}` | "
                        f"{r['wins']} / {r['losses']} | `{r['wr']:.1%}` | "
                        f"`{r['pf']:.2f}` | **{r['net_pnl']:.1f}** |\n")

            # ── Equity Curve ────────────────────────────────────────
            f.write("\n## Curva de Equidad Agregada OOS (Unidades R)\n")
            f.write("```text\n")
            equity = df_ledger["cum_pnl"].to_list()
            max_eq = max(abs(v) for v in equity) if equity else 1
            steps = 40
            chunk = max(1, len(equity) // steps)
            for i in range(0, len(equity), chunk):
                val = equity[i]
                bar_len = int(abs(val) / max(max_eq / 80, 1)) if max_eq > 0 else 0
                bar = "#" * bar_len if val > 0 else "-" * bar_len
                f.write(f"Trades {i:06} | {val:9.2f} R | {bar}\n")
            f.write("```\n\n")

            # ── Risk Architecture ───────────────────────────────────
            f.write("---\n")
            f.write("### Lógica de Protección de Capital y Gestión\n")
            f.write("> Cada operación simulada respeta la siguiente arquitectura de riesgo:\n\n")
            f.write("1. **Costo de Fricción (-0.1R)**: Penalización automática por spreads y comisiones.\n")
            f.write("2. **Hardware Stop Loss (1.1R)**: Stop en extremo opuesto del OR. Pérdida = -1.1R.\n")
            f.write("3. **Asimetría TREND (1.4R Neto)**: TP a 1.5R, neto +1.4R tras fricción.\n")
            f.write("4. **Imán MAGNET (0.9R Neto)**: Dirección dada por posición de pd_close vs OR. Neto +0.9R.\n")
            f.write("5. **Filtro ATR (0.1-0.8)**: No opera si volatilidad fuera de rango.\n")
            f.write("6. **Deduplicación**: Máx 1 trade/día/símbolo.\n")
            f.write("7. **Walk-Forward**: Edges descubiertos en train, validados en test (OOS).\n")
            f.write("8. **FDR**: Solo setups estadísticamente significativos tras corrección.\n")

        self.log(f"Reporte generado: {report_path}")


if __name__ == "__main__":
    ROOT = "c:\\Proyectos\\kha0sys3"
    sim = AlphaPortfolioSimulator(
        data_dir=os.path.join(ROOT, "data"),
        config_path=os.path.join(ROOT, "src", "infrastructure", "config", "asset_config.json"),
        reports_dir=os.path.join(ROOT, "reports")
    )
    # Walk-forward validation (OOS)
    sim.run_walk_forward(n_folds=5)
    # Statistical validations
    sim.run_validations()
    # Generate report with all results
    sim.generate_report()
