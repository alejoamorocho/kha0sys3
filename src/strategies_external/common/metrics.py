"""Metricas estandar para evaluar listas de Trade."""

import math

from src.strategies_external.common.trade import Trade


def evaluate(trades: list[Trade]) -> dict[str, float]:
    if not trades:
        return {
            "n_trades": 0, "win_rate": 0.0, "profit_factor": 0.0,
            "expectancy_R": 0.0, "avg_win_R": 0.0, "avg_loss_R": 0.0,
            "max_dd_R": 0.0, "max_dd_pct": 0.0, "sharpe": 0.0,
            "sortino": 0.0, "calmar": 0.0, "total_R": 0.0,
        }

    sorted_trades = sorted(trades, key=lambda t: t.entry_ts)
    pnl_Rs = [t.pnl_R for t in sorted_trades]
    n = len(pnl_Rs)
    wins = [r for r in pnl_Rs if r > 0]
    losses = [r for r in pnl_Rs if r <= 0]
    win_rate = len(wins) / n
    sum_wins = sum(wins)
    sum_losses_abs = abs(sum(losses))
    profit_factor = (sum_wins / sum_losses_abs) if sum_losses_abs > 0 else float("inf")
    expectancy = sum(pnl_Rs) / n
    avg_win = (sum_wins / len(wins)) if wins else 0.0
    avg_loss = (sum(losses) / len(losses)) if losses else 0.0

    # Drawdown sobre equity acumulado (en R)
    equity = []
    cum = 0.0
    for r in pnl_Rs:
        cum += r
        equity.append(cum)
    peak = equity[0]
    max_dd = 0.0
    for v in equity:
        peak = max(peak, v)
        dd = peak - v
        if dd > max_dd:
            max_dd = dd

    pnl_pcts = [t.pnl_pct for t in sorted_trades]
    cum_pct = 0.0
    peak_pct = 0.0
    max_dd_pct = 0.0
    for r in pnl_pcts:
        cum_pct += r
        peak_pct = max(peak_pct, cum_pct)
        max_dd_pct = max(max_dd_pct, peak_pct - cum_pct)

    # Sharpe / Sortino: convencion simple, mean / std de pnl_R; rf=0.
    mean_r = sum(pnl_Rs) / n
    var = sum((r - mean_r) ** 2 for r in pnl_Rs) / n
    std = math.sqrt(var)
    sharpe = (mean_r / std) if std > 0 else 0.0

    downside = [min(0.0, r - mean_r) for r in pnl_Rs]
    down_var = sum(d ** 2 for d in downside) / n
    down_std = math.sqrt(down_var)
    sortino = (mean_r / down_std) if down_std > 0 else 0.0

    total_R = sum(pnl_Rs)
    calmar = (total_R / max_dd) if max_dd > 0 else 0.0

    return {
        "n_trades": n,
        "win_rate": win_rate,
        "profit_factor": profit_factor,
        "expectancy_R": expectancy,
        "avg_win_R": avg_win,
        "avg_loss_R": avg_loss,
        "max_dd_R": max_dd,
        "max_dd_pct": max_dd_pct,
        "sharpe": sharpe,
        "sortino": sortino,
        "calmar": calmar,
        "total_R": total_R,
    }
