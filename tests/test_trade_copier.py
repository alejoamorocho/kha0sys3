"""Unit tests for the pure copier logic (no MT5 needed)."""
from src.execution.trade_copier import TradeCopier

CFG = {
    "source": {"path": "x", "login": 1, "broker": "src"},
    "dest": {"path": "y", "login": 2, "broker": "dst"},
    "symbol_map": {"XAUUSD.f": "XAUUSD+"},
    "fixed_lot": 0.12,
}


def _copier():
    return TradeCopier(dict(CFG))


def test_reconcile_opens_new_source_positions():
    src = [{"ticket": 111}, {"ticket": 222}]
    state = {"111": 9001}  # 111 already copied
    to_open, to_close = TradeCopier.reconcile(src, state)
    assert [p["ticket"] for p in to_open] == [222]
    assert to_close == []


def test_reconcile_closes_vanished_source_positions():
    src = [{"ticket": 111}]
    state = {"111": 9001, "222": 9002}  # 222 no longer on source
    to_open, to_close = TradeCopier.reconcile(src, state)
    assert to_open == []
    assert to_close == [9002]


def test_reconcile_empty_source_closes_all_copies():
    src = []
    state = {"111": 9001, "222": 9002}
    to_open, to_close = TradeCopier.reconcile(src, state)
    assert to_open == []
    assert sorted(to_close) == [9001, 9002]


def test_reconcile_noop_when_in_sync():
    src = [{"ticket": 111}, {"ticket": 222}]
    state = {"111": 9001, "222": 9002}
    to_open, to_close = TradeCopier.reconcile(src, state)
    assert to_open == [] and to_close == []


def test_symbol_map_gold_only():
    c = _copier()
    assert c.map_symbol("XAUUSD.f") == "XAUUSD+"
    assert c.map_symbol("EURUSD.f") is None  # not mapped -> skipped


def test_fixed_lot_is_constant():
    c = _copier()
    assert c.fixed_lot == 0.12


def test_reopen_when_copy_vanished_but_source_open():
    # Source 111 still open but its copy is gone from the live dest map -> must
    # be queued to (re)open. This is the "copy flat while source open" guard.
    src = [{"ticket": 111}]
    dst_map = {}  # no live copy
    to_open, to_close = TradeCopier.reconcile(src, dst_map)
    assert [p["ticket"] for p in to_open] == [111]
    assert to_close == []


def test_backstop_disabled_returns_zero_without_mt5():
    c = _copier()  # config has no backstop_sl_usd
    assert c.backstop_sl_usd is None
    assert c._backstop_sl("XAUUSD+", True, 2000.0) == 0.0
