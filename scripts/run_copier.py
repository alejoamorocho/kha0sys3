"""Entry point for the trade copier (NSSM service Kha0sysCopier).

Reads src/execution/copier_config.json. Pass --live to force dry_run=false
(otherwise the config's dry_run value is used). Pass --dry-run to force observe.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.execution.trade_copier import TradeCopier

CONFIG_PATH = Path(__file__).resolve().parent.parent / "src" / "execution" / "copier_config.json"


def main() -> None:
    cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    if "--live" in sys.argv:
        cfg["dry_run"] = False
    if "--dry-run" in sys.argv:
        cfg["dry_run"] = True

    telegram = None
    try:
        from src.monitoring.telegram_notifier import TelegramNotifier
        telegram = TelegramNotifier()
    except Exception as e:
        print(f"[COPIER] Telegram init skipped: {e}", flush=True)

    TradeCopier(cfg, telegram=telegram).run()


if __name__ == "__main__":
    main()
