"""Runner COT-1: backtest con doc + indicator + ATR sweep.

Downloads (and caches) Disaggregated COT data from cftc.gov per symbol.
ATR grid limited to 3 combos (COT-1 is slow due to COT data overhead).
Symbols with missing COT data are gracefully skipped.
"""

from pathlib import Path

import polars as pl

from src.strategies_external.common.backtester import run_backtest
from src.strategies_external.common.metrics import evaluate
from src.strategies_external.common.monte_carlo import monte_carlo_bootstrap
from src.strategies_external.common.trade import Trade
from src.strategies_external.common.walk_forward import walk_forward_split
from src.strategies_external.data_loader import (
    aggregate_to_daily, best_tracking_tf, load_csv,
)
from src.strategies_external.data_sources.cot_downloader import (
    cot_index, download_cot,
)
from src.strategies_external.data_sources.seasonality import seasonal_mean_return
from src.strategies_external.exit_managers import (
    ATRExitManager, DocExitManager, IndicatorExitManager,
)
from src.strategies_external.reporting.markdown import write_backtest_report
from src.strategies_external.strategies.cot1 import COT1Strategy


_SYMBOL_TO_COT = {
    "XAUUSD": "GOLD",
    "XAGUSD": "SILVER",
    "WTI": "CRUDE OIL, LIGHT SWEET",
    "BRENT": "BRENT CRUDE",
    "NATGAS": "NATURAL GAS",
    "SP500": "S&P 500",
    "NASDAQ100": "NASDAQ-100",
}


def _trades_to_parquet(trades: list[Trade], path: Path) -> None:
    if not trades:
        path.touch()
        return
    df = pl.DataFrame(
        [{
            "symbol": t.symbol, "strategy": t.strategy, "exit_mode": t.exit_mode,
            "side": t.side, "entry_ts": t.entry_ts, "entry": t.entry,
            "stop": t.stop, "tp1": t.tp1, "tp2": t.tp2,
            "exit_ts": t.exit_ts, "exit": t.exit, "exit_reason": t.exit_reason,
            "R": t.R, "pnl_R": t.pnl_R, "pnl_pct": t.pnl_pct,
            "bars_in_trade": t.bars_in_trade,
        } for t in trades],
        schema={"symbol": pl.Utf8, "strategy": pl.Utf8, "exit_mode": pl.Utf8,
                "side": pl.Utf8, "entry_ts": pl.Datetime, "entry": pl.Float64,
                "stop": pl.Float64, "tp1": pl.Float64, "tp2": pl.Float64,
                "exit_ts": pl.Datetime, "exit": pl.Float64,
                "exit_reason": pl.Utf8, "R": pl.Float64, "pnl_R": pl.Float64,
                "pnl_pct": pl.Float64, "bars_in_trade": pl.Int64},
    )
    df.write_parquet(path)


def run_cot1_backtest(
    symbols: list[str],
    data_dir: str = "data",
    output_path: Path | str = "reports/external/cot1_backtest.md",
    cot_dir: str = "data/cot",
    years: range = range(2018, 2026),
    atr_grid: list[tuple[float, float, float]] | None = None,
) -> dict[str, dict]:
    if atr_grid is None:
        atr_grid = [(1.0, 1.5, 3.0), (1.5, 2.0, 4.0), (2.0, 2.5, 4.0)]

    output_path = Path(output_path)

    # Per symbol: ensure COT data, build cot_index series
    per_symbol_cot: dict[str, pl.DataFrame] = {}
    for sym in symbols:
        keyword = _SYMBOL_TO_COT.get(sym)
        if keyword is None:
            print(f"  No COT mapping for {sym}, skipping")
            continue
        safe = keyword.lower().replace(" ", "_").replace(",", "")
        all_cot_dfs = []
        for year in years:
            path = Path(cot_dir) / f"{safe}_{year}.parquet"
            if not path.exists():
                try:
                    download_cot(year, keyword, output_dir=cot_dir)
                except Exception as e:
                    print(f"  COT download failed for {sym} {year}: {e}")
                    continue
            if path.exists():
                all_cot_dfs.append(pl.read_parquet(path))
        if not all_cot_dfs:
            print(f"  no COT data for {sym}, skipping")
            continue
        cot_df = pl.concat(all_cot_dfs).sort("date")
        cot_df = cot_df.with_columns(
            cot_index(cot_df["net"], window=26).alias("cot_index")
        )
        # Convert date column to datetime for compatibility with strategy code
        cot_df = cot_df.with_columns(pl.col("date").cast(pl.Datetime))
        per_symbol_cot[sym] = cot_df.select(["date", "cot_index"])

    strategy = COT1Strategy()
    doc_mgr = DocExitManager(strategy="cot1")
    ind_mgr = IndicatorExitManager(strategy="cot1")

    per_symbol: dict[str, tuple[list, pl.DataFrame]] = {}
    for sym in symbols:
        if sym not in per_symbol_cot:
            continue
        df_h1 = load_csv(sym, "H1", data_dir=data_dir)
        df_daily = aggregate_to_daily(df_h1)
        _, df_track = best_tracking_tf(sym, data_dir=data_dir)
        # build seasonality from daily data
        seasonality = seasonal_mean_return(df_daily.select(["time", "close"]), window_days=5)
        sigs = strategy.generate_signals(
            df_daily, symbol=sym,
            cot_index_series=per_symbol_cot[sym],
            seasonality=seasonality,
        )
        per_symbol[sym] = (sigs, df_track)

    trades_by_mode: dict[str, list[Trade]] = {"doc": [], "atr": [], "indicator": []}

    for sym, (sigs, df_track) in per_symbol.items():
        doc_signals = [doc_mgr.attach_levels(s) for s in sigs]
        trades_by_mode["doc"].extend(run_backtest(doc_signals, df_track, exit_mode="doc"))
        trades_by_mode["indicator"].extend(
            run_backtest([ind_mgr.attach_levels(s) for s in sigs], df_track, exit_mode="indicator")
        )

    # ATR sweep
    atr_grid_results = []
    best_atr_trades: list[Trade] = []
    best_atr_calmar = -float("inf")
    for sl, tp1, tp2 in atr_grid:
        cand_trades: list[Trade] = []
        atr_mgr = ATRExitManager(sl_mult=sl, tp1_mult=tp1, tp2_mult=tp2)
        for sym, (sigs, df_track) in per_symbol.items():
            cand_trades.extend(
                run_backtest([atr_mgr.attach_levels(s) for s in sigs],
                             df_track, exit_mode="atr")
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

    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_backtest_report(
        output_path,
        strategy_name="cot1",
        symbols=symbols,
        trades_by_mode=trades_by_mode,
        config={"period": "2018-01-01..today", "risk_pct": 0.005,
                "atr_grid": atr_grid,
                "note": "COT data from cftc.gov; symbols without COT skipped gracefully"},
        walk_forward_windows=wf,
        monte_carlo_results=mc,
        atr_grid_results=atr_grid_results,
    )

    all_trades = trades_by_mode["doc"] + trades_by_mode["atr"] + trades_by_mode["indicator"]
    _trades_to_parquet(all_trades, output_path.parent / "cot1_trades.parquet")

    summary = {m: evaluate(ts) for m, ts in trades_by_mode.items()}
    summary["atr_grid_results"] = atr_grid_results
    return summary


if __name__ == "__main__":
    summary = run_cot1_backtest(
        symbols=["XAUUSD", "XAGUSD", "WTI", "BRENT", "NATGAS"],
        data_dir="data",
        output_path="reports/external/cot1_backtest.md",
    )
    print("COT-1 backtest done.")
    for mode in ("doc", "atr", "indicator"):
        m = summary[mode]
        print(f"  [{mode}] n={m['n_trades']} wr={m['win_rate']:.3f} "
              f"pf={m['profit_factor']:.3f} dd_R={m['max_dd_R']:.3f} "
              f"calmar={m['calmar']:.3f}")
    if summary.get("atr_grid_results"):
        best = max(summary["atr_grid_results"], key=lambda r: r["calmar"])
        print(f"  best ATR: sl={best['sl']} tp1={best['tp1']} tp2={best['tp2']} "
              f"calmar={best['calmar']:.3f}")
