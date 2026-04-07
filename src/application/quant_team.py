class QuantTeam:
    """
    Simulates a specialized advisory team (Math, Stats, Algo) that debates
    and suggests strategies, strictly filtering mathematical edges > 60%,
    and brainstorming future cross-dimensional permutations (Feature Engineering).
    """
    
    @staticmethod
    def debate_asset_portfolio(symbol: str, combinations: list) -> str:
        md = f"## 🎯 🧠 Master Quant Team Debate: {symbol}\n\n"
        md += "Nuestro equipo algorítmico ha procesado la matriz omnidireccional. **Atención: Como estándar de nuestro fondo de cobertura simulado, únicamente listaremos esquemas operables que posean un Win Rate (Histórico Real) superior al `60.0%`**. Si las colas distribucionales del activo son aleatorias, nos abstenemos de proponer mecánicas suicidas en él.\n\n"
        
        edges_found = []
        
        for c in combinations:
            sess = f"{c['session_name']} ({c['duration']}m)"
            metrics = c['metrics']
            
            # --- Arquetipo 1: Extensión Macro (Momentum de > 1.5 OR o 1.0 ATR) ---
            if metrics['extensions']['UP']['up_gt_1.5_or'] >= 0.60:
                 edges_found.append(f"- **[EDGE TENDENCIAL UP] {sess}**: Tasa de extensión extrema al alza (1.5x tamaño de caja) del `{metrics['extensions']['UP']['up_gt_1.5_or']:.2%}`. Sugerencia Algo: Disparar *Ruptura de Inercia* persiguiendo TP fijo.")
            if metrics['extensions']['DOWN']['down_gt_1.5_or'] >= 0.60:
                 edges_found.append(f"- **[EDGE TENDENCIAL DOWN] {sess}**: Tasa de extensión polar bajista (1.5x) del `{metrics['extensions']['DOWN']['down_gt_1.5_or']:.2%}`. Sugerencia Algo: Estrategia de continuidad tipo cascada con salidas mecánicas de OR.")
            
            # --- Arquetipo 2: Falsos Rompimientos Extremos (Reversion Trampa) ---
            if metrics['false_breaks']['p_false_breakup'] >= 0.60:
                 edges_found.append(f"- **[EDGE FADE-BREAKOUT] {sess}**: Trampa de Liquidez Alcista del `{metrics['false_breaks']['p_false_breakup']:.2%}`. Cada vez que rompe al alza, termina invalidándose devorando el OR Low. Sugerencia Algo: Stop-Limit en contra de falsos quiebres (Atrapar inversores manuales).")
            if metrics['false_breaks']['p_false_breakdown'] >= 0.60:
                 edges_found.append(f"- **[EDGE FADE-BREAKOUT] {sess}**: Trampa de Liquidez Bajista del `{metrics['false_breaks']['p_false_breakdown']:.2%}`. Sugerencia Algo: Colocar orden de compra ciega si el activo cruza brevemente el piso y titubea.")
                 
            # --- Arquetipo 3: Atracción de Niveles Día Anterior (Institutional Memory Magnet) ---
            if metrics['pd_interactions']['p_touch_pd_close'] >= 0.60:
                edges_found.append(f"- **[EDGE MAGNET PD_CLOSE] {sess}**: Imantación cíclica brutal. El `{metrics['pd_interactions']['p_touch_pd_close']:.2%}` de las veces la volatilidad es mitigada revisitando el Cierre del Día Anterior. Sugerencia Algo: Sistema Mean-Reversion absoluto.")
            if metrics['pd_interactions']['p_touch_pd_mid'] >= 0.60:
                edges_found.append(f"- **[EDGE MAGNET PD_MID] {sess}**: Regreso estricto al Fair-value. Toca el punto medio 50% de liquidez del día previo un `{metrics['pd_interactions']['p_touch_pd_mid']:.2%}` de los eventos evaluados.")

        # Eliminar Edges duplicados usando set si es necesario, pero mantenemos por sesión para fidelidad
        md += "### 🏆 Lógica Mecánica Revelada (> 60% Fidelidad Operativa)\n"
        if not edges_found:
             md += "> ⚠️ **ALERTA DE SISTEMA (PÓLIZA DE RIESGO)**\n"
             md += "> Tras compilar todas las permutaciones históricas de ventana y horario, la asimetría probabilística simple no logró consolidar un nivel de confianza base superior al **60%** en rangos operables o mitigaciones lógicas de reversión. \n"
             md += "> *Resolución:* **NO SE RECOMIENDA AUTOMATIZAR** modelos ciegos para este instrumento empleando estos features puros. Depende excesivamente de macroeconomía exógena (Aleatoriedad predominante intradía).\n\n"
        else:
             md += "> Se han detectado asimetrías de enorme valor predictivo superando los tests empíricos de rigor:\n\n"
             for edge in sorted(list(set(edges_found))):
                 md += f"{edge}\n\n"
                 
        # --- Debate Cuántico Real: Cross-Feature Computed ---
        best_combo = max(
            combinations, 
            key=lambda c: (
                (c['metrics']['false_breaks']['p_false_breakup'] + c['metrics']['false_breaks']['p_false_breakdown'])/2 
                + max(c['metrics']['pd_interactions']['p_touch_pd_close'], c['metrics']['pd_interactions']['p_touch_pd_mid'])
            )
        )
        adv = best_combo['metrics'].get('advanced_crossing', {})
        if adv:
            md += "### 🧪 Laboratorio Quant: Resultados de Feature Crossing Estructural\n"
            md += f"Hemos sometido la mejor matriz base (`{best_combo['session_name']} {best_combo['duration']}m`) a una sub-perforación condicional aislando las variantes de volatilidad extrema y apertura direccional. A continuación la probabilidad neta aislada:\n\n"
            
            def p_edge(d, desc):
                if not d or d.get('n_days', 0) == 0: return ""
                return f"- **{desc}**: Eventos={d['n_days']} | UP: `{d['p_break_up']:.0%}` | Ext 1.5 UP: `{d['up_ext_1.5']:.0%}` | Falsa Ruptura DW: `{d['f_breakdw']:.0%}` | Reversión a PD_Close: `{d.get('touch_pd_close', 0):.0%}`\n"
                
            md += "#### 1. Percentiles de Volatilidad (Ancho del Rango de Apertura en Pips)\n"
            md += p_edge(adv.get('q1_tight_width'), "Rango Ultras Estrecho (Q1)")
            md += p_edge(adv.get('q4_loose_width'), "Rango Masivo Hiper-Volátil (Q4)")
            
            md += "\n#### 2. Relación de Apertura (Memoria de Día Anterior)\n"
            md += p_edge(adv.get('inside_pd_or'), "Apertura Interna (Consolidación atrapada en el OR de ayer)")
            md += p_edge(adv.get('gap_outside_pd_or'), "Apertura en Gap Bidireccional (Desconexión de ayer)")
            
            md += "\n> *Nota de Mesa Operativa:* Analiza si filtrar por un rango apretado (Q1) eleva tu falso rompimiento o detona tu extensión objetivo por encima del base histórico. Si la extensión TENDENCIAL UP salta al 80% en Q1, el sistema de trading debe programar explícitamente: `IF OR_Width < Cuartil_25 THEN EJECUTAR ALGORITMO`.\n"
        
        md += "\n---\n*Los datos presentados son crudos y vectorizados vía Polars. El trading definitivo requerirá acoplar las estrategias en MetaTrader/cTrader.*"
        
        return md
