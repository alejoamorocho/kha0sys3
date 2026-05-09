"""
Telegram Notifier — Kha0sys3
Modulo de notificaciones Telegram siguiendo la logica ORB del bot de trading.
Envia alertas de trades, estado de cuenta, y metricas de riesgo.
"""

import requests
import json
from datetime import datetime, timezone
from typing import Optional
from pathlib import Path


class TelegramNotifier:
    """Notificador Telegram para el bot de trading ORB Kha0sys3."""

    API_URL = "https://api.telegram.org/bot{token}/sendMessage"

    def __init__(self, config_path: str = "config/telegram.yaml", risk_percent: float = 0.03):
        self._load_config(config_path)
        self._risk_display = f"{risk_percent * 100:.1f}%"

    def _load_config(self, config_path: str):
        """Carga credenciales desde .env / env vars o desde telegram.yaml.

        Orden de precedencia:
          1. variables de entorno (TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_GROUP_CHAT_ID)
          2. config/telegram.yaml (legacy)
        Si ninguno define el token, levanta RuntimeError.
        """
        import os
        from src.domain.env_loader import load_env
        load_env()

        token = os.environ.get("TELEGRAM_TOKEN")
        chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        group_chat_id = os.environ.get("TELEGRAM_GROUP_CHAT_ID", "")

        if not token or not chat_id:
            path = Path(config_path)
            if path.exists():
                import yaml
                with open(path, "r", encoding="utf-8") as f:
                    cfg = yaml.safe_load(f) or {}
                token = token or cfg.get("token")
                chat_id = chat_id or (str(cfg["chat_id"]) if cfg.get("chat_id") else None)
                group_chat_id = group_chat_id or str(cfg.get("group_chat_id", ""))

        if not token or not chat_id:
            raise RuntimeError(
                "TelegramNotifier: faltan credenciales. Define TELEGRAM_TOKEN y "
                "TELEGRAM_CHAT_ID en .env o crea config/telegram.yaml."
            )

        self.token = token
        self.chat_id = str(chat_id)
        self.group_chat_id = str(group_chat_id)

    def _send(self, text: str, chat_id: Optional[str] = None) -> bool:
        """Envia mensaje a un chat especifico."""
        target = chat_id or self.chat_id
        url = self.API_URL.format(token=self.token)
        payload = {
            "chat_id": target,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }
        try:
            resp = requests.post(url, json=payload, timeout=10)
            return resp.status_code == 200
        except requests.RequestException as e:
            print(f"Telegram send error: {e}")
            return False

    def _broadcast(self, text: str) -> bool:
        """Envia a chat personal + grupo (mirror)."""
        personal_ok = self._send(text, self.chat_id)
        group_ok = True
        if self.group_chat_id:
            group_ok = self._send(text, self.group_chat_id)
        return personal_ok and group_ok

    def notify_bot_started(self, portfolio: list[dict]):
        """Notifica que el bot ha iniciado con el portfolio activo."""
        lines = []
        for s in portfolio:
            edge = s.get("edge", "ORB")
            durs = s.get("durations", [15])
            durs_str = "/".join(str(d) for d in durs)
            lines.append(f"  {s['sym']} │ {edge} │ {s.get('magic_time','')} │ {durs_str}m")
        portfolio_text = "\n".join(lines)
        msg = (
            "<b>🚀 Kha0sys3 Bot Iniciado</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<code>{portfolio_text}</code>\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"<code>Riesgo/Trade: {self._risk_display}</code>\n"
            f"<code>Hora UTC: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')}</code>"
        )
        self._broadcast(msg)

    def notify_bot_stopped(self, reason: str = "Manual"):
        """Notifica que el bot se ha detenido."""
        msg = (
            "<b>🛑 Kha0sys3 Bot Detenido</b>\n"
            f"<code>Razon: {reason}</code>\n"
            f"<code>Hora UTC: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')}</code>"
        )
        self._broadcast(msg)

    def notify_orb_detected(self, symbol: str, range_high: float,
                            range_low: float, range_width: float):
        """Notifica deteccion de Opening Range."""
        msg = (
            f"<b>📊 ORB Detectado: {symbol}</b>\n"
            f"<code>High : {range_high:.5f}</code>\n"
            f"<code>Low  : {range_low:.5f}</code>\n"
            f"<code>Width: {range_width:.5f}</code>\n"
            f"<code>Hora : {datetime.now(timezone.utc).strftime('%H:%M')} UTC</code>"
        )
        self._broadcast(msg)

    def notify_order_placed(self, symbol: str, direction: str,
                            entry: float, sl: float, tp: float,
                            lots: float, edge: str = ""):
        """Notifica colocacion de orden stop."""
        emoji = "🟢" if direction == "BUY_STOP" else "🔴"
        edge_label = f"\n<code>Edge  : {edge}</code>" if edge else ""
        msg = (
            f"<b>{emoji} Orden Colocada: {symbol}</b>\n"
            f"<code>Tipo  : {direction}</code>{edge_label}\n"
            f"<code>Entry : {entry:.5f}</code>\n"
            f"<code>SL    : {sl:.5f}</code>\n"
            f"<code>TP    : {tp:.5f}</code>\n"
            f"<code>Lots  : {lots:.2f}</code>"
        )
        self._broadcast(msg)

    def notify_order_rejected(self, symbol: str, reason: str):
        """Notifica que una orden fue rechazada."""
        msg = (
            f"<b>⚠️ Orden Rechazada: {symbol}</b>\n"
            f"<code>Razon: {reason}</code>"
        )
        self._broadcast(msg)

    def notify_spread_alert(self, symbol: str, current: float, average: float):
        """Notifica spread anomalo."""
        msg = (
            f"<b>⚠️ Spread Alto: {symbol}</b>\n"
            f"<code>Actual  : {current:.1f}</code>\n"
            f"<code>Promedio: {average:.1f}</code>\n"
            f"<code>Ratio   : {current/average:.2f}x</code>"
        )
        self._broadcast(msg)

    def notify_exposure_blocked(self, symbol: str):
        """Notifica que se bloqueo por exposicion existente."""
        msg = (
            f"<b>🛡️ Exposicion Existente: {symbol}</b>\n"
            f"<code>Ordenes pendientes o posiciones abiertas detectadas.</code>\n"
            f"<code>Nueva entrada bloqueada — Standby.</code>"
        )
        self._broadcast(msg)

    def notify_account_status(self, balance: float, equity: float,
                              margin_free: float, open_positions: int):
        """Reporte periodico del estado de cuenta."""
        msg = (
            "<b>📈 Estado de Cuenta</b>\n"
            f"<code>Balance    : ${balance:,.2f}</code>\n"
            f"<code>Equity     : ${equity:,.2f}</code>\n"
            f"<code>Margen Libre: ${margin_free:,.2f}</code>\n"
            f"<code>Posiciones : {open_positions}</code>\n"
            f"<code>Hora UTC   : {datetime.now(timezone.utc).strftime('%H:%M')}</code>"
        )
        self._broadcast(msg)

    def notify_error(self, error_msg: str, context: str = "General"):
        """Notifica un error critico."""
        msg = (
            f"<b>❌ Error Critico</b>\n"
            f"<code>Contexto: {context}</code>\n"
            f"<code>Error   : {error_msg[:500]}</code>\n"
            f"<code>Hora    : {datetime.now(timezone.utc).strftime('%H:%M')} UTC</code>"
        )
        self._broadcast(msg)

    def notify_heartbeat(self, uptime_hours: float, trades_today: int):
        """Heartbeat periodico para confirmar que el bot esta vivo."""
        msg = (
            "<b>💓 Heartbeat Kha0sys3</b>\n"
            f"<code>Uptime : {uptime_hours:.1f}h</code>\n"
            f"<code>Trades : {trades_today}</code>\n"
            f"<code>Estado : Operativo</code>\n"
            f"<code>Hora   : {datetime.now(timezone.utc).strftime('%H:%M')} UTC</code>"
        )
        self._broadcast(msg)

    def notify_orphan_cleanup(self, symbol: str, count: int):
        """Notifica limpieza de ordenes huerfanas."""
        msg = (
            f"<b>🧹 Limpieza Ordenes: {symbol}</b>\n"
            f"<code>Ordenes canceladas: {count}</code>"
        )
        self._broadcast(msg)
