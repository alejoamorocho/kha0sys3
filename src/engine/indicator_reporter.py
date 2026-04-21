"""Rendering: Markdown final report + JSON export compatible with bot_config format."""
from __future__ import annotations
import json
from pathlib import Path
import polars as pl


def render_final_report(final: pl.DataFrame) -> str:
    if len(final) == 0:
        return "# Indicator Discovery -- Final Report\n\nNo strategies passed strict gates.\n"
    lines = [
        "# Indicator Discovery -- Final Report",
        "",
        f"- Strategies passing all gates: **{len(final)}**",
        "- Gates: trades/year >= 100, WR >= 80%, PF >= 1.3, expectancy >= 0.1R, "
        "MaxDD <= 20R, WF OOS/IS >= 0.85, MC ruin < 1%, decay ratio >= 0.7",
        "",
        "## All passing strategies",
        "",
        "| Symbol | TF | Session | Signal | Filters | TP*ATR | SL*ATR "
        "| Trades | WR | PF | Exp (R) | MaxDD | WF | MC | Decay |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in final.iter_rows(named=True):
        flt = ",".join(r["filters"]) if r["filters"] else "-"
        lines.append(
            f"| {r['symbol']} | {r['tf']} | {r['session']} | {r['signal_type']} "
            f"| {flt} | {r['tp_atr_mult']} | {r['sl_atr_mult']} "
            f"| {r['n_trades']} | {r['wr']:.3f} | {r['pf']:.2f} "
            f"| {r['expectancy_r']:.3f} | {r['max_dd_r']:.1f} "
            f"| {r['wf_ratio']:.2f} | {r['mc_ruin']:.4f} | {r['decay_ratio']:.2f} |"
        )
    lines.append("")
    lines.append("## Coverage by symbol")
    cov = final.group_by("symbol").len().sort("len", descending=True)
    for r in cov.iter_rows(named=True):
        lines.append(f"- {r['symbol']}: {r['len']}")
    return "\n".join(lines) + "\n"


def export_strategies_json(final: pl.DataFrame, out_path: Path) -> None:
    if len(final) == 0:
        out_path.write_text("[]", encoding="utf-8")
        return
    items = []
    for r in final.iter_rows(named=True):
        items.append({
            "archetype": "INDICATOR",
            "symbol": r["symbol"], "tf": r["tf"], "session": r["session"],
            "signal_type": r["signal_type"], "filters": list(r["filters"]),
            "tp_atr_mult": float(r["tp_atr_mult"]),
            "sl_atr_mult": float(r["sl_atr_mult"]),
            "atr_period": 14,
            "metrics": {
                "wr": float(r["wr"]), "pf": float(r["pf"]),
                "expectancy_r": float(r["expectancy_r"]),
                "trades_per_year": float(r["trades_per_year"]),
                "wf_ratio": float(r["wf_ratio"]),
                "mc_ruin": float(r["mc_ruin"]),
                "decay_ratio": float(r["decay_ratio"]),
            },
        })
    out_path.write_text(json.dumps(items, indent=2), encoding="utf-8")
