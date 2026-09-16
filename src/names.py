from __future__ import annotations

import re
from typing import Optional


def short_display_name(name: Optional[str]) -> str:
    if not name:
        return ""
    s = str(name).strip()
    # BattleTag#1234 → BattleTag
    if "#" in s:
        s = s.split("#", 1)[0].strip()
    return s


def memory_key(name: Optional[str]) -> str:
    return short_display_name(name).lower()
