"""Walk-forward split: divide trades en N ventanas con split IS/OOS."""

from src.strategies_external.common.trade import Trade


def walk_forward_split(
    trades: list[Trade], n_windows: int = 5, is_pct: float = 0.7
) -> list[tuple[list[Trade], list[Trade]]]:
    """Particiona trades cronologicamente en ventanas no solapadas.

    Args:
        trades: lista de Trade.
        n_windows: numero de ventanas.
        is_pct: fraccion de cada ventana usada como in-sample (resto OOS).

    Returns:
        Lista de tuplas (in_sample, out_of_sample) para cada ventana.
    """
    if not (0.0 < is_pct < 1.0):
        raise ValueError("is_pct must be in (0, 1)")
    sorted_trades = sorted(trades, key=lambda t: t.entry_ts)
    n = len(sorted_trades)
    if n < n_windows * 2:
        raise ValueError(f"too few trades ({n}) for {n_windows} windows")

    window_size = n // n_windows
    is_size = int(window_size * is_pct)
    windows = []
    for w in range(n_windows):
        start = w * window_size
        end = start + window_size if w < n_windows - 1 else n
        chunk = sorted_trades[start:end]
        is_chunk = chunk[:is_size]
        oos_chunk = chunk[is_size:is_size + (window_size - is_size)]
        windows.append((is_chunk, oos_chunk))
    return windows
