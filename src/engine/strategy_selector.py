from typing import List, Dict


class StrategySelector:
    TARGET_WR = 0.65
    MAX_STRATEGIES = 3
    MIN_TRADES_FOR_SELECTION = 30

    @classmethod
    def select_top_strategies(cls, candidates: List[Dict]) -> List[Dict]:
        if not candidates:
            return []

        viable = [c for c in candidates if c["n_trades"] >= cls.MIN_TRADES_FOR_SELECTION]
        if not viable:
            return []

        above_target = [c for c in viable if c["win_rate"] >= cls.TARGET_WR]
        below_target = [c for c in viable if c["win_rate"] < cls.TARGET_WR]

        selected = []
        used_archetypes = set()
        used_sessions = set()
        used_directions = set()

        def _diversity_score(candidate: Dict) -> float:
            score = candidate["win_rate"] * 100
            arch = candidate["archetype"]
            sess = candidate["session_name"]
            dirn = candidate["direction"]
            if arch not in used_archetypes:
                score += 10
            if sess not in used_sessions:
                score += 5
            if dirn not in used_directions:
                score += 5
            score += min(candidate["n_trades"] / 100, 5)
            key = f"{arch}_{sess}_{dirn}"
            for s in selected:
                if f"{s['archetype']}_{s['session_name']}_{s['direction']}" == key:
                    score -= 20
            return score

        pool = list(above_target if above_target else below_target)
        while len(selected) < cls.MAX_STRATEGIES and pool:
            scored = [(c, _diversity_score(c)) for c in pool]
            scored.sort(key=lambda x: x[1], reverse=True)
            best = scored[0][0]
            selected.append(best)
            used_archetypes.add(best["archetype"])
            used_sessions.add(best["session_name"])
            used_directions.add(best["direction"])
            pool.remove(best)

        if len(selected) < cls.MAX_STRATEGIES and above_target and below_target:
            for candidate in below_target:
                if len(selected) >= cls.MAX_STRATEGIES:
                    break
                arch = candidate["archetype"]
                sess = candidate["session_name"]
                if arch not in used_archetypes or sess not in used_sessions:
                    if candidate["win_rate"] >= 0.55:
                        selected.append(candidate)
                        used_archetypes.add(arch)
                        used_sessions.add(sess)

        return selected

    @classmethod
    def explain_selection(cls, selected: List[Dict], all_candidates: List[Dict]) -> str:
        md = ""
        total_scanned = len(all_candidates)
        above_65 = sum(1 for c in all_candidates if c["win_rate"] >= cls.TARGET_WR)

        md += f"**Estrategias escaneadas:** {total_scanned}\n"
        md += f"**Con WR >= 65%:** {above_65}\n"
        md += f"**Seleccionadas:** {len(selected)}\n\n"

        if not selected:
            md += "> No se encontraron estrategias viables para este activo.\n"
            return md

        for i, s in enumerate(selected, 1):
            ctx = s.get("context_label", "BASE")
            md += f"**Estrategia #{i}:** {s['archetype']} | {s['session_name']} {s['duration']}m | {ctx}\n"
            md += f"- WR: `{s['win_rate']:.2%}` | Trades: `{s['n_trades']}` | W/L: `{s['wins']}/{s['losses']}`\n"
            reasons = []
            if s["win_rate"] >= cls.TARGET_WR:
                reasons.append("WR supera umbral 65%")
            if i == 1:
                reasons.append("Mejor WR del activo")
            if s["n_trades"] >= 200:
                reasons.append(f"Alta significancia estadistica (N={s['n_trades']})")
            if s.get("context_label") != "BASE":
                reasons.append(f"Filtro contextual activo: {ctx}")
            md += f"- Razon: {', '.join(reasons)}\n\n"

        return md
