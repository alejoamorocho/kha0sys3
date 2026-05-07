"""Bootstrap Monte Carlo de listas de trades."""

import random

from src.strategies_external.common.trade import Trade


def monte_carlo_bootstrap(
    trades: list[Trade],
    n_simulations: int = 10_000,
    ruin_threshold_R: float = -15.0,
    seed: int | None = None,
) -> dict[str, float]:
    """Re-ordena trades aleatoriamente N veces; calcula prob_ruin y DD quantiles.

    `prob_ruin` = fraccion de simulaciones cuyo equity (en R) toco ruin_threshold_R.
    """
    if not trades:
        raise ValueError("empty trade list")

    rng = random.Random(seed)
    pnl_Rs = [t.pnl_R for t in trades]
    n = len(pnl_Rs)

    ruin_count = 0
    dds: list[float] = []
    finals: list[float] = []

    for _ in range(n_simulations):
        permuted = rng.sample(pnl_Rs, n)
        cum = 0.0
        peak = 0.0
        max_dd = 0.0
        ruined = False
        for r in permuted:
            cum += r
            if cum <= ruin_threshold_R:
                ruined = True
            peak = max(peak, cum)
            max_dd = max(max_dd, peak - cum)
        if ruined:
            ruin_count += 1
        dds.append(max_dd)
        finals.append(cum)

    dds.sort()
    finals.sort()

    def q(arr: list[float], pct: float) -> float:
        idx = int(pct * (len(arr) - 1))
        return arr[idx]

    return {
        "prob_ruin": ruin_count / n_simulations,
        "dd_q5_R": q(dds, 0.05),
        "dd_q50_R": q(dds, 0.50),
        "dd_q95_R": q(dds, 0.95),
        "final_q5_R": q(finals, 0.05),
        "final_q50_R": q(finals, 0.50),
        "final_q95_R": q(finals, 0.95),
        "n_simulations": n_simulations,
    }
