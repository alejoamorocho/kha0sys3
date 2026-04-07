import os
import json
import polars as pl
import numpy as np
from datetime import datetime

from src.infrastructure.data.polars_loader import CSVPolarsLoader
from src.application.calculators import DataEnricher
from src.application.trackers import TrackerEngine

class AlphaCompoundingRoadmap:
    def __init__(self, data_dir: str, config_path: str, reports_dir: str):
        self.data_dir = data_dir
        self.reports_dir = reports_dir
        self.loader = CSVPolarsLoader(data_dir)
        with open(config_path, "r") as f:
            self.config = json.load(f)
        os.makedirs(reports_dir, exist_ok=True)
        
        # Selección de Activos "Elite" para Cuenta Pequeña ($1000)
        # Escogidos por: Alta Probabilidad, Bajo Spread, Diferente Horario
        self.elite_setups = [
            {"symbol": "USDJPY", "session": "Tokyo", "time_start": "00:00", "dur": 15, "edge": "MAGNET_CLOSE"},
            {"symbol": "EURUSD", "session": "London", "time_start": "07:00", "dur": 15, "edge": "MAGNET_CLOSE"},
            {"symbol": "NASDAQ100", "session": "Pre-Market", "time_start": "12:00", "dur": 15, "edge": "MAGNET_CLOSE"},
            {"symbol": "XAUUSD", "session": "London", "time_start": "07:00", "dur": 30, "edge": "TREND_UP"}
        ]

    def log(self, msg: str):
        print(f"[ROADMAP] {msg}")

    def run_sequential_simulation(self, start_balance=1000.0, risk_percent=0.035, target=20000.0):
        self.log(f"🚀 Iniciando Hoja de Ruta: ${start_balance} -> ${target}...")
        FRICTION_DEFAULT = 0.1
        FRICTION_INDEX = 0.2
        INDEX_SYMBOLS = {"SP500", "NASDAQ100", "VIX"}

        all_trades = []
        
        # 1. Recolectar todos los trades potenciales de los assets elegidos
        for setup in self.elite_setups:
            try:
                sym = setup["symbol"]
                df_raw = self.loader.load_data(sym, "M15")
                df_enr = DataEnricher.enrich_with_daily_context(df_raw, "00:00", "23:59")
                df_or = DataEnricher.enrich_with_opening_range(df_enr, setup["time_start"], setup["dur"])
                stats = TrackerEngine.track_events(df_or, tp_multiplier=5.0)
                
                valid_days = stats.filter(
                    pl.col("first_break_dir").is_in(["UP", "DOWN"]) & 
                    pl.col("or_atr_ratio").is_between(0.1, 0.8)
                )
                
                for row in valid_days.iter_rows(named=True):
                    pnl = 0.0
                    trade_dir = row["first_break_dir"]
                    
                    friction = FRICTION_INDEX if sym in INDEX_SYMBOLS else FRICTION_DEFAULT

                    if setup["edge"] == "MAGNET_CLOSE":
                        pd_close_val = row["pd_close"]
                        or_high_val = row["or_high"]
                        or_low_val = row["or_low"]

                        if pd_close_val is None or or_high_val is None or or_low_val is None:
                            continue
                        if or_low_val <= pd_close_val <= or_high_val:
                            continue

                        # Determine direction and check SL chronology
                        if pd_close_val > or_high_val:
                            time_entry = row["time_entry_up"]
                            time_sl = row["time_sl_up"]
                        else:
                            time_entry = row["time_entry_down"]
                            time_sl = row["time_sl_down"]

                        if time_entry is None:
                            continue

                        if row["touches_pd_close"] > 0:
                            if time_sl is not None and time_sl <= time_entry:
                                pnl = -1.0 - friction
                            else:
                                pnl = 1.0 - friction
                        else:
                            pnl = -1.0 - friction
                    elif setup["edge"] == "TREND_UP" and trade_dir == "UP":
                        max_ext = row["max_up"] / row["or_width"]
                        pnl = 1.5 - friction if max_ext >= 1.5 else -1.0 - friction
                    
                    if pnl != 0:
                        # Calculamos la hora exacta de ejecución (t_start + dur)
                        h, m = map(int, setup["time_start"].split(':'))
                        exec_time = h + (m + setup["dur"])/60.0
                        
                        all_trades.append({
                            "timestamp": datetime.combine(row["trade_date"], datetime.min.time()).timestamp() + (exec_time * 3600),
                            "date": row["trade_date"],
                            "symbol": sym,
                            "session": setup["session"],
                            "pnl_r": pnl
                        })
            except Exception as e:
                self.log(f"Error procesando {setup['symbol']}: {e}")

        # 2. Ordenar cronológicamente (Muy importante para compuesto)
        all_trades.sort(key=lambda x: x["timestamp"])
        
        # 3. Procesar con Interés Compuesto y Lógica de Margen
        balance = start_balance
        equity_curve = []
        max_balance = start_balance
        max_dd = 0.0
        
        milestones = {2000: None, 5000: None, 10000: None, 20000: None}
        
        for trade in all_trades:
            if balance >= target: break
            
            risk_amount = balance * risk_percent
            profit_loss = trade["pnl_r"] * risk_amount
            
            balance += profit_loss
            
            # Drawdown check
            max_balance = max(max_balance, balance)
            dd = (balance - max_balance) / max_balance
            max_dd = min(max_dd, dd)
            
            equity_curve.append(balance)
            
            # Check milestones
            for m in milestones:
                if balance >= m and milestones[m] is None:
                    milestones[m] = trade["date"]

        self.generate_roadmap_report(start_balance, balance, equity_curve, milestones, max_dd)

    def generate_roadmap_report(self, start, end, curve, milestones, max_dd):
        report_path = os.path.join(self.reports_dir, "Roadmap_1k_to_20k.md")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# 🗺️ Hoja de Ruta Algorítmica: $1,000 ➡️ $20,000\n\n")
            f.write("> **Simulación Cruda**: Basada en interés compuesto (3.5% riesgo) y los 4 pilares de Alpha descubiertos.\n\n")
            
            f.write("## 💹 Resultados de la Travesía\n")
            f.write(f"- **Balance Final:** `${end:,.2f}`\n")
            f.write(f"- **Total Trades:** `{len(curve)}` \n")
            f.write(f"- **Máximo Drawdown (Relativo):** `{max_dd:.2%}`\n")
            f.write(f"- **Riesgo por Trade:** `3.5% Compensado` (Ajustado diariamente al balance).\n\n")
            
            f.write("## 📅 Hitos del Camino (Milestones)\n")
            f.write("| Objetivo | Fecha Alcanzada | Trades Necesarios |\n")
            f.write("|:---|:---|:---|\n")
            for m, date in milestones.items():
                f.write(f"| ${m:,} | {date if date else 'Pendiente'} | {sum(1 for x in curve if x < m)} |\n")
            
            f.write("\n## 🧬 Activos de Ejecución (Margen Eficiente)\n")
            f.write("1. **Tokyo Magnet (USDJPY)**: Estabilizador de madrugada.\n")
            f.write("2. **London Magnet (EURUSD)**: Motor de liquidez matutino.\n")
            f.write("3. **NASDAQ Pre-Market**: El acelerador de crecimiento.\n")
            f.write("4. **Gold Trend**: El diversificador de volatilidad.\n\n")
            
            f.write("## 📈 Gráfico de Crecimiento Exponencial\n")
            f.write("```text\n")
            steps = 40
            chunk = max(1, len(curve) // steps)
            for i in range(0, len(curve), chunk):
                val = curve[i]
                bar = "#" * int(val/500)
                f.write(f"T{i:04} | ${val:9.2f} | {bar}\n")
            f.write("```\n\n")
            
            f.write("--- \n")
            f.write("### 📜 Nota de Gestión de Margen\n")
            f.write("> [!TIP]\n")
            f.write("> Con una cuenta de $1,000, un riesgo del 3.5% ($35) equivale aproximadamente a 0.03/0.05 lotes en divisas. Esto deja margen suficiente para 2-3 operaciones simultáneas sin riesgo de 'Margin Call'.\n")

        self.log(f"✅ Reporte de Hoja de Ruta generado en: {report_path}")

if __name__ == "__main__":
    import sys
    ROOT = "c:\\Proyectos\\kha0sys3"
    roadmap = AlphaCompoundingRoadmap(
        data_dir=os.path.join(ROOT, "data"),
        config_path=os.path.join(ROOT, "src", "infrastructure", "config", "asset_config.json"),
        reports_dir=os.path.join(ROOT, "reports")
    )
    roadmap.run_sequential_simulation()
