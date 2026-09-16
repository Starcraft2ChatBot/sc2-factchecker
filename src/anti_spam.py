from __future__ import annotations

import time
from collections import defaultdict, deque
from typing import Any, Dict, Deque

from .names import memory_key


class AntiSpam:
    def __init__(self, cfg: Dict[str, Any] | None = None):
        cfg = cfg or {}
        self.global_cooldown = float(cfg.get("global_cooldown_sec", 4) or 4)
        self.per_player_cooldown = float(cfg.get("per_player_cooldown_sec", 12) or 12)
        self.max_per_minute = int(cfg.get("max_replies_per_player_per_minute", 4) or 4)
        self.mute_list = {memory_key(n) for n in (cfg.get("mute_list") or []) if n}
        self._last_global = 0.0
        self._last_player: Dict[str, float] = {}
        self._player_hits: Dict[str, Deque[float]] = defaultdict(deque)

    def can_reply(self, msg) -> bool:
        key = memory_key(getattr(msg, "player", "") or "")
        if key in self.mute_list:
            return False
        now = time.time()
        if now - self._last_global < self.global_cooldown:
            return False
        if now - self._last_player.get(key, 0.0) < self.per_player_cooldown:
            return False
        hits = self._player_hits[key]
        while hits and now - hits[0] > 60.0:
            hits.popleft()
        if len(hits) >= self.max_per_minute:
            return False
        return True

    def record_reply(self, player: str) -> None:
        key = memory_key(player)
        now = time.time()
        self._last_global = now
        self._last_player[key] = now
        self._player_hits[key].append(now)
