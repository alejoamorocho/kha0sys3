import numpy as np
from scipy import stats as scipy_stats
from typing import List, Dict, Any
from datetime import date


class StatisticalValidator:
    """
    Suite de validación estadística para backtests de trading.
    Monte Carlo, FDR (Benjamini-Hochberg), y análisis de decay.
    """

    @staticmethod
    def monte_carlo(pnls: List[float], n_sims: int = 10000) -> Dict[str, Any]:
        """
        Bootstrap with replacement: resamples trades to generate
        different PnL sequences with varying final outcomes.
        Also computes drawdown distribution.
        """
        pnls_arr = np.array(pnls)
        n = len(pnls_arr)
        if n == 0:
            return {"error": "No trades"}

        final_pnls = np.zeros(n_sims)
        max_drawdowns = np.zeros(n_sims)

        rng = np.random.default_rng(42)
        for i in range(n_sims):
            # Bootstrap: sample WITH replacement
            sample = rng.choice(pnls_arr, size=n, replace=True)
            equity = np.cumsum(sample)
            final_pnls[i] = equity[-1]
            peak = np.maximum.accumulate(equity)
            max_drawdowns[i] = (equity - peak).min()

        return {
            "n_sims": n_sims,
            "n_trades": n,
            "pnl_p5": float(np.percentile(final_pnls, 5)),
            "pnl_p25": float(np.percentile(final_pnls, 25)),
            "pnl_p50": float(np.percentile(final_pnls, 50)),
            "pnl_p75": float(np.percentile(final_pnls, 75)),
            "pnl_p95": float(np.percentile(final_pnls, 95)),
            "pnl_mean": float(final_pnls.mean()),
            "pnl_std": float(final_pnls.std()),
            "dd_p5": float(np.percentile(max_drawdowns, 5)),
            "dd_p50": float(np.percentile(max_drawdowns, 50)),
            "dd_p95": float(np.percentile(max_drawdowns, 95)),
            "prob_ruin": float((final_pnls < 0).mean()),
            "prob_profit": float((final_pnls > 0).mean()),
        }

    @staticmethod
    def multiple_testing_correction(
        setup_stats: List[Dict], alpha: float = 0.05, null_wr: float = 0.5
    ) -> Dict[str, Any]:
        """
        Benjamini-Hochberg FDR correction.
        Tests H0: win_rate <= null_wr for each setup.
        MAGNET_CLOSE uses null_wr=0.55 (breakeven WR).
        """
        if not setup_stats:
            return {"error": "No setups"}

        results = []
        for s in setup_stats:
            n = s["trades"]
            k = s["wins"]
            if n < 10:
                continue
            # Edge-specific null: MAGNET breakeven is 55%, TREND is 50%
            effective_null = 0.55 if "MAGNET" in s.get("label", "") else null_wr
            p_value = 1.0 - scipy_stats.binom.cdf(k - 1, n, effective_null)
            results.append({
                "label": s["label"],
                "trades": n,
                "wins": k,
                "observed_wr": s["observed_wr"],
                "null_wr": effective_null,
                "p_value": p_value
            })

        if not results:
            return {"total_tested": 0, "significant_count": 0, "significant_setups": []}

        results.sort(key=lambda x: x["p_value"])
        m = len(results)

        for i, r in enumerate(results):
            bh_threshold = alpha * (i + 1) / m
            r["p_adj"] = min(r["p_value"] * m / (i + 1), 1.0)
            r["significant"] = r["p_value"] <= bh_threshold

        for i in range(m - 2, -1, -1):
            results[i]["p_adj"] = min(results[i]["p_adj"], results[i + 1]["p_adj"])

        significant = [r for r in results if r["significant"]]

        return {
            "total_tested": m,
            "significant_count": len(significant),
            "alpha": alpha,
            "null_wr": null_wr,
            "significant_setups": results
        }

    @staticmethod
    def decay_analysis(
        pnls: List[float], dates: list, window_days: int = 365
    ) -> Dict[str, Any]:
        """
        Analiza si el edge se mantiene, mejora o degrada en ventanas temporales.
        """
        if not pnls or not dates:
            return {"error": "No data"}

        # Convert dates to ordinal for grouping
        date_ordinals = []
        for d in dates:
            if isinstance(d, date):
                date_ordinals.append(d.toordinal())
            else:
                date_ordinals.append(date.fromisoformat(str(d)).toordinal())

        arr_pnl = np.array(pnls)
        arr_ord = np.array(date_ordinals)

        min_ord = arr_ord.min()
        max_ord = arr_ord.max()

        windows = []
        start = min_ord
        while start < max_ord:
            end = start + window_days
            mask = (arr_ord >= start) & (arr_ord < end)
            w_pnls = arr_pnl[mask]

            if len(w_pnls) >= 10:
                w_wins = (w_pnls > 0).sum()
                wr = w_wins / len(w_pnls)
                total_pnl = w_pnls.sum()
                exp = total_pnl / len(w_pnls)

                start_date = date.fromordinal(int(start))
                end_date = date.fromordinal(min(int(end), int(max_ord)))

                windows.append({
                    "period": f"{start_date.isoformat()} -> {end_date.isoformat()}",
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "trades": len(w_pnls),
                    "wr": float(wr),
                    "pnl": float(total_pnl),
                    "expectancy": float(exp)
                })

            start = end

        if len(windows) < 2:
            return {"windows": windows, "decay_score": 1.0, "decay_p_value": None,
                    "trend": "ESTABLE"}

        expectancies = [w["expectancy"] for w in windows]

        if len(expectancies) >= 3:
            from scipy.stats import spearmanr
            x = list(range(len(expectancies)))
            corr, p_value = spearmanr(x, expectancies)
            # Map: corr -1..+1 -> decay_score 0..2 (1.0 = stable)
            decay_score = 1.0 + corr
            decay_p_value = p_value
        else:
            first_half = np.mean(expectancies[:len(expectancies)//2])
            second_half = np.mean(expectancies[len(expectancies)//2:])
            if first_half > 0:
                decay_score = second_half / first_half
            elif first_half == 0:
                decay_score = 1.0 if second_half >= 0 else 0.0
            else:
                decay_score = 0.0
            decay_score = max(0.0, min(2.0, decay_score))
            decay_p_value = None

        return {
            "windows": windows,
            "decay_score": float(decay_score),
            "decay_p_value": float(decay_p_value) if decay_p_value is not None else None,
            "trend": "MEJORANDO" if decay_score > 1.1 else (
                "ESTABLE" if decay_score >= 0.7 else (
                    "DEGRADANDO" if decay_score >= 0.3 else "COLAPSANDO"
                )
            )
        }
