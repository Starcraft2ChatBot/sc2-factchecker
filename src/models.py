from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Channel(str, Enum):
    ALL = "all"
    GENERAL = "general"
    ARCADE = "arcade"
    COOP = "coop"
    TEAM = "team"
    WHISPER = "whisper"
    SYSTEM = "system"


@dataclass
class ChatMessage:
    player: str
    text: str
    channel: Channel = Channel.ALL
    is_self: bool = False
    display_name: str = ""
    chat_tab_index: int = 0
    chat_tab: str = ""
    is_game_request: bool = False
    game_request_kind: str = ""

    def __str__(self) -> str:
        who = self.display_name or self.player
        return f"[{self.channel.value}] {who}: {self.text}"
