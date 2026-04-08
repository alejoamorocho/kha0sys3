import os
from typing import List, Dict
from src.domain.strategy_models import StrategyDef, StrategyResult


class StrategyReporter:

    def __init__(self, reports_dir: str):
        self.reports_dir = reports_dir
        os.makedirs(reports_dir, exist_ok=True)

    def write_strategy_report(self, result: StrategyResult) -> str:
        s = result.strategy
        filename = f"{s.symbol}_{s.archetype}_{s.session_name}_{s.duration}m"
        if s.context_filter:
            ctx_label = s.context_filter.get("label", "filtered")
            filename += f"_{ctx_label}"
        # Sanitize for Windows: remove characters invalid in filenames
        for ch in ['<', '>', ':', '"', '|', '?', '*', '/', '\\']:
            filename = filename.replace(ch, "")
        filename = filename.replace(" ", "_") + "_Strategy.md"
        filepath = os.path.join(self.reports_dir, filename)

        md = self._build_strategy_md(result)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md)
        return filepath

    def write_asset_summary(self, symbol: str, individual_results: List[StrategyResult],
                            group_result: StrategyResult,
                            selection_explanation: str,
                            all_candidates: List[Dict]) -> str:
        filepath = os.path.join(self.reports_dir, f"{symbol}_Strategy_Summary.md")
        md = self._build_asset_summary_md(symbol, individual_results, group_result,
                                           selection_explanation, all_candidates)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md)
        return filepath

    def _build_strategy_md(self, result: StrategyResult) -> str:
        s = result.strategy
        status = "APROBADA" if result.passes_filter else "NO APROBADA"

        md = f"# Reporte de Estrategia: {s.label}\n\n"
        md += f"**Status:** `[{status}]`\n\n"

        md += "## Definicion de la Estrategia\n\n"
        md += f"| Parametro | Valor |\n"
        md += f"| --- | --- |\n"
        md += f"| Activo | {s.symbol} |\n"
        md += f"| Sesion | {s.session_name} ({s.time_start} UTC) |\n"
        md += f"| Duracion OR | {s.duration} minutos |\n"
        md += f"| Arquetipo | {s.archetype} |\n"
        md += f"| Direccion | {s.direction} |\n"
        md += f"| TP Multiplier | {s.tp_multiplier}x OR |\n"
        if s.context_filter:
            md += f"| Filtro Contextual | `{s.context_filter.get('label', str(s.context_filter))}` |\n"
        md += "\n"

        md += "### Logica de Ejecucion\n\n"
        base_arch = s.archetype.replace("_UP", "").replace("_DOWN", "")
        if base_arch == "MOMENTUM":
            md += f"Entrada en la rotura {'alcista' if s.direction == 'UP' else 'bajista'} del Opening Range. "
            md += f"TP fijo a {s.tp_multiplier}x OR width. SL en el extremo opuesto del OR (1R riesgo).\n\n"
        elif base_arch == "FADE":
            md += f"Entrada CONTRA la rotura {'alcista' if s.direction == 'UP' else 'bajista'}. "
            md += "Cuando el precio rompe el OR, se entra en direccion opuesta apostando a que es un falso rompimiento. "
            md += "TP a 1x OR width (el extremo opuesto). SL a 1x OR width en la direccion del breakout. R:R = 1:1.\n\n"
        elif base_arch == "SHAKEOUT":
            md += f"Re-entrada {'LARGA' if s.direction == 'UP' else 'CORTA'} despues de un falso rompimiento. "
            md += "Espera a que el breakout falle (SL hit), luego re-entra en la direccion original del breakout "
            md += "apostando a que el mercado barre stops y luego continua. TP a 1x OR extension. R:R = 1:1.\n\n"

        if s.context_filter:
            md += f"**Filtro activo:** Solo opera cuando `{s.context_filter.get('col', '')} {s.context_filter.get('op', '')} {s.context_filter.get('val', '')}`\n\n"

        md += "## Resultados del Backtest\n\n"
        md += "### Metricas Principales\n\n"
        md += f"| Metrica | Valor | Umbral |\n"
        md += f"| --- | --- | --- |\n"

        wr_icon = "PASS" if result.win_rate >= 0.65 else "FAIL"
        tpy_icon = "PASS" if result.trades_per_year >= 20 else "FAIL"
        pf_icon = "PASS" if result.profit_factor > 1.0 else "FAIL"

        md += f"| Win Rate | `{result.win_rate:.2%}` | >= 65% [{wr_icon}] |\n"
        md += f"| Trades/Ano | `{result.trades_per_year:.1f}` | >= 20 [{tpy_icon}] |\n"
        md += f"| Profit Factor | `{result.profit_factor:.2f}` | > 1.0 [{pf_icon}] |\n"
        md += f"| Total Trades | `{result.total_trades}` | - |\n"
        md += f"| Net R | `{result.net_r:.2f}R` | - |\n"
        md += f"| R Promedio/Trade | `{result.avg_r_per_trade:.3f}R` | - |\n"
        md += f"| Max Drawdown | `{result.max_drawdown:.2f}R` | - |\n"
        md += f"| Sharpe (anualizado) | `{result.sharpe:.3f}` | - |\n"
        md += "\n"

        if result.yearly_stats:
            md += "### Desglose Anual\n\n"
            md += "| Ano | Trades | Wins | WR | Net R |\n"
            md += "| --- | --- | --- | --- | --- |\n"
            for yr in sorted(result.yearly_stats.keys()):
                ys = result.yearly_stats[yr]
                yr_wr = ys["wr"]
                md += f"| {yr} | {ys['trades']} | {ys['wins']} | `{yr_wr:.1%}` | `{ys['net_r']:.1f}R` |\n"
            md += "\n"
            md += f"**Mejor ano:** {result.best_year} | **Peor ano:** {result.worst_year}\n\n"

        md += "## Veredicto del Equipo Quant\n\n"
        if result.passes_filter:
            md += f"> **ESTRATEGIA APROBADA.** WR={result.win_rate:.1%}, PF={result.profit_factor:.2f}, "
            md += f"{result.trades_per_year:.0f} trades/ano. Edge consistente y explotable.\n"
        else:
            fails = []
            if result.win_rate < 0.65:
                fails.append(f"WR={result.win_rate:.1%} < 65%")
            if result.trades_per_year < 20:
                fails.append(f"Trades/ano={result.trades_per_year:.0f} < 20")
            if result.profit_factor <= 1.0:
                fails.append(f"PF={result.profit_factor:.2f} <= 1.0")
            md += f"> **ESTRATEGIA NO APROBADA.** Falla en: {', '.join(fails)}. "
            md += "Se documenta para referencia pero no se recomienda para operacion.\n"

        md += "\n---\n*Generado por KHA0SYS3 Strategy Pipeline*\n"
        return md

    def write_discovery_report(self, results: List[Dict], total_scanned: int,
                                deployed_count: int) -> str:
        filepath = os.path.join(self.reports_dir, "DISCOVERY_New_Edges.md")

        md = "# KHA0SYS3 - Edge Discovery Report\n\n"
        md += f"**Total permutaciones escaneadas:** {total_scanned}\n"
        md += f"**Estrategias desplegadas (excluidas):** {deployed_count}\n"
        md += f"**Nuevos edges encontrados:** {len(results)}\n"
        md += f"**Filtros:** WR >= 55%, PF > 1.0, N >= 30\n\n"

        if not results:
            md += "> No se encontraron nuevos edges con los criterios establecidos.\n"
        else:
            arch_counts = {}
            for r in results:
                arch_counts[r["archetype"]] = arch_counts.get(r["archetype"], 0) + 1
            md += "## Distribucion por Arquetipo\n\n"
            for arch, count in sorted(arch_counts.items(), key=lambda x: -x[1]):
                md += f"- **{arch}**: {count} edges\n"
            md += "\n"

            asset_counts = {}
            for r in results:
                asset_counts[r["symbol"]] = asset_counts.get(r["symbol"], 0) + 1
            md += "## Distribucion por Activo\n\n"
            for sym, count in sorted(asset_counts.items(), key=lambda x: -x[1]):
                md += f"- **{sym}**: {count} edges\n"
            md += "\n"

            filter_counts = {}
            for r in results:
                fl = r.get("context_label", "BASE")
                filter_counts[fl] = filter_counts.get(fl, 0) + 1
            md += "## Distribucion por Filtro\n\n"
            for fl, count in sorted(filter_counts.items(), key=lambda x: -x[1]):
                md += f"- **{fl}**: {count} edges\n"
            md += "\n"

            md += "## Top Edges (score = WR * log(N) * PF)\n\n"
            md += "| # | Activo | Sesion | Dur | Arquetipo | Filtro | WR | N | T/Ano | PF | NetR | DD | Score |\n"
            md += "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
            for i, r in enumerate(results, 1):
                md += (
                    f"| {i} | {r['symbol']} | {r['session_name']} | {r['duration']}m | "
                    f"{r['archetype']} | {r.get('context_label', 'BASE')} | "
                    f"`{r['win_rate']:.1%}` | {r['n_trades']} | "
                    f"`{r.get('trades_per_year', 0):.0f}` | "
                    f"`{r.get('pf', 0):.2f}` | `{r.get('net_r', 0):.0f}R` | "
                    f"`{r.get('max_dd', 0):.1f}R` | `{r.get('composite', 0):.2f}` |\n"
                )

        md += "\n---\n*Generado por KHA0SYS3 Discovery Pipeline*\n"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md)
        return filepath

    def _build_asset_summary_md(self, symbol: str, results: List[StrategyResult],
                                 group_result: StrategyResult,
                                 selection_explanation: str,
                                 all_candidates: List[Dict]) -> str:
        md = f"# Resumen de Estrategias: {symbol}\n\n"

        md += "## Seleccion del Equipo Quant\n\n"
        md += selection_explanation + "\n"

        md += "## Resultados Individuales\n\n"
        md += "| # | Estrategia | WR | PF | Trades/Ano | Net R | Status |\n"
        md += "| --- | --- | --- | --- | --- | --- | --- |\n"
        for i, r in enumerate(results, 1):
            status = "APROBADA" if r.passes_filter else "NO APROBADA"
            md += f"| {i} | {r.strategy.archetype} {r.strategy.session_name} {r.strategy.duration}m | "
            md += f"`{r.win_rate:.1%}` | `{r.profit_factor:.2f}` | `{r.trades_per_year:.0f}` | "
            md += f"`{r.net_r:.1f}R` | {status} |\n"
        md += "\n"

        md += "## Resultado Grupal (todas las estrategias combinadas)\n\n"
        if group_result.total_trades > 0:
            md += f"| Metrica | Valor |\n"
            md += f"| --- | --- |\n"
            md += f"| Total Trades | `{group_result.total_trades}` |\n"
            md += f"| Trades/Ano | `{group_result.trades_per_year:.1f}` |\n"
            md += f"| Win Rate | `{group_result.win_rate:.2%}` |\n"
            md += f"| Profit Factor | `{group_result.profit_factor:.2f}` |\n"
            md += f"| Net R | `{group_result.net_r:.2f}R` |\n"
            md += f"| Max Drawdown | `{group_result.max_drawdown:.2f}R` |\n"
            md += f"| Sharpe | `{group_result.sharpe:.3f}` |\n"
        else:
            md += "> No se pudieron combinar las estrategias (sin trades validos).\n"

        md += "\n"

        md += "## Top 10 Candidatos Descartados\n\n"
        selected_keys = set()
        for r in results:
            selected_keys.add(f"{r.strategy.archetype}_{r.strategy.session_name}_{r.strategy.duration}")

        discarded = [c for c in all_candidates
                     if f"{c['archetype']}_{c['session_name']}_{c['duration']}" not in selected_keys][:10]
        if discarded:
            md += "| Estrategia | WR | Trades | Razon |\n"
            md += "| --- | --- | --- | --- |\n"
            for c in discarded:
                reason = "Menor WR" if c["win_rate"] < 0.65 else "Duplicado/No complementaria"
                md += f"| {c['archetype']} {c['session_name']} {c['duration']}m {c.get('context_label', '')} | "
                md += f"`{c['win_rate']:.1%}` | {c['n_trades']} | {reason} |\n"
        else:
            md += "> No hay candidatos adicionales.\n"

        md += "\n---\n*Generado por KHA0SYS3 Strategy Pipeline*\n"
        return md
