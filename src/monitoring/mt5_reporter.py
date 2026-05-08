"""
MT5 Reporter — Kha0sys3
Extrae datos reales de MetaTrader 5: PnL, posiciones, historial de trades.
Todos los calculos provienen directamente del broker, sin estimaciones locales.
"""

import MetaTrader5 as mt5
from datetime import datetime, timedelta, timezone
from typing import Optional
from dataclasses import dataclass


@dataclass
class AccountSnapshot:
    balance: float
    equity: float
    margin: float
    margin_free: float
    margin_level: float
    profit: float  # PnL no realizado (floating)
    leverage: int
    currency: str
    server: str
    login: int


@dataclass
class PnLReport:
    period: str
    realized_pnl: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    best_trade: float
    worst_trade: float
    avg_profit: float
    avg_loss: float
    profit_factor: float
    total_commission: float
    total_swap: float


@dataclass
class PositionInfo:
    ticket: int
    symbol: str
    direction: str
    volume: float
    open_price: float
    current_price: float
    sl: float
    tp: float
    profit: float
    swap: float
    commission: float
    open_time: datetime
    magic: int
    comment: str


class MT5Reporter:
    """Extrae metricas reales directamente desde MetaTrader 5.

    All read methods accept an optional `magic` parameter. When set, results
    are filtered to that magic number, so a single Reporter can be scoped to
    a specific bot (e.g. magic=1338 for the MATH runner) without observing
    state from other bots that share the account.
    """

    def get_account(self) -> Optional[AccountSnapshot]:
        info = mt5.account_info()
        if info is None:
            return None
        return AccountSnapshot(
            balance=info.balance,
            equity=info.equity,
            margin=info.margin,
            margin_free=info.margin_free,
            margin_level=info.margin_level if info.margin_level else 0.0,
            profit=info.profit,
            leverage=info.leverage,
            currency=info.currency,
            server=info.server,
            login=info.login,
        )

    def get_open_positions(self, magic: Optional[int] = None) -> list[PositionInfo]:
        positions = mt5.positions_get()
        if positions is None:
            return []
        if magic is not None:
            positions = [p for p in positions if getattr(p, "magic", 0) == magic]
        result = []
        for p in positions:
            direction = "LONG" if p.type == mt5.POSITION_TYPE_BUY else "SHORT"
            result.append(PositionInfo(
                ticket=p.ticket,
                symbol=p.symbol,
                direction=direction,
                volume=p.volume,
                open_price=p.price_open,
                current_price=p.price_current,
                sl=p.sl,
                tp=p.tp,
                profit=p.profit,
                swap=p.swap,
                commission=p.commission if hasattr(p, 'commission') else 0.0,
                open_time=datetime.fromtimestamp(p.time, tz=timezone.utc),
                magic=p.magic,
                comment=p.comment,
            ))
        return result

    def get_deals_history(self, from_date: datetime, to_date: datetime,
                          magic: Optional[int] = None) -> list:
        deals = mt5.history_deals_get(from_date, to_date)
        if deals is None:
            return []
        if magic is not None:
            deals = [d for d in deals if getattr(d, "magic", 0) == magic]
        return list(deals)

    def calculate_pnl(self, period: str = "daily",
                      magic: Optional[int] = None) -> Optional[PnLReport]:
        """Calcula PnL realizado basado en historial real de MT5."""
        now = datetime.now(timezone.utc)

        if period == "daily":
            from_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == "weekly":
            days_since_monday = now.weekday()
            from_date = (now - timedelta(days=days_since_monday)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
        elif period == "monthly":
            from_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        elif period == "yearly":
            from_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            from_date = now - timedelta(days=1)

        deals = self.get_deals_history(from_date, now, magic=magic)

        # Filtrar solo deals de cierre (DEAL_ENTRY_OUT) que tienen PnL
        close_deals = [d for d in deals if d.entry == mt5.DEAL_ENTRY_OUT]

        if not close_deals:
            return PnLReport(
                period=period,
                realized_pnl=0.0,
                total_trades=0,
                winning_trades=0,
                losing_trades=0,
                win_rate=0.0,
                best_trade=0.0,
                worst_trade=0.0,
                avg_profit=0.0,
                avg_loss=0.0,
                profit_factor=0.0,
                total_commission=0.0,
                total_swap=0.0,
            )

        profits = [d.profit for d in close_deals]
        commissions = [d.commission for d in close_deals]
        swaps = [d.swap for d in close_deals]

        winning = [p for p in profits if p > 0]
        losing = [p for p in profits if p < 0]

        total_gross_profit = sum(winning) if winning else 0.0
        total_gross_loss = abs(sum(losing)) if losing else 0.0

        return PnLReport(
            period=period,
            realized_pnl=sum(profits) + sum(commissions) + sum(swaps),
            total_trades=len(close_deals),
            winning_trades=len(winning),
            losing_trades=len(losing),
            win_rate=(len(winning) / len(close_deals) * 100) if close_deals else 0.0,
            best_trade=max(profits) if profits else 0.0,
            worst_trade=min(profits) if profits else 0.0,
            avg_profit=(total_gross_profit / len(winning)) if winning else 0.0,
            avg_loss=(total_gross_loss / len(losing)) if losing else 0.0,
            profit_factor=(total_gross_profit / total_gross_loss) if total_gross_loss > 0 else float('inf'),
            total_commission=sum(commissions),
            total_swap=sum(swaps),
        )

    def get_pending_orders(self, magic: Optional[int] = None) -> list:
        orders = mt5.orders_get()
        if orders is None:
            return []
        if magic is not None:
            orders = [o for o in orders if getattr(o, "magic", 0) == magic]
        return list(orders)

    def is_mt5_connected(self) -> bool:
        info = mt5.terminal_info()
        if info is None:
            return False
        return info.connected

    def get_terminal_info(self) -> dict:
        info = mt5.terminal_info()
        if info is None:
            return {"connected": False}
        return {
            "connected": info.connected,
            "trade_allowed": info.trade_allowed,
            "community_connection": info.community_connection,
            "build": info.build,
            "path": info.path,
        }
