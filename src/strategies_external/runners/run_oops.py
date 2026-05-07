"""Runner OOPS: ejecuta backtest con 3 modos de exit sobre los símbolos dados,
escribe reporte Markdown y trades en parquet.
"""

from pathlib import Path

import polars as pl

from src.strategies_external.common.backtester import run_backtest
from src.strategies_external.common.metrics import evaluate
from src.strategies_external.common.trade import Trade
from src.strategies_external.data_loader import (
    aggregate_to_daily, best_tracking_tf, load_csv,
)
from src.strategies_external.exit_managers import (
    ATRExitManager, DocExitManager, IndicatorExitManager,
)
from src.strategies_external.reporting.markdown import write_backtest_report
from src.strategies_external.strategies.oops import OOPSStrategy


def _trades_to_parquet(trades: list[Trade], path: Path) -> None:
    if not trades:
        path.touch()
        return
    # Use explicit schema to handle nullable tp2 column (None vs float)
    schema = {
        "symbol": pl.Utf8,
        "strategy": pl.Utf8,
        "exit_mode": pl.Utf8,
        "side": pl.Utf8,
        "entry_ts": pl.Datetime,
        "entry": pl.Float64,
        "stop": pl.Float64,
        "tp1": pl.Float64,
        "tp2": pl.Float64,
        "exit_ts": pl.Datetime,
        "exit": pl.Float64,
        "exit_reason": pl.Utf8,
        "R": pl.Float64,
        "pnl_R": pl.Float64,
        "pnl_pct": pl.Float64,
        "bars_in_trade": pl.Int64,
    }
    df = pl.DataFrame(
        [{
            "symbol": t.symbol, "strategy": t.strategy, "exit_mode": t.exit_mode,
            "side": t.side, "entry_ts": t.entry_ts, "entry": t.entry,
            "stop": t.stop, "tp1": t.tp1, "tp2": t.tp2,
            "exit_ts": t.exit_ts, "exit": t.exit, "exit_reason": t.exit_reason,
            "R": t.R, "pnl_R": t.pnl_R, "pnl_pct": t.pnl_pct,
            "bars_in_trade": t.bars_in_trade,
        } for t in trades],
        schema=schema,
    )
    df.write_parquet(path)


def run_oops_backtest(
    symbols: list[str],
    data_dir: str = "data",
    output_path: "Path | str" = "reports/external/oops_backtest.md",
    atr_grid: "list[tuple[float, float, float]] | None" = None,
) -> dict:
    """Corre OOPS sobre los símbolos dados con 3 modos de exit.

    Returns: dict mode -> metrics dict, plus 'atr_grid_results' list.
    """
    from src.strategies_external.common.walk_forward import walk_forward_split
    from src.strategies_external.common.monte_carlo import monte_carlo_bootstrap

    if atr_grid is None:
        atr_grid = [(1.5, 1.5, 3.0)]

    output_path = Path(output_path)
    strategy = OOPSStrategy()
    doc_mgr = DocExitManager(strategy="oops")
    ind_mgr = IndicatorExitManager(strategy="oops")

    # Pre-collect signals + tracking dataframes per symbol (avoid recomputing in sweep)
    per_symbol: dict[str, tuple[list, pl.DataFrame]] = {}
    for sym in symbols:
        df_h1 = load_csv(sym, "H1", data_dir=data_dir)
        df_daily = aggregate_to_daily(df_h1)
        _, df_track = best_tracking_tf(sym, data_dir=data_dir)
        signals_raw = strategy.generate_signals(df_daily, symbol=sym)
        per_symbol[sym] = (signals_raw, df_track)

    trades_by_mode: dict[str, list[Trade]] = {"doc": [], "atr": [], "indicator": []}

    # Plan 2.5: doc OOPS = 0.75% risk per trade
    risk_pct = 0.0075

    # Doc and indicator (single mode each)
    for sym, (sigs, df_track) in per_symbol.items():
        trades_by_mode["doc"].extend(
            run_backtest([doc_mgr.attach_levels(s) for s in sigs],
                         df_track, exit_mode="doc", risk_pct=risk_pct)
        )
        trades_by_mode["indicator"].extend(
            run_backtest([ind_mgr.attach_levels(s) for s in sigs],
                         df_track, exit_mode="indicator", risk_pct=risk_pct)
        )

    # ATR sweep: evaluate each grid combo across all symbols, pick best by calmar
    atr_grid_results = []
    best_atr_trades: list[Trade] = []
    best_atr_calmar = -float("inf")
    for sl, tp1, tp2 in atr_grid:
        cand_trades: list[Trade] = []
        atr_mgr = ATRExitManager(sl_mult=sl, tp1_mult=tp1, tp2_mult=tp2)
        for sym, (sigs, df_track) in per_symbol.items():
            cand_trades.extend(
                run_backtest([atr_mgr.attach_levels(s) for s in sigs],
                             df_track, exit_mode="atr", risk_pct=risk_pct)
            )
        m = evaluate(cand_trades)
        atr_grid_results.append({"sl": sl, "tp1": tp1, "tp2": tp2, **m})
        if m["calmar"] > best_atr_calmar:
            best_atr_calmar = m["calmar"]
            best_atr_trades = cand_trades

    trades_by_mode["atr"] = best_atr_trades

    doc_trades = trades_by_mode["doc"]
    try:
        wf = walk_forward_split(doc_trades, n_windows=5, is_pct=0.7)
    except ValueError:
        wf = None
    mc = monte_carlo_bootstrap(doc_trades, n_simulations=10_000,
                                ruin_threshold_R=-15.0, seed=42) if doc_trades else None

    write_backtest_report(
        output_path,
        strategy_name="oops",
        symbols=symbols,
        trades_by_mode=trades_by_mode,
        config={"period": "2018-01-01..today", "risk_pct": risk_pct,
                "atr_grid": atr_grid},
        walk_forward_windows=wf,
        monte_carlo_results=mc,
        atr_grid_results=atr_grid_results,
    )

    # Combina trades en un único parquet
    all_trades = trades_by_mode["doc"] + trades_by_mode["atr"] + trades_by_mode["indicator"]
    _trades_to_parquet(all_trades, output_path.parent / "oops_trades.parquet")

    summary = {m: evaluate(ts) for m, ts in trades_by_mode.items()}
    summary["atr_grid_results"] = atr_grid_results
    return summary


if __name__ == "__main__":
    grid = [(sl, tp1, tp2)
            for sl in (1.0, 1.5, 2.0, 2.5)
            for tp1 in (1.0, 1.5, 2.0)
            for tp2 in (2.0, 3.0, 4.0)
            if tp2 > tp1]
    summary = run_oops_backtest(
        symbols=["SP500", "NASDAQ100"],
        data_dir="data",
        output_path="reports/external/oops_backtest.md",
        atr_grid=grid,
    )
    print("OOPS backtest done.")
    for mode in ("doc", "atr", "indicator"):
        m = summary[mode]
        print(f"  [{mode}] n={m['n_trades']} wr={m['win_rate']:.3f} "
              f"pf={m['profit_factor']:.3f} dd_R={m['max_dd_R']:.3f} "
              f"calmar={m['calmar']:.3f}")
    best = max(summary["atr_grid_results"], key=lambda r: r["calmar"])
    print(f"  best ATR: sl={best['sl']} tp1={best['tp1']} tp2={best['tp2']} "
          f"calmar={best['calmar']:.3f}")
