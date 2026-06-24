"""Tests for the deal-based open-position reconstruction in the source keeper.

This is the logic that REPLACED positions_get() after we proved positions_get is
blind to TMFinancials managed-account positions (2 live trades stayed open 5-7
min with the keeper healthy and positions_get returned 0 the whole time, while
history_deals_get returned every trade). Reconstruction must be exact: a missed
open = a missed copy; a phantom open = a wrong copy with no SL/TP.

Deal data below mirrors the REAL deals pulled from login 50925289 (XAUUSD.f).
entry: 0=IN(open) 1=OUT(close) 2=INOUT 3=OUT_BY ; type: 0=BUY 1=SELL
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.copier_source_keeper import reconstruct_open


def deal(pos, entry, dtype, vol, sym="XAUUSD.f", t=0, ticket=0):
    return {"position_id": pos, "entry": entry, "type": dtype,
            "volume": vol, "symbol": sym, "time": t, "ticket": ticket}


# The 4 real round-trips (all CLOSED): IN then OUT, equal volume -> net 0.
BALANCE = deal(0, 0, 2, 0.0, sym="", t=1, ticket=108608676)
T1 = [deal(93832434, 0, 0, 0.018478, t=10, ticket=109111763),   # BUY open
      deal(93832434, 1, 1, 0.018478, t=11, ticket=109111891)]   # close
T2 = [deal(93873774, 0, 1, 0.018477, t=20, ticket=109854352),   # SELL open
      deal(93873774, 1, 0, 0.018477, t=21, ticket=109854481)]   # close
T3 = [deal(93909211, 0, 0, 0.018488, t=30, ticket=110525809),   # BUY open
      deal(93909211, 1, 1, 0.018488, t=31, ticket=110525886)]   # close
T4 = [deal(93935706, 0, 0, 0.01848, t=40, ticket=111092307),    # BUY open
      deal(93935706, 1, 1, 0.01848, t=41, ticket=111092435)]    # close


def test_all_closed_yields_no_open():
    """The exact real history (all 4 closed + a balance op) => zero open. A
    phantom 'open' here would make the copier open a ghost trade."""
    deals = [BALANCE] + T1 + T2 + T3 + T4
    assert reconstruct_open(deals) == []


def test_balance_op_is_ignored():
    assert reconstruct_open([BALANCE]) == []


def test_single_open_buy_detected():
    """Trade #3 with only its IN deal (manager just opened) => one open BUY."""
    deals = [BALANCE] + T1 + T2 + [T3[0]]      # T3 open, not yet closed
    out = reconstruct_open(deals)
    assert len(out) == 1
    p = out[0]
    assert p["ticket"] == 93909211
    assert p["type"] == 0                        # BUY/long
    assert p["symbol"] == "XAUUSD.f"
    assert abs(p["volume"] - 0.018488) < 1e-9
    assert p["sl"] == 0.0 and p["tp"] == 0.0     # TMF has no SL/TP


def test_single_open_sell_detected():
    """An open SELL must carry type=1 so the copy goes short, not long."""
    deals = [deal(93873774, 0, 1, 0.018477, t=20)]
    out = reconstruct_open(deals)
    assert len(out) == 1 and out[0]["type"] == 1


def test_partial_close_stays_open_with_residual_volume():
    deals = [deal(555, 0, 0, 0.10, t=1), deal(555, 1, 1, 0.04, t=2)]
    out = reconstruct_open(deals)
    assert len(out) == 1
    assert abs(out[0]["volume"] - 0.06) < 1e-9


def test_close_by_opposite_counts_as_closed():
    deals = [deal(777, 0, 0, 0.05, t=1), deal(777, 3, 1, 0.05, t=2)]  # OUT_BY
    assert reconstruct_open(deals) == []


def test_non_gold_is_filtered():
    deals = [deal(888, 0, 0, 0.10, sym="EURUSD", t=1)]
    assert reconstruct_open(deals, gold_only=True) == []
    assert len(reconstruct_open(deals, gold_only=False)) == 1


def test_multiple_simultaneous_opens():
    deals = [BALANCE] + T1 + [T3[0]] + [deal(93873774, 0, 1, 0.018477, t=20)]
    out = reconstruct_open(deals)
    tickets = sorted(p["ticket"] for p in out)
    assert tickets == [93873774, 93909211]
