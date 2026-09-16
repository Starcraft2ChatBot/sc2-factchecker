from __future__ import annotations

from abc import ABC, abstractmethod
from typing import AsyncIterator, Optional

from ..models import ChatMessage, Channel


class ChatBackend(ABC):
    """Abstract chat backend (simulated console or live SC2 OCR)."""

    @abstractmethod
    async def connect(self) -> None: ...

    @abstractmethod
    async def disconnect(self) -> None: ...

    @abstractmethod
    async def listen(self) -> AsyncIterator[ChatMessage]:
        """Yield new messages as they arrive."""
        ...

    @abstractmethod
    async def send(
        self,
        text: str,
        channel: Channel = Channel.ALL,
        target: Optional[str] = None,
        **kwargs,
    ) -> None:
        """Send a message into the lobby chat."""
        ...

    @abstractmethod
    async def is_connected(self) -> bool: ...
