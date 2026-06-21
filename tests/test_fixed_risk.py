"""Fixed-USD risk sizing: when risk_fixed_usd is set, the lot size must risk
exactly that USD amount at SL hit, independent of account balance / WR tier."""
from src.execution.risk_manager import DynamicRiskAllocator, BalanceTieredRiskAllocator


def _loss_per_lot(entry, sl, tick_size, tick_value):
    return (abs(entry - sl) / tick_size) * tick_value


def test_dynamic_fixed_usd_risks_exactly_target():
    a = DynamicRiskAllocator(risk_fixed_usd=100.0)
    lots = a.calculate_lots(
        account_balance=380_000, entry_price=2000.0, sl_price=1995.0,
        tick_value=1.0, tick_size=0.01, volume_step=0.01, win_rate=0.9,
    )
    lpl = _loss_per_lot(2000.0, 1995.0, 0.01, 1.0)  # 500 per lot
    assert abs(lots * lpl - 100.0) <= lpl * 0.01 + 1e-6


def test_dynamic_fixed_usd_independent_of_balance():
    a = DynamicRiskAllocator(risk_fixed_usd=100.0)
    kw = dict(entry_price=2000.0, sl_price=1995.0, tick_value=1.0,
              tick_size=0.01, volume_step=0.01, win_rate=0.9)
    assert a.calculate_lots(account_balance=380_000, **kw) == \
           a.calculate_lots(account_balance=2_000_000, **kw)


def test_tiered_fixed_usd_fx():
    a = BalanceTieredRiskAllocator(
        tiers=[{"max_balance": None, "min_risk": 0.005, "max_risk": 0.005}],
        risk_fixed_usd=100.0,
    )
    lots = a.calculate_lots(
        account_balance=380_000, entry_price=1.30, sl_price=1.2990,
        tick_value=1.0, tick_size=0.00001, volume_step=0.01, win_rate=0.9,
    )
    lpl = _loss_per_lot(1.30, 1.2990, 0.00001, 1.0)  # 100 per lot -> ~1 lot
    assert abs(lots * lpl - 100.0) <= lpl * 0.01 + 1e-6


def test_no_fixed_still_uses_balance_pct():
    a = DynamicRiskAllocator(min_risk=0.001, max_risk=0.001,
                             risk_tiers=[(None, 0.001, 0.001)])
    lots = a.calculate_lots(
        account_balance=100_000, entry_price=2000.0, sl_price=1995.0,
        tick_value=1.0, tick_size=0.01, volume_step=0.01, win_rate=0.5,
    )
    lpl = _loss_per_lot(2000.0, 1995.0, 0.01, 1.0)  # 500; risk=100 -> 0.2 lots
    assert abs(lots * lpl - 100.0) <= lpl * 0.01 + 1e-6
