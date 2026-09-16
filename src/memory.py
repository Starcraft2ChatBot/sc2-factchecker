from __future__ import annotations

import json
import logging
from collections import defaultdict, deque
from pathlib import Path
from typing import Deque, Dict, List, Optional

from .models import ChatMessage
from .names import memory_key

logger = logging.getLogger("sc2_factchecker.memory")


class ConversationMemory:
    def __init__(self, max_per_player: int = 20, persist_path: Optional[str] = None):
        self.max_per_player = max(5, int(max_per_player or 20))
        self.persist_path = Path(persist_path) if persist_path else None
        self._data: Dict[str, Deque[ChatMessage]] = defaultdict(
            lambda: deque(maxlen=self.max_per_player)
        )
        if self.persist_path and self.persist_path.exists():
            try:
                self._load()
            except Exception:
                logger.exception("Failed to load memory")

    def add(self, msg: ChatMessage) -> None:
        key = memory_key(msg.player)
        self._data[key].append(msg)
        self._maybe_persist()

    def get_context(self, player: str) -> List[ChatMessage]:
        return list(self._data.get(memory_key(player), []))

    def _maybe_persist(self) -> None:
        if not self.persist_path:
            return
        try:
            self.persist_path.parent.mkdir(parents=True, exist_ok=True)
            payload = {}
            for k, dq in self._data.items():
                payload[k] = [
                    {
                        "player": m.player,
                        "text": m.text,
                        "is_self": m.is_self,
                        "display_name": m.display_name,
                    }
                    for m in dq
                ]
            self.persist_path.write_text(json.dumps(payload, ensure_ascii=False, indent=0), encoding="utf-8")
        except Exception:
            logger.debug("memory persist failed", exc_info=True)

    def _load(self) -> None:
        raw = json.loads(self.persist_path.read_text(encoding="utf-8"))
        for k, items in (raw or {}).items():
            dq: Deque[ChatMessage] = deque(maxlen=self.max_per_player)
            for it in items[-self.max_per_player :]:
                dq.append(
                    ChatMessage(
                        player=it.get("player") or k,
                        text=it.get("text") or "",
                        is_self=bool(it.get("is_self")),
                        display_name=it.get("display_name") or "",
                    )
                )
            self._data[k] = dq
