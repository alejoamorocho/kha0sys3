from datetime import datetime, timedelta
from pathlib import Path

from src.strategies_external.common.trade import Trade
from src.strategies_external.reporting.markdown import write_backtest_report
from src.strategies_external.common.walk_forward import walk_forward_split
from src.strategies_external.common.monte_carlo import monte_carlo_bootstrap


def _trade(day: int, pnl_R: float, mode: str = "doc") -> Trade:
    base = datetime(2024, 1, 1)
    return Trade(
        symbol="SP500", strategy="oops", exit_mode=mode, side="long",
        entry_ts=base + timedelta(days=day), entry=100.0, stop=99.0,
        tp1=None, tp2=None,
        exit_ts=base + timedelta(days=day, hours=1), exit=100.0 + pnl_R,
        exit_reason="tp1" if pnl_R > 0 else "stop",
        R=10.0, pnl_R=pnl_R, pnl_pct=pnl_R * 0.005, bars_in_trade=4,
    )


def test_report_includes_metrics_and_modes(tmp_path: Path):
    trades_by_mode = {
        "doc": [_trade(0, 1.0), _trade(1, -1.0), _trade(2, 2.0)],
        "atr": [_trade(0, 0.5, "atr"), _trade(1, 0.5, "atr")],
        "indicator": [_trade(0, 1.5, "indicator")],
    }
    report_path = tmp_path / "oops_backtest.md"
    write_backtest_report(
        report_path,
        strategy_name="oops",
        symbols=["SP500"],
        trades_by_mode=trades_by_mode,
        config={"period": "2018-01-01..2026-03-24", "risk_pct": 0.005},
    )
    content = report_path.read_text()
    assert "# OOPS backtest report" in content
    assert "doc" in content
    assert "atr" in content
    assert "indicator" in content
    assert "win_rate" in content
    assert "SP500" in content


def test_report_includes_wf_and_mc(tmp_path: Path):
    base = datetime(2024, 1, 1)
    trades = [_trade(i, 0.5 if i % 3 != 0 else -1.0) for i in range(60)]
    trades_by_mode = {"doc": trades}
    wf = walk_forward_split(trades, n_windows=5, is_pct=0.7)
    mc = monte_carlo_bootstrap(trades, n_simulations=1000, ruin_threshold_R=-15.0, seed=1)
    report_path = tmp_path / "oops_backtest.md"
    write_backtest_report(
        report_path, strategy_name="oops", symbols=["SP500"],
        trades_by_mode=trades_by_mode,
        config={"period": "2018..", "risk_pct": 0.005},
        walk_forward_windows=wf, monte_carlo_results=mc,
    )
    content = report_path.read_text()
    assert "Walk-forward" in content
    assert "Monte Carlo" in content
    assert "prob_ruin" in content
