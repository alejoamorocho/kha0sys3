"""Runner FADE: executes FADE strategies from bot_config.json against M1/M15 data.

Produces a Markdown report comparing live vs backtest win rates per strategy,
plus aggregate metrics across all enabled FADE strategies with M1-overlap symbols.
"""

from datetime import datetime
from pathlib import Path

import polars as pl

from src.strategies_external.common.backtester import run_backtest
from src.strategies_external.common.metrics import evaluate
from src.strategies_external.data_loader import best_tracking_tf, load_csv
from src.strategies_external.exit_managers import DocExitManager
from src.strategies_external.strategies.fade_adapter import (
    FADEAdapter,
    load_fade_portfolio,
    _M1_AVAILABLE,
)


def run_fade_backtest(
    bot_config_path: str = "src/execution/bot_config.json",
    asset_config_path: str = "src/infrastructure/config/asset_config.json",
    data_dir: str = "data",
    output_path: "Path | str" = "reports/external/fade_m1_backtest.md",
    enabled_only: bool = True,
    risk_pct: float = 0.01,
) -> dict:
    """Run FADE backtest for all enabled strategies with M1/best tracking TF.

    Args:
        bot_config_path: Path to bot_config.json.
        asset_config_path: Path to asset_config.json.
        data_dir: Root data directory (contains M15/ CSVs and M1/ CSVs).
        output_path: Output Markdown report path.
        enabled_only: If True, only run enabled strategies.
        risk_pct: Fixed risk fraction per trade (bot live uses dynamic; 1% for backtest).

    Returns:
        dict with keys: 'per_strategy', 'aggregate', 'n_strategies'.
    """
    portfolio = load_fade_portfolio(
        bot_config_path, enabled_only=enabled_only, symbols_filter=_M1_AVAILABLE
    )
    print(
        f"Loaded {len(portfolio)} FADE strategies "
        f"(enabled={enabled_only}, M1-overlap symbols)"
    )
    if not portfolio:
        print("No strategies to run. Check bot_config.json or symbol filter.")
        return {"per_strategy": [], "aggregate": evaluate([]), "n_strategies": 0}

    adapter = FADEAdapter(asset_config_path)
    doc_mgr = DocExitManager(strategy="fade")

    # Load M15 + best tracking TF per symbol once (avoid redundant I/O)
    sym_data: dict[str, tuple[pl.DataFrame, pl.DataFrame, str]] = {}
    for sym in {s["sym_internal"] for s in portfolio}:
        try:
            df_m15 = load_csv(sym, "M15", data_dir=data_dir)
            tf_label, df_track = best_tracking_tf(sym, data_dir=data_dir)
            sym_data[sym] = (df_m15, df_track, tf_label)
            print(f"  Loaded {sym}: M15={df_m15.height} bars, tracking={tf_label} {df_track.height} bars")
        except FileNotFoundError as e:
            print(f"  SKIP {sym}: {e}")

    all_trades = []
    per_strategy_summary = []

    for s_cfg in portfolio:
        sym = s_cfg["sym_internal"]
        if sym not in sym_data:
            continue

        df_m15, df_track, tf_label = sym_data[sym]

        # Generate raw signals from M15 OR data
        sigs_raw = adapter.generate_signals_for_strategy(df_m15, sym, s_cfg)
        if not sigs_raw:
            print(
                f"  {sym} {s_cfg['edge']} {s_cfg['magic_time']}: "
                f"0 signals generated (ATR filter or no data)"
            )
            continue

        # Attach TP/SL levels via DocExitManager
        sigs = [doc_mgr.attach_levels(sig) for sig in sigs_raw]

        # Run backtest against fine tracking TF
        trades = run_backtest(sigs, df_track, exit_mode="doc", risk_pct=risk_pct)
        m = evaluate(trades)

        row = {
            "sym": s_cfg["sym"],
            "sym_internal": sym,
            "edge": s_cfg["edge"],
            "magic_time": s_cfg["magic_time"],
            "duration": s_cfg["duration"],
            "tp_mult": s_cfg["tp_mult"],
            "sl_mult": s_cfg["sl_mult"],
            "live_wr": s_cfg.get("win_rate"),
            "tracking_tf": tf_label,
            **m,
        }
        per_strategy_summary.append(row)
        all_trades.extend(trades)

        live_wr_str = f"{s_cfg.get('win_rate', 0):.3f}" if s_cfg.get("win_rate") else "n/a"
        print(
            f"  {sym} {s_cfg['edge']} {s_cfg['magic_time']}: "
            f"signals={len(sigs)} n={m['n_trades']} wr={m['win_rate']:.3f} "
            f"pf={m['profit_factor']:.3f} (live_wr={live_wr_str})"
        )

    # Aggregate metrics across all strategies
    total_m = evaluate(all_trades)
    print(
        f"\nAggregate: n={total_m['n_trades']} wr={total_m['win_rate']:.3f} "
        f"pf={total_m['profit_factor']:.3f} calmar={total_m['calmar']:.3f}"
    )

    # Write Markdown report
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# FADE M1 Backtest — bot live strategies",
        f"Generated: {datetime.utcnow().isoformat()}Z",
        "",
        "## Per-strategy comparison (live vs M1/M15 backtest)",
        "",
        "| sym | edge | magic | dur | tp | sl | tracking_tf | live_wr | bt_n | bt_wr | bt_pf | bt_dd_R | bt_calmar |",
        "|-----|------|-------|-----|-----|-----|------------|---------|------|-------|-------|---------|----------|",
    ]

    for r in per_strategy_summary:
        lwr = f"{r['live_wr']:.3f}" if r["live_wr"] is not None else "n/a"
        # Drift analysis: flag if |live_wr - bt_wr| > 10pp
        drift = ""
        if r["live_wr"] is not None and r["n_trades"] > 0:
            diff = abs(r["live_wr"] - r["win_rate"])
            if diff > 0.10:
                drift = f" DRIFT={diff:.2%}"
        lines.append(
            f"| {r['sym']} | {r['edge']} | {r['magic_time']} | {r['duration']} | "
            f"{r['tp_mult']} | {r['sl_mult']} | {r['tracking_tf']} | "
            f"{lwr} | {r['n_trades']} | "
            f"{r['win_rate']:.3f} | {r['profit_factor']:.3f} | "
            f"{r['max_dd_R']:.1f} | {r['calmar']:.3f} |{drift}"
        )

    lines.append("")
    lines.append("## Aggregate (all enabled FADE strategies)")
    lines.append(f"- n_strategies: {len(per_strategy_summary)}")
    lines.append(f"- n_trades: {total_m['n_trades']}")
    lines.append(f"- win_rate: {total_m['win_rate']:.3f}")
    lines.append(f"- profit_factor: {total_m['profit_factor']:.3f}")
    lines.append(f"- expectancy_R: {total_m['expectancy_R']:.3f}")
    lines.append(f"- max_dd_R: {total_m['max_dd_R']:.3f}")
    lines.append(f"- calmar: {total_m['calmar']:.3f}")
    lines.append(f"- total_R: {total_m['total_R']:.3f}")
    lines.append("")
    lines.append("## Drift analysis (|live_wr - bt_wr| > 10pp)")
    lines.append("")

    drift_rows = [
        r for r in per_strategy_summary
        if r["live_wr"] is not None and r["n_trades"] > 0
        and abs(r["live_wr"] - r["win_rate"]) > 0.10
    ]
    if drift_rows:
        lines.append("| sym | edge | live_wr | bt_wr | diff |")
        lines.append("|-----|------|---------|-------|------|")
        for r in drift_rows:
            diff = r["live_wr"] - r["win_rate"]
            lines.append(
                f"| {r['sym']} | {r['edge']} | {r['live_wr']:.3f} | "
                f"{r['win_rate']:.3f} | {diff:+.3f} |"
            )
    else:
        lines.append("No strategies with drift > 10pp detected.")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReport written to: {output_path}")

    return {
        "per_strategy": per_strategy_summary,
        "aggregate": total_m,
        "n_strategies": len(per_strategy_summary),
    }


if __name__ == "__main__":
    result = run_fade_backtest()
    print(f"\nDone. {result['n_strategies']} strategies processed.")
    if result["per_strategy"]:
        print("\nPer-strategy summary (first 10):")
        for r in result["per_strategy"][:10]:
            lwr = f"{r['live_wr']:.3f}" if r["live_wr"] else "n/a"
            print(
                f"  {r['sym']:10s} {r['edge']:10s} {r['magic_time']:6s} "
                f"n={r['n_trades']:4d} wr={r['win_rate']:.3f} "
                f"pf={r['profit_factor']:.3f} live_wr={lwr}"
            )
