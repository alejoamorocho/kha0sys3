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

    def upload_file(self, local_content: str, remote_path: str, chunk: int = 2000) -> dict:
        """Sube contenido como archivo al VPS via base64 + PowerShell.

        Trocea el base64 (append a un .b64 temporal) y luego decodifica, porque
        meter todo el base64 inline en UNA linea de PowerShell revienta el limite
        de la linea de comando (~8KB) para archivos no triviales ("The command
        line is too long"). El base64 solo usa [A-Za-z0-9+/=], asi que es seguro
        envolverlo en comillas simples de PowerShell.
        """
        import base64

        encoded = base64.b64encode(local_content.encode("utf-8")).decode("ascii")
        tmp = remote_path + ".b64upload"
        # Limpia cualquier upload previo a medias.
        self.run_ps(f"Remove-Item '{tmp}' -Force -ErrorAction SilentlyContinue")
        for i in range(0, len(encoded), chunk):
            part = encoded[i:i + chunk]
            r = self.run_ps(f"Add-Content -Path '{tmp}' -Value '{part}' -NoNewline -Encoding ascii")
            if r["status"] != 0:
                return r
        # Decodifica el .b64 completo al destino y limpia el temporal.
        decode = (
            f"$b64 = Get-Content '{tmp}' -Raw; "
            f"[IO.File]::WriteAllBytes('{remote_path}', [Convert]::FromBase64String($b64)); "
            f"Remove-Item '{tmp}' -Force -ErrorAction SilentlyContinue"
        )
        return self.run_ps(decode)

    def test_connection(self) -> bool:
        """Verifica conectividad basica con el VPS."""
        try:
            result = self.run_ps("Get-Date")
            return result["status"] == 0
        except Exception as e:
            print(f"Error de conexion VPS: {e}")
            return False
