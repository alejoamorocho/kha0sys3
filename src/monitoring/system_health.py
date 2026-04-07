"""
System Health Monitor — Kha0sys3
Monitorea el estado del sistema: CPU, RAM, disco, MT5, procesos Python.
"""

import psutil
import os
import subprocess
from datetime import datetime
from dataclasses import dataclass
from typing import Optional

import MetaTrader5 as mt5


@dataclass
class SystemHealth:
    cpu_percent: float
    ram_used_gb: float
    ram_total_gb: float
    ram_percent: float
    disk_used_gb: float
    disk_total_gb: float
    disk_percent: float
    python_processes: int
    mt5_running: bool
    mt5_connected: bool
    mt5_trade_allowed: bool
    uptime_hours: float
    timestamp: datetime


class SystemHealthMonitor:
    """Monitorea la salud del sistema operativo y servicios criticos."""

    def __init__(self):
        self._boot_time = psutil.boot_time()

    def get_health(self) -> SystemHealth:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage("C:\\")

        python_procs = len([
            p for p in psutil.process_iter(["name"])
            if "python" in (p.info["name"] or "").lower()
        ])

        mt5_running = any(
            "terminal" in (p.info["name"] or "").lower() or
            "metatrader" in (p.info["name"] or "").lower()
            for p in psutil.process_iter(["name"])
        )

        mt5_connected = False
        mt5_trade_allowed = False
        try:
            term_info = mt5.terminal_info()
            if term_info:
                mt5_connected = term_info.connected
                mt5_trade_allowed = term_info.trade_allowed
        except Exception:
            pass

        uptime_seconds = (datetime.now().timestamp() - self._boot_time)

        return SystemHealth(
            cpu_percent=cpu,
            ram_used_gb=ram.used / (1024 ** 3),
            ram_total_gb=ram.total / (1024 ** 3),
            ram_percent=ram.percent,
            disk_used_gb=disk.used / (1024 ** 3),
            disk_total_gb=disk.total / (1024 ** 3),
            disk_percent=disk.percent,
            python_processes=python_procs,
            mt5_running=mt5_running,
            mt5_connected=mt5_connected,
            mt5_trade_allowed=mt5_trade_allowed,
            uptime_hours=uptime_seconds / 3600,
            timestamp=datetime.utcnow(),
        )

    def check_nssm_service(self, service_name: str) -> str:
        """Verifica el estado de un servicio NSSM."""
        try:
            result = subprocess.run(
                ["C:\\nssm\\nssm.exe", "status", service_name],
                capture_output=True, text=True, timeout=10,
            )
            return result.stdout.strip()
        except Exception:
            return "UNKNOWN"

    def get_critical_alerts(self) -> list[str]:
        """Devuelve lista de alertas criticas del sistema."""
        health = self.get_health()
        alerts = []

        if health.cpu_percent > 90:
            alerts.append(f"CPU critico: {health.cpu_percent:.1f}%")
        if health.ram_percent > 90:
            alerts.append(f"RAM critica: {health.ram_percent:.1f}%")
        if health.disk_percent > 95:
            alerts.append(f"Disco critico: {health.disk_percent:.1f}%")
        if not health.mt5_running:
            alerts.append("MetaTrader 5 NO esta corriendo")
        if not health.mt5_connected:
            alerts.append("MT5 NO conectado al broker")
        if not health.mt5_trade_allowed:
            alerts.append("MT5 trading NO permitido")

        return alerts
