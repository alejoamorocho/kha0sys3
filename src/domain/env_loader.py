"""
Env loader — Kha0sys3
Lee .env desde la raiz del repo y carga variables a os.environ si no estan
ya definidas. Sin dependencias externas (no usa python-dotenv).

Uso:
    from src.domain.env_loader import load_env
    load_env()
    token = os.environ["TELEGRAM_TOKEN"]
"""
from __future__ import annotations

import os
from pathlib import Path

_LOADED = False


def _find_env_file(start: Path) -> Path | None:
    """Busca .env subiendo desde start hasta encontrarlo o llegar a la raiz."""
    cur = start.resolve()
    for parent in (cur, *cur.parents):
        candidate = parent / ".env"
        if candidate.exists():
            return candidate
    return None


def _parse_line(line: str) -> tuple[str, str] | None:
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    if "=" not in line:
        return None
    key, _, val = line.partition("=")
    key = key.strip()
    val = val.strip()
    # Strip wrapping quotes (single or double) if present
    if len(val) >= 2 and val[0] == val[-1] and val[0] in ("'", '"'):
        val = val[1:-1]
    return key, val


def load_env(env_path: str | Path | None = None, override: bool = False) -> dict[str, str]:
    """Carga .env. Idempotente — ejecutar mas de una vez es no-op por defecto.

    Args:
        env_path: ruta explicita; si None, busca .env desde cwd hacia arriba.
        override: si True, sobreescribe variables ya presentes en os.environ.

    Returns:
        Dict de las claves que se cargaron desde el archivo (vacio si no existe).
    """
    global _LOADED
    if _LOADED and env_path is None:
        return {}

    path = Path(env_path) if env_path else _find_env_file(Path.cwd())
    loaded: dict[str, str] = {}
    if path is None or not path.exists():
        _LOADED = True
        return loaded

    try:
        with open(path, "r", encoding="utf-8") as f:
            for raw in f:
                parsed = _parse_line(raw)
                if parsed is None:
                    continue
                key, val = parsed
                if override or key not in os.environ:
                    os.environ[key] = val
                loaded[key] = val
    except Exception as e:
        print(f"env_loader: warning leyendo {path}: {e}")

    _LOADED = True
    return loaded
