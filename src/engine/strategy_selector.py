from typing import List, Dict


class StrategySelector:
    TARGET_WR = 0.65
    MAX_STRATEGIES = 3
    MIN_TRADES_FOR_SELECTION = 20

    @classmethod
    def select_top_strategies(cls, candidates: List[Dict]) -> List[Dict]:
        """
        Quant team selection logic:
        - Slot 1: Best volume strategy (highest N * WR product, prefers BASE)
        - Slot 2: Best complementary strategy (different archetype/session/direction)
        - Slot 3: Third best that complements both
        Balances win rate with statistical significance and trade volume.
        """
        if not candidates:
            return []

        viable = [c for c in candidates if c["n_trades"] >= cls.MIN_TRADES_FOR_SELECTION]
        if not viable:
            return []

        selected = []
        used_keys = set()

        def _combo_key(c: Dict) -> str:
            return f"{c['archetype']}_{c['session_name']}_{c['duration']}_{c.get('context_label', 'BASE')}"

        def _selection_score(candidate: Dict, slot: int) -> float:
            wr = candidate["win_rate"]
            n = candidate["n_trades"]
            is_base = candidate.get("context_label", "BASE") == "BASE"

            # Core score: WR * log(N) to balance quality and quantity
            import math
            score = wr * math.log(max(n, 1)) * 10

            # Slot 1: Prefer BASE strategies with high volume
            if slot == 1:
                if is_base:
                    score += 20
                if n >= 200:
                    score += 15
                elif n >= 100:
                    score += 10

            # Slots 2-3: Prefer diversity
            if slot >= 2:
                arch = candidate["archetype"]
                sess = candidate["session_name"]
                dirn = candidate["direction"]

                # Bonus for new archetype/session/direction
                used_archs = {s["archetype"] for s in selected}
                used_sess = {s["session_name"] for s in selected}
                used_dirs = {s["direction"] for s in selected}

                if arch not in used_archs:
                    score += 15
                if sess not in used_sess:
                    score += 10
                if dirn not in used_dirs:
                    score += 8

                # Penalty for near-duplicate
                for s in selected:
                    if (s["archetype"] == arch and s["session_name"] == sess
                            and s["duration"] == candidate["duration"]):
                        score -= 30

            # WR bonus
            if wr >= cls.TARGET_WR:
                score += 10

            return score

        # Select slot by slot
        for slot in range(1, cls.MAX_STRATEGIES + 1):
            remaining = [c for c in viable if _combo_key(c) not in used_keys]
            if not remaining:
                break

            scored = [(c, _selection_score(c, slot)) for c in remaining]
            scored.sort(key=lambda x: x[1], reverse=True)
            best = scored[0][0]
            selected.append(best)
            used_keys.add(_combo_key(best))

        return selected

    @classmethod
    def explain_selection(cls, selected: List[Dict], all_candidates: List[Dict]) -> str:
        md = ""
        total_scanned = len(all_candidates)
        above_65 = sum(1 for c in all_candidates if c["win_rate"] >= cls.TARGET_WR)
        base_candidates = [c for c in all_candidates if c.get("context_label", "BASE") == "BASE"]
        best_base_wr = max((c["win_rate"] for c in base_candidates), default=0)

        md += f"**Estrategias escaneadas:** {total_scanned}\n"
        md += f"**Con WR >= 65%:** {above_65}\n"
        md += f"**Mejor WR base (sin filtro):** `{best_base_wr:.2%}`\n"
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
                reasons.append("Mejor score volumen-calidad")
            if s["n_trades"] >= 200:
                reasons.append(f"Alta significancia estadistica (N={s['n_trades']})")
            if ctx != "BASE":
                reasons.append(f"Filtro contextual: {ctx}")
            else:
                reasons.append("Estrategia base (todas las condiciones)")
            md += f"- Razon: {', '.join(reasons)}\n\n"

        return md
