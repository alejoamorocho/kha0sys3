"""
Telegram Bot Interactivo — Kha0sys3
Bot con comandos completos para control total del sistema de trading.
Datos extraidos directamente de MetaTrader 5 — sin estimaciones.

Comandos disponibles:
    /start     - Menu principal
    /status    - Estado completo del sistema
    /balance   - Balance y equity en tiempo real
    /pnl       - PnL realizado del dia
    /weekly    - PnL semanal
    /monthly   - PnL mensual
    /positions - Posiciones abiertas
    /orders    - Ordenes pendientes
    /health    - Salud del VPS (CPU, RAM, Disco)
    /stop      - Detener el bot de trading
    /resume    - Reanudar el bot de trading
"""

import asyncio
import threading
import time
import os
import signal
from datetime import datetime, timezone
from typing import Optional, Callable
from pathlib import Path

from telegram import Update, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from src.monitoring.mt5_reporter import MT5Reporter, AccountSnapshot, PnLReport, PositionInfo
from src.monitoring.system_health import SystemHealthMonitor, SystemHealth


class TelegramCommandBot:
    """Bot de Telegram interactivo con control total del sistema de trading."""

    def __init__(self, config_path: str = "config/telegram.yaml",
                 stop_callback: Optional[Callable] = None,
                 resume_callback: Optional[Callable] = None):
        self._load_config(config_path)
        self.reporter = MT5Reporter()
        self.health_monitor = SystemHealthMonitor()
        self.stop_callback = stop_callback
        self.resume_callback = resume_callback
        self._bot_active = True
        self._start_time = time.time()
        self._app: Optional[Application] = None
        self._thread: Optional[threading.Thread] = None

    def _load_config(self, config_path: str):
        path = Path(config_path)
        if path.exists():
            import yaml
            with open(path, "r") as f:
                cfg = yaml.safe_load(f)
            self.token = cfg["token"]
            self.admin_chat_id = int(cfg["chat_id"])
            self.group_chat_id = str(cfg.get("group_chat_id", ""))
        else:
            self.token = "8268613194:AAF1Dt15QXwUGAA4M_A8xrDqNMoSiYbpoyk"
            self.admin_chat_id = 778542603
            self.group_chat_id = "-5170985767"

    def _is_admin(self, update: Update) -> bool:
        return update.effective_chat.id == self.admin_chat_id

    # ─── Formatters ───────────────────────────────────────────────

    def _fmt_account(self, acc: AccountSnapshot) -> str:
        pnl_emoji = "+" if acc.profit >= 0 else ""
        return (
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "       <b>CUENTA DE TRADING</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  Broker    │ Vantage International\n"
            f"  Cuenta    │ {acc.login}\n"
            f"  Servidor  │ {acc.server}\n"
            f"  Apal.     │ 1:{acc.leverage}\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  Balance   │ <b>${acc.balance:,.2f}</b>\n"
            f"  Equity    │ <b>${acc.equity:,.2f}</b>\n"
            f"  Flotante  │ {pnl_emoji}${acc.profit:,.2f}\n"
            f"  Margen    │ ${acc.margin:,.2f}\n"
            f"  M. Libre  │ ${acc.margin_free:,.2f}\n"
            f"  Nivel     │ {acc.margin_level:.1f}%\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  <i>{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC</i>"
        )

    def _fmt_pnl(self, report: PnLReport) -> str:
        period_names = {
            "daily": "HOY", "weekly": "SEMANAL",
            "monthly": "MENSUAL", "yearly": "ANUAL",
        }
        title = period_names.get(report.period, report.period.upper())
        pnl_emoji = "🟢" if report.realized_pnl >= 0 else "🔴"

        pf_str = f"{report.profit_factor:.2f}" if report.profit_factor != float('inf') else "∞"

        return (
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"   {pnl_emoji} <b>P&L {title}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  Realizado │ <b>${report.realized_pnl:+,.2f}</b>\n"
            f"  Trades    │ {report.total_trades}\n"
            f"  Ganados   │ {report.winning_trades}\n"
            f"  Perdidos  │ {report.losing_trades}\n"
            f"  Win Rate  │ {report.win_rate:.1f}%\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  Mejor     │ ${report.best_trade:+,.2f}\n"
            f"  Peor      │ ${report.worst_trade:+,.2f}\n"
            f"  Avg Win   │ ${report.avg_profit:,.2f}\n"
            f"  Avg Loss  │ -${report.avg_loss:,.2f}\n"
            f"  P. Factor │ {pf_str}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  Comision  │ ${report.total_commission:,.2f}\n"
            f"  Swap      │ ${report.total_swap:,.2f}\n"
            f"  Neto      │ <b>${report.realized_pnl:+,.2f}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  <i>{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC</i>"
        )

    def _fmt_position(self, pos: PositionInfo) -> str:
        direction_emoji = "🟢" if pos.direction == "LONG" else "🔴"
        pnl_emoji = "+" if pos.profit >= 0 else ""
        duration = datetime.now() - pos.open_time
        hours = duration.total_seconds() / 3600

        return (
            f"  {direction_emoji} <b>{pos.symbol}</b> │ {pos.direction}\n"
            f"     Vol: {pos.volume} │ Entry: {pos.open_price}\n"
            f"     SL: {pos.sl} │ TP: {pos.tp}\n"
            f"     P&L: <b>{pnl_emoji}${pos.profit:,.2f}</b> │ {hours:.1f}h\n"
        )

    def _fmt_health(self, health: SystemHealth) -> str:
        mt5_status = "🟢 Conectado" if health.mt5_connected else "🔴 Desconectado"
        trade_status = "🟢 Habilitado" if health.mt5_trade_allowed else "🔴 Deshabilitado"
        mt5_proc = "🟢 Corriendo" if health.mt5_running else "🔴 Detenido"

        cpu_bar = self._progress_bar(health.cpu_percent)
        ram_bar = self._progress_bar(health.ram_percent)
        disk_bar = self._progress_bar(health.disk_percent)

        return (
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "      <b>SALUD DEL SISTEMA</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  CPU       │ {cpu_bar} {health.cpu_percent:.1f}%\n"
            f"  RAM       │ {ram_bar} {health.ram_percent:.1f}%\n"
            f"            │ {health.ram_used_gb:.1f}/{health.ram_total_gb:.1f} GB\n"
            f"  Disco     │ {disk_bar} {health.disk_percent:.1f}%\n"
            f"            │ {health.disk_used_gb:.1f}/{health.disk_total_gb:.1f} GB\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  MT5 Proc  │ {mt5_proc}\n"
            f"  MT5 Conn  │ {mt5_status}\n"
            f"  Trading   │ {trade_status}\n"
            f"  Python    │ {health.python_processes} procesos\n"
            f"  Uptime    │ {health.uptime_hours:.1f} horas\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  <i>{health.timestamp.strftime('%Y-%m-%d %H:%M')} UTC</i>"
        )

    def _progress_bar(self, percent: float, width: int = 8) -> str:
        filled = int(width * percent / 100)
        empty = width - filled
        return "█" * filled + "░" * empty

    # ─── Command Handlers ─────────────────────────────────────────

    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self._is_admin(update):
            return

        bot_status = "🟢 ACTIVO" if self._bot_active else "🔴 DETENIDO"
        uptime = (time.time() - self._start_time) / 3600

        msg = (
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "    <b>KHA0SYS3 CONTROL PANEL</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  Estado    │ {bot_status}\n"
            f"  Uptime    │ {uptime:.1f}h\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "  <b>Comandos disponibles:</b>\n\n"
            "  /status    — Estado completo\n"
            "  /balance   — Balance y equity\n"
            "  /pnl       — P&L del dia\n"
            "  /weekly    — P&L semanal\n"
            "  /monthly   — P&L mensual\n"
            "  /positions — Posiciones abiertas\n"
            "  /orders    — Ordenes pendientes\n"
            "  /health    — Salud del VPS\n"
            "  /stop      — Detener trading\n"
            "  /resume    — Reanudar trading\n"
            "━━━━━━━━━━━━━━━━━━━━━━"
        )
        await update.message.reply_text(msg, parse_mode="HTML")

    async def cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self._is_admin(update):
            return

        acc = self.reporter.get_account()
        daily = self.reporter.calculate_pnl("daily")
        health = self.health_monitor.get_health()
        positions = self.reporter.get_open_positions()
        orders = self.reporter.get_pending_orders()
        alerts = self.health_monitor.get_critical_alerts()

        bot_status = "🟢 ACTIVO" if self._bot_active else "🔴 DETENIDO"
        uptime = (time.time() - self._start_time) / 3600

        balance_str = f"${acc.balance:,.2f}" if acc else "N/A"
        equity_str = f"${acc.equity:,.2f}" if acc else "N/A"
        floating_str = f"${acc.profit:+,.2f}" if acc else "N/A"
        daily_pnl = f"${daily.realized_pnl:+,.2f}" if daily else "N/A"

        mt5_conn = "🟢" if health.mt5_connected else "🔴"
        mt5_trade = "🟢" if health.mt5_trade_allowed else "🔴"

        msg = (
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "    <b>ESTADO GENERAL KHA0SYS3</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  Bot       │ {bot_status}\n"
            f"  Uptime    │ {uptime:.1f}h\n"
            f"  MT5       │ {mt5_conn} Conn │ {mt5_trade} Trade\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  Balance   │ <b>{balance_str}</b>\n"
            f"  Equity    │ {equity_str}\n"
            f"  Flotante  │ {floating_str}\n"
            f"  P&L Hoy   │ <b>{daily_pnl}</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  Posiciones│ {len(positions)} abiertas\n"
            f"  Ordenes   │ {len(orders)} pendientes\n"
            f"  CPU       │ {health.cpu_percent:.1f}%\n"
            f"  RAM       │ {health.ram_percent:.1f}%\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
        )

        if alerts:
            msg += "  <b>⚠️ ALERTAS:</b>\n"
            for alert in alerts:
                msg += f"  • {alert}\n"
            msg += "━━━━━━━━━━━━━━━━━━━━━━\n"

        msg += f"  <i>{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC</i>"
        await update.message.reply_text(msg, parse_mode="HTML")

    async def cmd_balance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self._is_admin(update):
            return
        acc = self.reporter.get_account()
        if not acc:
            await update.message.reply_text("❌ No se pudo obtener datos de la cuenta MT5.")
            return
        await update.message.reply_text(self._fmt_account(acc), parse_mode="HTML")

    async def cmd_pnl(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self._is_admin(update):
            return
        report = self.reporter.calculate_pnl("daily")
        if not report:
            await update.message.reply_text("❌ No se pudo calcular P&L.")
            return
        await update.message.reply_text(self._fmt_pnl(report), parse_mode="HTML")

    async def cmd_weekly(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self._is_admin(update):
            return
        report = self.reporter.calculate_pnl("weekly")
        if not report:
            await update.message.reply_text("❌ No se pudo calcular P&L semanal.")
            return
        await update.message.reply_text(self._fmt_pnl(report), parse_mode="HTML")

    async def cmd_monthly(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self._is_admin(update):
            return
        report = self.reporter.calculate_pnl("monthly")
        if not report:
            await update.message.reply_text("❌ No se pudo calcular P&L mensual.")
            return
        await update.message.reply_text(self._fmt_pnl(report), parse_mode="HTML")

    async def cmd_positions(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self._is_admin(update):
            return
        positions = self.reporter.get_open_positions()

        if not positions:
            msg = (
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "      <b>POSICIONES ABIERTAS</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "  Sin posiciones abiertas.\n"
                "━━━━━━━━━━━━━━━━━━━━━━"
            )
        else:
            total_pnl = sum(p.profit for p in positions)
            pnl_emoji = "🟢" if total_pnl >= 0 else "🔴"

            msg = (
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "      <b>POSICIONES ABIERTAS</b>\n"
                f"  {pnl_emoji} Flotante Total: <b>${total_pnl:+,.2f}</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
            )
            for pos in positions:
                msg += self._fmt_position(pos)
                msg += "──────────────────────\n"

        msg += f"  <i>{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC</i>"
        await update.message.reply_text(msg, parse_mode="HTML")

    async def cmd_orders(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self._is_admin(update):
            return
        orders = self.reporter.get_pending_orders()

        if not orders:
            msg = (
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "      <b>ORDENES PENDIENTES</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "  Sin ordenes pendientes.\n"
                "━━━━━━━━━━━━━━━━━━━━━━"
            )
        else:
            msg = (
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "      <b>ORDENES PENDIENTES</b>\n"
                f"  Total: {len(orders)}\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
            )
            for o in orders:
                order_type = "BUY_STOP" if o.type == 4 else "SELL_STOP" if o.type == 5 else f"Type {o.type}"
                msg += (
                    f"  #{o.ticket} │ {o.symbol}\n"
                    f"     {order_type} │ Vol: {o.volume_current}\n"
                    f"     Price: {o.price_open} │ SL: {o.sl} │ TP: {o.tp}\n"
                    "──────────────────────\n"
                )

        msg += f"  <i>{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC</i>"
        await update.message.reply_text(msg, parse_mode="HTML")

    async def cmd_health(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self._is_admin(update):
            return
        health = self.health_monitor.get_health()
        await update.message.reply_text(self._fmt_health(health), parse_mode="HTML")

    async def cmd_stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self._is_admin(update):
            return

        if not self._bot_active:
            await update.message.reply_text(
                "⚠️ El bot ya esta detenido.",
                parse_mode="HTML",
            )
            return

        self._bot_active = False

        msg = (
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "    🛑 <b>BOT DETENIDO</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "  El bot de trading ha sido\n"
            "  detenido por comando admin.\n\n"
            "  No se colocaran nuevas ordenes.\n"
            "  Las posiciones abiertas siguen\n"
            "  activas en el broker.\n\n"
            "  Usa /resume para reanudar.\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  <i>{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC</i>"
        )
        await update.message.reply_text(msg, parse_mode="HTML")

        if self.stop_callback:
            self.stop_callback()

    async def cmd_resume(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self._is_admin(update):
            return

        if self._bot_active:
            await update.message.reply_text(
                "✅ El bot ya esta activo.",
                parse_mode="HTML",
            )
            return

        self._bot_active = True

        msg = (
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "    🟢 <b>BOT REANUDADO</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "  El bot de trading ha sido\n"
            "  reanudado por comando admin.\n\n"
            "  Se reanudan operaciones normales.\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  <i>{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC</i>"
        )
        await update.message.reply_text(msg, parse_mode="HTML")

        if self.resume_callback:
            self.resume_callback()

    # ─── Broadcast (para notificaciones push) ─────────────────────

    async def _send_message(self, text: str, chat_id: Optional[int] = None):
        if self._app is None:
            return
        target = chat_id or self.admin_chat_id
        try:
            await self._app.bot.send_message(
                chat_id=target,
                text=text,
                parse_mode="HTML",
                disable_web_page_preview=True,
            )
        except Exception as e:
            print(f"Telegram send error: {e}")

    async def broadcast(self, text: str):
        """Envia mensaje a admin + grupo."""
        await self._send_message(text, self.admin_chat_id)
        if self.group_chat_id:
            await self._send_message(text, int(self.group_chat_id))

    def send_sync(self, text: str):
        """Envia mensaje de forma sincrona (para usar desde threads no-async)."""
        if self._app is None:
            return
        loop = self._app._loop
        if loop and loop.is_running():
            asyncio.run_coroutine_threadsafe(self.broadcast(text), loop)

    # ─── Notificaciones Push Profesionales ────────────────────────

    def notify_bot_started(self, portfolio: list[dict], risk_percent: float = 0.03):
        symbols = ", ".join(s["sym"] for s in portfolio)
        risk_display = f"{risk_percent * 100:.1f}%"
        msg = (
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "   🚀 <b>KHA0SYS3 INICIADO</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  Portfolio │ {symbols}\n"
            f"  Riesgo    │ {risk_display} por trade\n"
            f"  Estrategia│ ORB (Opening Range)\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  <i>{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC</i>"
        )
        self.send_sync(msg)

    def notify_bot_stopped(self, reason: str = "Manual"):
        msg = (
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "   🛑 <b>KHA0SYS3 DETENIDO</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  Razon     │ {reason}\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  <i>{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC</i>"
        )
        self.send_sync(msg)

    def notify_orb_detected(self, symbol: str, range_high: float,
                            range_low: float, range_width: float):
        msg = (
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"   📊 <b>ORB DETECTADO: {symbol}</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  High      │ {range_high:.5f}\n"
            f"  Low       │ {range_low:.5f}\n"
            f"  Width     │ {range_width:.5f}\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  <i>{datetime.now(timezone.utc).strftime('%H:%M')} UTC</i>"
        )
        self.send_sync(msg)

    def notify_order_placed(self, symbol: str, direction: str,
                            entry: float, sl: float, tp: float, lots: float):
        emoji = "🟢" if "BUY" in direction else "🔴"
        risk_pips = abs(entry - sl)
        reward_pips = abs(tp - entry)
        rr = reward_pips / risk_pips if risk_pips > 0 else 0

        msg = (
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"   {emoji} <b>ORDEN: {symbol}</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  Tipo      │ {direction}\n"
            f"  Entry     │ {entry:.5f}\n"
            f"  Stop Loss │ {sl:.5f}\n"
            f"  Take Prof │ {tp:.5f}\n"
            f"  Volumen   │ {lots:.2f} lots\n"
            f"  R:R       │ 1:{rr:.1f}\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  <i>{datetime.now(timezone.utc).strftime('%H:%M')} UTC</i>"
        )
        self.send_sync(msg)

    def notify_order_rejected(self, symbol: str, reason: str):
        msg = (
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"   ⚠️ <b>RECHAZADA: {symbol}</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  Razon     │ {reason}\n"
            "━━━━━━━━━━━━━━━━━━━━━━"
        )
        self.send_sync(msg)

    def notify_spread_alert(self, symbol: str, current: float, average: float):
        msg = (
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"   ⚠️ <b>SPREAD ALTO: {symbol}</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  Actual    │ {current:.1f}\n"
            f"  Promedio  │ {average:.1f}\n"
            f"  Ratio     │ {current/average:.2f}x\n"
            "━━━━━━━━━━━━━━━━━━━━━━"
        )
        self.send_sync(msg)

    def notify_exposure_blocked(self, symbol: str):
        msg = (
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"   🛡️ <b>BLOQUEADO: {symbol}</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "  Posicion u ordenes existentes.\n"
            "  Nueva entrada bloqueada.\n"
            "━━━━━━━━━━━━━━━━━━━━━━"
        )
        self.send_sync(msg)

    def notify_error(self, error_msg: str, context: str = "General"):
        msg = (
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"   ❌ <b>ERROR: {context}</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  {error_msg[:400]}\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  <i>{datetime.now(timezone.utc).strftime('%H:%M')} UTC</i>"
        )
        self.send_sync(msg)

    def notify_heartbeat(self, uptime_hours: float, trades_today: int):
        acc = self.reporter.get_account()
        daily = self.reporter.calculate_pnl("daily")
        health = self.health_monitor.get_health()

        balance_str = f"${acc.balance:,.2f}" if acc else "N/A"
        equity_str = f"${acc.equity:,.2f}" if acc else "N/A"
        daily_pnl = f"${daily.realized_pnl:+,.2f}" if daily else "N/A"
        mt5_status = "🟢" if health.mt5_connected else "🔴"

        msg = (
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "   💓 <b>HEARTBEAT</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  Uptime    │ {uptime_hours:.1f}h\n"
            f"  Trades    │ {trades_today} hoy\n"
            f"  Balance   │ {balance_str}\n"
            f"  Equity    │ {equity_str}\n"
            f"  P&L Hoy   │ {daily_pnl}\n"
            f"  MT5       │ {mt5_status}\n"
            f"  CPU       │ {health.cpu_percent:.1f}%\n"
            f"  RAM       │ {health.ram_percent:.1f}%\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  <i>{datetime.now(timezone.utc).strftime('%H:%M')} UTC</i>"
        )
        self.send_sync(msg)

    def notify_orphan_cleanup(self, symbol: str, count: int):
        msg = (
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"   🧹 <b>LIMPIEZA: {symbol}</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  Ordenes canceladas: {count}\n"
            "━━━━━━━━━━━━━━━━━━━━━━"
        )
        self.send_sync(msg)

    def notify_system_alert(self, alerts: list[str]):
        alert_text = "\n".join(f"  • {a}" for a in alerts)
        msg = (
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "   🚨 <b>ALERTA DEL SISTEMA</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"{alert_text}\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"  <i>{datetime.now(timezone.utc).strftime('%H:%M')} UTC</i>"
        )
        self.send_sync(msg)

    # ─── Bot Runner ───────────────────────────────────────────────

    @property
    def is_active(self) -> bool:
        return self._bot_active

    def _build_app(self) -> Application:
        app = Application.builder().token(self.token).build()

        app.add_handler(CommandHandler("start", self.cmd_start))
        app.add_handler(CommandHandler("status", self.cmd_status))
        app.add_handler(CommandHandler("balance", self.cmd_balance))
        app.add_handler(CommandHandler("pnl", self.cmd_pnl))
        app.add_handler(CommandHandler("weekly", self.cmd_weekly))
        app.add_handler(CommandHandler("monthly", self.cmd_monthly))
        app.add_handler(CommandHandler("positions", self.cmd_positions))
        app.add_handler(CommandHandler("orders", self.cmd_orders))
        app.add_handler(CommandHandler("health", self.cmd_health))
        app.add_handler(CommandHandler("stop", self.cmd_stop))
        app.add_handler(CommandHandler("resume", self.cmd_resume))

        return app

    async def _set_commands(self):
        commands = [
            BotCommand("start", "Panel de control"),
            BotCommand("status", "Estado completo"),
            BotCommand("balance", "Balance y equity"),
            BotCommand("pnl", "P&L del dia"),
            BotCommand("weekly", "P&L semanal"),
            BotCommand("monthly", "P&L mensual"),
            BotCommand("positions", "Posiciones abiertas"),
            BotCommand("orders", "Ordenes pendientes"),
            BotCommand("health", "Salud del VPS"),
            BotCommand("stop", "Detener trading"),
            BotCommand("resume", "Reanudar trading"),
        ]
        await self._app.bot.set_my_commands(commands)

    def start_polling(self):
        """Inicia el bot en un thread separado para no bloquear el LiveTrader."""
        self._app = self._build_app()

        def _run():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            self._app._loop = loop

            loop.run_until_complete(self._app.initialize())
            loop.run_until_complete(self._app.start())
            loop.run_until_complete(self._set_commands())
            loop.run_until_complete(
                self._app.updater.start_polling(drop_pending_updates=True)
            )
            loop.run_forever()

        self._thread = threading.Thread(target=_run, daemon=True)
        self._thread.start()

    def stop_polling(self):
        if self._app and self._app._loop:
            async def _stop():
                await self._app.updater.stop()
                await self._app.stop()
                await self._app.shutdown()
            future = asyncio.run_coroutine_threadsafe(
                _stop(), self._app._loop
            )
            future.result(timeout=10)
