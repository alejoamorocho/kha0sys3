import polars as pl
import json
import os
import optuna
import numpy as np
import matplotlib.pyplot as plt

from src.infrastructure.data.polars_loader import CSVPolarsLoader
from src.application.calculators import DataEnricher
from src.application.trackers import TrackerEngine
from src.engine.report_generator import ReportGenerator

class EdgeOptimizer:
    def __init__(self, data_dir: str, config_path: str):
        self.loader = CSVPolarsLoader(data_dir)
        with open(config_path, "r") as f:
            self.config = json.load(f)
        self.rg = ReportGenerator(data_dir, config_path, "reports")
        self.all_qualified_edges = {}

    def log(self, text):
        with open("optuna_log.txt", "a", encoding="utf-8") as f:
            f.write(text + "\n")

    def extract_top_edges(self):
        """Scans the portfolio and isolates ALL setups strictly >65%"""
        open("optuna_log.txt", "w", encoding="utf-8").close()  # Clear log
        self.log("🔍 Extrayendo config empíricas MASIVAS (>65%) del universo...")
        for sym, cfg in self.config.items():
            try:
                df_raw = self.loader.load_data(sym, "M15")
                df_enr = DataEnricher.enrich_with_daily_context(df_raw, cfg["pd_start"], cfg["pd_end"])
            except Exception as e:
                print(f"[WARN] Loading data for {sym}: {e}")
                continue
                
            sessions = cfg.get("sessions", [])
            durations = [15, 30, 45, 60]
            
            valid_setups = []
            
            for sess in sessions:
                for d in durations:
                    try:
                        metrics = self.rg._evaluate_combo(df_enr, sess["time_start"], d)
                        if "error" in metrics: continue
                        
                        p_up = metrics['extensions']['UP']['up_gt_1.5_or']
                        p_dw = metrics['extensions']['DOWN']['down_gt_1.5_or']
                        p_fup = metrics['false_breaks']['p_false_breakup']
                        p_fdw = metrics['false_breaks']['p_false_breakdown']
                        p_pdc = metrics['pd_interactions']['p_touch_pd_close']
                        
                        max_local = max(p_up, p_dw, p_fup, p_fdw, p_pdc)
                        if max_local >= 0.65:
                            valid_setups.append({
                                "session": sess["name"], 
                                "time_start": sess["time_start"], 
                                "duration": d, 
                                "max_edge_prob": max_local,
                                "type_score": "UP_Ext" if max_local == p_up else "DW_Ext" if max_local == p_dw else "Fade_UP" if max_local == p_fup else "Fade_DW" if max_local == p_fdw else "PD_Close_Magnet"
                            })
                    except Exception as e:
                        print(f"[WARN] Evaluating {sym} {sess['name']} {d}m: {e}")
                        
            if valid_setups:
                self.all_qualified_edges[sym] = valid_setups
                for s in valid_setups:
                    self.log(f"✅ {sym}: {s['session']} {s['duration']}m | Edge: {s['max_edge_prob']:.2%} | Type: {s['type_score']}")
            else:
                self.log(f"❌ {sym}: Descartado. No súperó ninguna rama del 65% absoluto.")
                
    def optimize_portfolio(self):
        if not self.all_qualified_edges:
            self.log("No hay assets válidos para optimizar.")
            return

        tear_sheet_data = []
        global_ledger = [] # To store dicts of {"date": date, "pnl": r_units}

        for sym, setups in self.all_qualified_edges.items():
            df_raw = self.loader.load_data(sym, "M15")
            cfg = self.config[sym]
            df_enr = DataEnricher.enrich_with_daily_context(df_raw, cfg["pd_start"], cfg["pd_end"])
            
            for setup in setups:
                self.log(f"\n🧬 Iniciando Genética para: {sym} ({setup['session']} {setup['duration']}m)")
                df_or = DataEnricher.enrich_with_opening_range(df_enr, setup["time_start"], setup["duration"])
                
                def objective(trial):
                    tp_narrow = trial.suggest_float("tp_narrow", 0.5, 5.0, step=0.1)
                    tp_normal = trial.suggest_float("tp_normal", 0.5, 5.0, step=0.1)
                    tp_wide = trial.suggest_float("tp_wide", 0.5, 5.0, step=0.1)
                    
                    FRICTION = 0.1
                    stats = TrackerEngine.track_events(df_or, tp_multiplier=5.0) # Track max extensions
                    
                    # Sync Filter: Enforce the same volatility window as the Live Bot (0.1 - 0.8 ATR)
                    valid_days = stats.filter(
                        pl.col("first_break_dir").is_in(["UP", "DOWN"]) & 
                        pl.col("or_atr_ratio").is_between(0.1, 0.8)
                    )
                    if valid_days.height == 0: return -1.0
                    
                    def calculate_pnl(row):
                        ratio = row["or_atr_ratio"]
                        tp = tp_narrow if ratio < 0.3 else tp_normal if ratio < 0.6 else tp_wide

                        dir = row["first_break_dir"]
                        max_ext = row["max_up"] / row["or_width"] if dir == "UP" else row["max_down"] / row["or_width"]

                        # Check SL chronology
                        time_sl = row.get(f"time_sl_{dir.lower()}")
                        time_tp = row.get(f"time_tp_{dir.lower()}")

                        if max_ext >= tp:
                            # TP level reached, but did SL hit first?
                            if time_sl is not None and (time_tp is None or time_sl <= time_tp):
                                return -1.0 - FRICTION
                            return tp - FRICTION
                        else:
                            return -1.0 - FRICTION
                        
                    pnls = [calculate_pnl(row) for row in valid_days.iter_rows(named=True)]
                    expectancy = sum(pnls) / len(pnls)
                    
                    # Penalty for low trade count in a bucket
                    if len(pnls) < 10: return -1.0
                    return expectancy

                study = optuna.create_study(direction="maximize")
                optuna.logging.set_verbosity(optuna.logging.WARNING)
                study.optimize(objective, n_trials=100)
                
                if len(study.trials) > 0 and study.best_value > -1.0:
                    best = study.best_params
                    best_val = study.best_value
                    
                    tp_min, tp_max = 0.5, 5.0
                    boundary_hit = ""
                    # Evaluar si alguna de las 3 cubetas tocó los límites
                    for k, v in best.items():
                        if abs(v - tp_min) < 0.01: boundary_hit += f"⚠️ Min {k} "
                        elif abs(v - tp_max) < 0.01: boundary_hit += f"⚠️ Max {k} "
                    
                    if not boundary_hit: boundary_hit = "Ok"
                    
                    stats_final = TrackerEngine.track_events(df_or, tp_multiplier=5.0) 
                    valid_final = stats_final.filter(
                        pl.col("first_break_dir").is_in(["UP", "DOWN"]) & 
                        pl.col("or_atr_ratio").is_between(0.1, 0.8)
                    )
                    
                    r_curves = []
                    gross_profit, gross_loss = 0.0, 0.0
                    FRICTION = 0.1
                    
                    for row in valid_final.iter_rows(named=True):
                        ratio = row["or_atr_ratio"]
                        tp = best['tp_narrow'] if ratio < 0.3 else best['tp_normal'] if ratio < 0.6 else best['tp_wide']
                        
                        dir = row["first_break_dir"]
                        max_ext = row["max_up"] / row["or_width"] if dir == "UP" else row["max_down"] / row["or_width"]
                        trade_date = row["trade_date"]
                        
                        # Check SL chronology
                        time_sl = row.get(f"time_sl_{dir.lower()}")
                        time_tp = row.get(f"time_tp_{dir.lower()}")

                        if max_ext >= tp and not (time_sl is not None and (time_tp is None or time_sl <= time_tp)):
                            r_net = tp - FRICTION
                        else:
                            r_net = -1.0 - FRICTION
                        
                        if r_net != 0.0:
                            r_curves.append(r_net)
                            global_ledger.append({"date": trade_date, "pnl": r_net})
                            if r_net > 0: gross_profit += r_net
                            else: gross_loss += abs(r_net)
                            
                    if not r_curves: continue
                    returns_arr = np.array(r_curves)
                    win_rate_final = returns_arr[returns_arr > 0].size / max(1, returns_arr[returns_arr != 0].size)
                    equity = np.cumsum(returns_arr)
                    max_dd = np.min(equity - np.maximum.accumulate(equity)) if len(equity) > 0 else 0.0
                    sharpe = (np.mean(returns_arr) / np.std(returns_arr)) if len(returns_arr) > 1 and np.std(returns_arr) > 0 else 0.0
                    pf = (gross_profit / max(1.0, gross_loss)) if gross_loss > 0 else float('inf')
                    
                    tear_sheet_data.append({
                        "symbol": sym,
                        "setup": f"{setup['session']} {setup['duration']}m",
                        "tp_opt": f"N:{best['tp_narrow']:.1f} M:{best['tp_normal']:.1f} W:{best['tp_wide']:.1f}",
                        "boundary": boundary_hit,
                        "trades": len(r_curves),
                        "wr": f"{win_rate_final:.2%}",
                        "max_dd": f"{max_dd:.2f}",
                        "pf": f"{pf:.2f}",
                        "sharpe": f"{sharpe:.3f}",
                        "net_pnl": f"{equity[-1]:.2f}",
                        "exp": f"{best_val:.2f}"
                    })
                    self.log(f"⭐ Optimal Expectancy para {sym}: {best_val:.2f} R | Matrix: {tear_sheet_data[-1]['tp_opt']}")

        # -------- GENERACIÓN TABLA MARKDOWN A NIVEL TEAR SHEET --------
        ts_md = "# 🏆 Portfolio Optimization Master Tear Sheet (ADAPTIVE)\n\n"
        ts_md += "A continuación todas las matrices paramétricas optimizadas con FRICCIÓN (0.1R), FILTRO ATR (0.1-0.8) y TARGET DINÁMICO (Adaptive TP).\n\n"
        
        # Markdown aligned format
        ts_md += "| Instrument | Winning Setup (+65% Base) | Dynamic TP Matrix (N/M/W) | Boundary Warning? | # Trades | Net Win Rate | Max Drawdown | Profit Factor | Sharpe Ratio | Net PnL (R-Net) | Exp (Net) |\n"
        ts_md += "|:-----------|:--------------------------|:--------------------------|:------------------|:---------|:-------------|:-------------|:--------------|:-------------|:------------|:----------|\n"
        
        for d in tear_sheet_data:
            ts_md += f"| **{d['symbol']}** | `{d['setup']}` | `{d['tp_opt']}x` | {d['boundary']} | {d['trades']} | {d['wr']} | {d['max_dd']} | {d['pf']} | {d['sharpe']} | **{d['net_pnl']}** | {d['exp']} |\n"
            
        with open("c:/Proyectos/kha0sys3/reports/Portfolio_Optimization_TearSheet.md", "w", encoding="utf-8") as f:
            f.write(ts_md)
            
        # -------- GENERACIÓN PORTFOLIO GLOBAL PARALELO --------
        if global_ledger:
            self.log("\n🌐 Generando Ledger Consolidado de Cuentas...")
            ledger_df = pl.DataFrame(global_ledger)
            # Agrupar pnl neto ganado por todos los robots en el transcurso del mismo día!
            daily_portfolio = ledger_df.group_by("date").agg(pl.col("pnl").sum().alias("net_r")).sort("date")
            
            pnl_series = daily_portfolio["net_r"].to_numpy()
            dates_series = daily_portfolio["date"].to_numpy()
            
            global_equity = np.cumsum(pnl_series)
            global_peak = np.maximum.accumulate(global_equity)
            global_dd = global_equity - global_peak
            global_max_dd = np.min(global_dd)
            
            gross_p_gl = pnl_series[pnl_series > 0].sum()
            gross_l_gl = abs(pnl_series[pnl_series < 0].sum())
            global_pf = (gross_p_gl / gross_l_gl) if gross_l_gl > 0 else float('inf')
            
            wins_gl = pnl_series[pnl_series > 0].size
            total_gl = pnl_series[pnl_series != 0].size
            global_wr = wins_gl / max(1, total_gl)
            global_sharpe = (np.mean(pnl_series) / np.std(pnl_series)) if np.std(pnl_series) > 0 else 0.0
            
            self.log(f"--- Ficha de Rendimiento Institucional (Cuenta Unificada) ---")
            self.log(f"Trades Diarios Transaccionados: {total_gl}")
            self.log(f"Win Rate Sumado Neta: {global_wr:.2%}")
            self.log(f"Profit Factor Central: {global_pf:.2f}")
            self.log(f"Sharpe Ratio Global: {global_sharpe:.3f}")
            self.log(f"Max Drawdown Unificado: {global_max_dd:.2f} R-Units Máximo Dolor Correlacionado")
            self.log(f"Curva Final Creciente Absoluta: +{global_equity[-1]:.2f} R-Units en Retorno Base Libre de Composición")
            
            # Gráfico de matplotlib
            plt.figure(figsize=(14, 7))
            plt.plot(np.arange(len(global_equity)), global_equity, label='Global Portfolio Equity (R-Units)', color='green', linewidth=2)
            plt.fill_between(np.arange(len(global_equity)), global_equity, alpha=0.1, color='green')
            plt.title('Aggregate Simulated Fund (Concurrent Robot Execution)')
            plt.xlabel('Simulated Trading Days (Time ->)')
            plt.ylabel('Cumulative Net Returns (Risk Units)')
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.legend()
            plt.tight_layout()
            plt.savefig('c:/Proyectos/kha0sys3/portfolio_curve.png')
            self.log("Curva gráfica guardada como portfolio_curve.png")

if __name__ == "__main__":
    opt = EdgeOptimizer('c:/Proyectos/kha0sys3/data', 'c:/Proyectos/kha0sys3/src/infrastructure/config/asset_config.json')
    opt.extract_top_edges()
    opt.optimize_portfolio()
