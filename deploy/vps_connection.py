"""
VPS Connection Module — Kha0sys3
Gateway WinRM para ejecutar comandos remotos en el VPS Windows Server.

Credenciales se leen desde .env (raiz del repo) o variables de entorno:
    VPS_IP, VPS_PORT, VPS_USER, VPS_PASS
"""

import os
import sys
import winrm
from typing import Optional

# Asegura que la raiz del repo este en sys.path para importar src.domain
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from src.domain.env_loader import load_env


def _required_env(key: str) -> str:
    val = os.environ.get(key)
    if not val:
        raise RuntimeError(
            f"VPSConnection: variable de entorno {key!r} no esta definida. "
            f"Crea .env en la raiz del repo (ver .env.example) o exportala."
        )
    return val


class VPSConnection:
    """Conexion WinRM al VPS Windows Server. Patron Singleton por sesion."""

    def __init__(self):
        load_env()
        self.VPS_IP = _required_env("VPS_IP")
        self.VPS_PORT = int(os.environ.get("VPS_PORT", "5986"))
        self.VPS_USER = _required_env("VPS_USER")
        self.VPS_PASS = _required_env("VPS_PASS")
        self._session: Optional[winrm.Session] = None

    @property
    def endpoint(self) -> str:
        return f"https://{self.VPS_IP}:{self.VPS_PORT}/wsman"

    def connect(self) -> winrm.Session:
        if self._session is None:
            self._session = winrm.Session(
                self.endpoint,
                auth=(self.VPS_USER, self.VPS_PASS),
                transport="basic",
                server_cert_validation="ignore",
            )
        return self._session

    def run_ps(self, script: str) -> dict:
        """Ejecuta un script PowerShell remoto y devuelve stdout/stderr."""
        session = self.connect()
        result = session.run_ps(script)
        return {
            "stdout": result.std_out.decode("utf-8", errors="replace").strip(),
            "stderr": result.std_err.decode("utf-8", errors="replace").strip(),
            "status": result.status_code,
        }

    def run_cmd(self, command: str) -> dict:
        """Ejecuta un comando CMD remoto."""
        session = self.connect()
        result = session.run_cmd(command)
        return {
            "stdout": result.std_out.decode("utf-8", errors="replace").strip(),
            "stderr": result.std_err.decode("utf-8", errors="replace").strip(),
            "status": result.status_code,
        }

    def upload_file(self, local_content: str, remote_path: str) -> dict:
        """Sube contenido como archivo al VPS via base64 + PowerShell."""
        import base64

        encoded = base64.b64encode(local_content.encode("utf-8")).decode("ascii")
        ps_script = (
            f"$bytes = [Convert]::FromBase64String('{encoded}');"
            f"[IO.File]::WriteAllBytes('{remote_path}', $bytes)"
        )
        return self.run_ps(ps_script)

    def test_connection(self) -> bool:
        """Verifica conectividad basica con el VPS."""
        try:
            result = self.run_ps("Get-Date")
            return result["status"] == 0
        except Exception as e:
            print(f"Error de conexion VPS: {e}")
            return False
