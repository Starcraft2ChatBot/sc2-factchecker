from __future__ import annotations

import asyncio
from typing import AsyncIterator, List, Optional

from ..models import ChatMessage, Channel
from .base import ChatBackend


class SimulatedChatBackend(ChatBackend):
    """Console backend for testing without StarCraft II."""

    def __init__(self, self_name: str = "FactChecker"):
        self.self_name = self_name
        self._queue: asyncio.Queue[ChatMessage] = asyncio.Queue()
        self._connected = False
        self._history: List[ChatMessage] = []

    async def connect(self) -> None:
        self._connected = True
        print(
            f"[simulated] Connected as {self.self_name}. "
            "Type messages as: PlayerName: message text  (empty line to skip)"
        )

    async def disconnect(self) -> None:
        self._connected = False

    async def is_connected(self) -> bool:
        return self._connected

    async def listen(self) -> AsyncIterator[ChatMessage]:
        loop = asyncio.get_event_loop()
        while self._connected:
            try:
                line = await loop.run_in_executor(None, input, "> ")
            except EOFError:
                break
            line = (line or "").strip()
            if not line:
                continue
            if ":" in line:
                player, text = line.split(":", 1)
                player, text = player.strip(), text.strip()
            else:
                player, text = "TestPlayer", line
            msg = ChatMessage(player=player, text=text, channel=Channel.ALL)
            self._history.append(msg)
            yield msg

    async def send(
        self,
        text: str,
        channel: Channel = Channel.ALL,
        target: Optional[str] = None,
        **kwargs,
    ) -> None:
        print(f"[BOT → {channel.value}] {text}")
