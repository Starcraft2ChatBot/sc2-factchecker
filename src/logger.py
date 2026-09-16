from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any, Dict, Optional


def setup_logger(cfg: Optional[Dict[str, Any]] = None) -> logging.Logger:
    cfg = cfg or {}
    level_name = str(cfg.get("level", "INFO")).upper()
    level = getattr(logging, level_name, logging.INFO)

    logger = logging.getLogger("sc2_factchecker")
    logger.setLevel(level)
    logger.handlers.clear()
    logger.propagate = False

    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s", "%H:%M:%S")

    if cfg.get("console", True):
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(level)
        ch.setFormatter(fmt)
        logger.addHandler(ch)

    log_file = cfg.get("file")
    if log_file:
        path = Path(str(log_file))
        path.parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(path, encoding="utf-8")
        fh.setLevel(level)
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    return logger
