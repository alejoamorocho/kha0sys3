import os
import json
import polars as pl
from typing import Dict, Any, List, Tuple

from src.infrastructure.data.polars_loader import CSVPolarsLoader
from src.application.calculators import DataEnricher
from src.application.trackers import TrackerEngine
from src.application.statistics import StatisticalEngine
from src.application.quant_team import QuantTeam

class ReportGenerator:
    def __init__(self, data_dir: str, config_path: str, reports_dir: str):
        self.data_dir = data_dir
        self.reports_dir = reports_dir
        self.loader = CSVPolarsLoader(data_dir)
        with open(config_path, "r") as f:
            self.config = json.load(f)
        os.makedirs(reports_dir, exist_ok=True)

    def generate_all(self):
        for sym, cfg in self.config.items():
            print(f"Scouting global parameter Grid for: {sym}...")
            try:
                self._explore_grid(sym, cfg)
            except Exception as e:
                print(f"Failed configuring {sym} statistical profile: {e}")

    def _explore_grid(self, sym: str, cfg: dict):
        df_raw = self.loader.load_data(sym, "M15")
        df_raw = DataEnricher.enrich_with_rsi(df_raw)  # NEW: add RSI before daily context
        df_enriched = DataEnricher.enrich_with_daily_context(df_raw, cfg["pd_start"], cfg["pd_end"])
        
        durations = [15, 30, 45, 60]
        sessions = cfg.get("sessions", [])
        
        combinations = []
        
        for sess in sessions:
            for d_min in durations:
                try:
                    metrics = self._evaluate_combo(df_enriched, sess["time_start"], d_min)
                    if "error" not in metrics:
                        combo_dict = {
                            "session_name": sess["name"],
                            "time_start": sess["time_start"],
                            "duration": d_min,
                            "metrics": metrics
                        }
                        combinations.append(combo_dict)
                except Exception as e:
                    pass
        
        if not combinations:
            print(f"No valid combos for {sym}.")
            return
            
        self._write_markdown(sym, cfg, combinations)

    def _evaluate_combo(self, df_enriched: pl.DataFrame, t_start: str, d_min: int) -> dict:
        df_or = DataEnricher.enrich_with_opening_range(df_enriched, t_start, d_min)
        stats_df = TrackerEngine.track_events(df_or, tp_multiplier=1.5)

        # Collect new feature columns from OR-enriched data
        agg_cols = [
            pl.col("or_open").first(),
            pl.col("pd_or_high").first(),
            pl.col("pd_or_low").first(),
        ]
        # Conditionally add new columns if they exist
        for col_name in ["rsi_at_or_close", "rsi_daily_14", "atr_change",
                          "atr_percentile", "or_position_vs_pd",
                          "or_open_vs_pd_close", "or_open_vs_pd_mid",
                          "or_high_vs_pd_high", "or_low_vs_pd_low"]:
            if col_name in df_or.columns:
                agg_cols.append(pl.col(col_name).first())

        daily_base = df_or.group_by("trade_date").agg(agg_cols)
        expanded_stats = daily_base.join(stats_df, on="trade_date", how="left")

        # Post-fade tracking
        expanded_stats = TrackerEngine.track_post_fade_events(df_or, expanded_stats)

        return StatisticalEngine.calculate_edges(expanded_stats)
        
    def _write_markdown(self, sym: str, cfg: dict, combos: List[dict]):
        md = f"# 🌐 Matriz Probabilística Omnidireccional: {sym}\n\n"
        md += "Este archivo representa la bitácora minera exhaustiva evaluando este activo cruzado por sus múltiples husos horarios y cajas de volatilidad (duraciones de la sesión). Los eventos históricos son depurados sin compasión.\n\n"
        
        # Table of Contents
        md += "## Índice de Permutaciones\n\n"
        for idx, c in enumerate(combos, 1):
            md += f"- [Permutación #{idx}: **{c['session_name']} {c['duration']}m**](#permutación-{idx}-{c['session_name'].lower().replace(' ', '-')}-{c['duration']}m)\n"
        
        md += "\n---\n"
        
        for idx, best in enumerate(combos, 1):
            m = best["metrics"]
            md += f"## Permutación #{idx}: {best['session_name']} {best['duration']}m\n"
            md += f"**Configuración:** Inicia a las `{best['time_start']} UTC`. Tamaño de caja evaluativa: `{best['duration']} minutos`. Días procesados válidos: `{m['total_evaluated_days']}`.\n\n"
            
            md += "### 🧭 Momentum Base Básico\n"
            md += f"- **Rotura Alcista (UP):** `{m['directional']['p_break_up']:.2%}`\n"
            md += f"- **Rotura Bajista (DOWN):** `{m['directional']['p_break_down']:.2%}`\n\n"
            
            md += "### 🎯 Extensiones Geométricas (Target Limits)\n"
            md += "| Multiplicador | Probabilidad Movimiento LUP (UP) | Probabilidad Movimiento DOWN (Cortos) |\n"
            md += "| --- | --- | --- |\n"
            md += f"| 1.0x Rango OR | `{m['extensions']['UP']['up_gt_1_or']:.2%}` | `{m['extensions']['DOWN']['down_gt_1_or']:.2%}` |\n"
            md += f"| 1.5x Rango OR | `{m['extensions']['UP']['up_gt_1.5_or']:.2%}` | `{m['extensions']['DOWN']['down_gt_1.5_or']:.2%}` |\n"
            md += f"| 2.0x Rango OR | `{m['extensions']['UP']['up_gt_2_or']:.2%}` | `{m['extensions']['DOWN']['down_gt_2_or']:.2%}` |\n"
            md += f"| 1.0x Volatilidad ATR Diaria | `{m['extensions']['UP']['up_gt_1_atr']:.2%}` | `{m['extensions']['DOWN']['down_gt_1_atr']:.2%}` |\n\n"
            
            md += "### ⚠️ Vulnerabilidad a Trampas (False Breakouts)\n"
            md += f"- Falsa Ruptura Alcista atrapada en SL contra-caja: `{m['false_breaks']['p_false_breakup']:.2%}`\n"
            md += f"- Falsa Ruptura Bajista atrapada en SL contra-caja: `{m['false_breaks']['p_false_breakdown']:.2%}`\n\n"
            
            md += "### 🧲 Mapeo Hacia Niveles Previo / Atracción de Reversión\n"
            md += f"- % Veces que pos-ruptura el precio cruzó o tocó el Precio de **Cierre Anterior (`PD_Close`)**: `{m['pd_interactions']['p_touch_pd_close']:.2%}`\n"
            md += f"- % Veces que el precio mitigó la Zona Imantada Media de ayer (`PD_Mid`): `{m['pd_interactions']['p_touch_pd_mid']:.2%}`\n"
            md += f"- % Reingreso de validación a la caja Opening Range de ayer (`PD_OR_High/Low` combinados): `{(m['pd_interactions']['p_touch_pd_or_high'] + m['pd_interactions']['p_touch_pd_or_low'])/2:.2%}`\n\n"
            
            md += "---\n\n"
            
        # Call the Quant Team Brainstorming logic processing the entire combinations list
        md += QuantTeam.debate_asset_portfolio(sym, combos)

        file_path = os.path.join(self.reports_dir, f"{sym}_Edge.md")
        with open(file_path, "w", encoding="utf-8") as fw:
            fw.write(md)

if __name__ == "__main__":
    rg = ReportGenerator(
        data_dir="c:/Proyectos/kha0sys3/data",
        config_path="c:/Proyectos/kha0sys3/src/infrastructure/config/asset_config.json",
        reports_dir="c:/Proyectos/kha0sys3/reports"
    )
    rg.generate_all()
