"""Generador de reportes Markdown para backtests del módulo strategies_external."""

from datetime import datetime
from pathlib import Path

from src.strategies_external.common.metrics import evaluate
from src.strategies_external.common.trade import Trade


_FIELDS = ["n_trades", "win_rate", "profit_factor", "expectancy_R",
           "avg_win_R", "avg_loss_R", "max_dd_R", "sharpe", "sortino",
           "calmar", "total_R"]


def _fmt(v: float) -> str:
    if isinstance(v, int):
        return str(v)
    if v == float("inf"):
        return "∞"
    return f"{v:.3f}"


def write_backtest_report(
    path: Path,
    strategy_name: str,
    symbols: list[str],
    trades_by_mode: dict[str, list[Trade]],
    config: dict,
) -> None:
    """Escribe report Markdown con métricas por modo de exit y por activo."""
    lines: list[str] = []
    lines.append(f"# {strategy_name.upper()} backtest report")
    lines.append("")
    lines.append(f"**Generated:** {datetime.utcnow().isoformat()}Z")
    lines.append(f"**Symbols:** {', '.join(symbols)}")
    lines.append(f"**Period:** {config.get('period', 'n/a')}")
    lines.append(f"**Risk per trade:** {config.get('risk_pct', 0.005) * 100:.2f}%")
    lines.append("")

    # Tabla cruzada modo × métrica
    lines.append("## Comparativa modos de exit")
    lines.append("")
    header = "| metric | " + " | ".join(trades_by_mode.keys()) + " |"
    sep = "|--------|" + "|".join(["--------"] * len(trades_by_mode)) + "|"
    lines.append(header)
    lines.append(sep)
    metrics_by_mode = {m: evaluate(ts) for m, ts in trades_by_mode.items()}
    for f in _FIELDS:
        row = f"| {f} | " + " | ".join(_fmt(metrics_by_mode[m][f]) for m in trades_by_mode) + " |"
        lines.append(row)
    lines.append("")

    # Per-symbol breakdown del modo "doc" como referencia
    lines.append("## Breakdown por activo (modo doc)")
    lines.append("")
    lines.append("| symbol | n | wr | pf | exp_R | dd_R | calmar |")
    lines.append("|--------|---|-----|-----|-------|------|--------|")
    doc_trades = trades_by_mode.get("doc", [])
    for sym in symbols:
        sym_trades = [t for t in doc_trades if t.symbol == sym]
        m = evaluate(sym_trades)
        lines.append(
            f"| {sym} | {m['n_trades']} | {_fmt(m['win_rate'])} | "
            f"{_fmt(m['profit_factor'])} | {_fmt(m['expectancy_R'])} | "
            f"{_fmt(m['max_dd_R'])} | {_fmt(m['calmar'])} |"
        )
    lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
