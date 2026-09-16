from __future__ import annotations

from dataclasses import dataclass
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
    raw: str = ""

    def __str__(self) -> str:
        who = self.display_name or self.player
        return f"[{self.channel.value}] {who}: {self.text}"

    @classmethod
    def from_parts(
        cls,
        player: str,
        text: str,
        channel: Channel = Channel.ALL,
        is_self: bool = False,
        raw: str = "",
        chat_tab: str = "",
        chat_tab_index: int = 0,
    ) -> "ChatMessage":
        return cls(
            player=player,
            text=text,
            channel=channel,
            is_self=is_self,
            display_name=player,
            chat_tab=chat_tab,
            chat_tab_index=chat_tab_index,
            raw=raw,
        )
