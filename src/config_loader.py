"""Config loader — no pydantic (Python 3.14 compatible)."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from dotenv import load_dotenv

load_dotenv()


class LLMConfig:
    def __init__(
        self,
        provider: str = "gemini",
        api_key: str = "",
        model: str = "gemini-2.0-flash",
        temperature: float = 0.3,
        max_output_tokens: int = 120,
        base_url: Optional[str] = None,
        think: bool = False,
        request_timeout_sec: float = 60,
        connect_timeout_sec: float = 10,
        health_timeout_sec: float = 10,
        fail_cooldown_sec: float = 45,
    ):
        self.provider = provider
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.base_url = base_url
        self.think = think
        self.request_timeout_sec = request_timeout_sec
        self.connect_timeout_sec = connect_timeout_sec
        self.health_timeout_sec = health_timeout_sec
        self.fail_cooldown_sec = fail_cooldown_sec

    def model_copy(self, update: Optional[Dict[str, Any]] = None) -> "LLMConfig":
        d = dict(self.__dict__)
        if update:
            d.update(update)
        return LLMConfig(**d)


class PersonalityConfig:
    def __init__(self, data: Optional[Dict[str, Any]] = None):
        data = data or {}
        self.aggressiveness = int(data.get("aggressiveness", 2))
        self.political_mode = str(data.get("political_mode", "factchecker") or "factchecker")
        self.response_length = str(data.get("response_length", "short") or "short")
        self.emoji_intensity = int(data.get("emoji_intensity", 0))
        self.sc2_reference_level = int(data.get("sc2_reference_level", 0))
        self.topics = dict(data.get("topics") or {})
        self.custom_enabled = bool(data.get("custom_enabled", True))
        self.custom_prompt = str(data.get("custom_prompt") or "")


class Config:
    def __init__(self, data: Dict[str, Any]):
        data = dict(data or {})

        live = dict(data.get("live") or {})
        legacy = dict(data.get("sc2_stub") or {})
        if legacy and not live:
            live = legacy
        elif legacy and live:
            merged = dict(legacy)
            merged.update(live)
            live = merged
        data["live"] = live
        data["sc2_stub"] = live

        backend = str(data.get("chat_backend") or "simulated").strip().lower()
        if backend in ("sc2_stub", "ocr", "live_ocr"):
            backend = "live"
        data["chat_backend"] = backend

        llm_raw = data.get("llm") or {}
        gem_raw = data.get("gemini") or {}

        if llm_raw:
            self.llm = LLMConfig(
                provider=str(llm_raw.get("provider") or "gemini"),
                api_key=str(llm_raw.get("api_key") or ""),
                model=str(llm_raw.get("model") or "gemini-2.0-flash"),
                temperature=float(llm_raw.get("temperature", 0.3) or 0.3),
                max_output_tokens=int(llm_raw.get("max_output_tokens", 120) or 120),
                base_url=llm_raw.get("base_url"),
                think=bool(llm_raw.get("think", False)),
                request_timeout_sec=float(llm_raw.get("request_timeout_sec", 60) or 60),
                connect_timeout_sec=float(llm_raw.get("connect_timeout_sec", 10) or 10),
                health_timeout_sec=float(llm_raw.get("health_timeout_sec", 10) or 10),
                fail_cooldown_sec=float(llm_raw.get("fail_cooldown_sec", 45) or 45),
            )
        else:
            self.llm = None

        self.gemini = LLMConfig(
            provider="gemini",
            api_key=str(gem_raw.get("api_key") or ""),
            model=str(gem_raw.get("model") or "gemini-2.0-flash"),
            temperature=float(gem_raw.get("temperature", 0.3) or 0.3),
            max_output_tokens=int(gem_raw.get("max_output_tokens", 120) or 120),
        )

        self.owner = dict(data.get("owner") or {})
        self.personality = PersonalityConfig(data.get("personality") or {})
        self.behaviour = dict(data.get("behaviour") or {})
        self.anti_spam = dict(data.get("anti_spam") or {})
        self.memory = dict(data.get("memory") or {})
        self.blacklist = dict(data.get("blacklist") or {})
        self.favorites = dict(data.get("favorites") or {})
        self.research = dict(data.get("research") or {})
        self.factcheck = dict(data.get("factcheck") or {})
        self.triggers = list(data.get("triggers") or [])
        self.canned_blocks = list(data.get("canned_blocks") or [])
        self.logging = dict(data.get("logging") or {})
        self.chat_backend = data["chat_backend"]
        self.live = live
        self.sc2_stub = live

    def resolved_llm(self) -> LLMConfig:
        if self.llm is not None:
            provider = (self.llm.provider or "gemini").lower().strip()
            key = self.llm.api_key or self.gemini.api_key or os.getenv("GEMINI_API_KEY", "")
            if provider in ("ollama", "local") and not key:
                key = "ollama"
            base = self.llm.base_url
            if provider in ("ollama", "local") and not base:
                base = "http://127.0.0.1:11434/v1"
            return self.llm.model_copy(
                update={"api_key": key, "base_url": base, "provider": provider}
            )
        return LLMConfig(
            provider="gemini",
            api_key=self.gemini.api_key or os.getenv("GEMINI_API_KEY", ""),
            model=self.gemini.model,
            temperature=self.gemini.temperature,
            max_output_tokens=self.gemini.max_output_tokens,
        )

    @classmethod
    def load(cls, path: str | Path = "config/config.yml") -> "Config":
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Config not found: {path}. Create config/config.yml.")
        with path.open(encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        if not (data.get("gemini") or {}).get("api_key"):
            data.setdefault("gemini", {})["api_key"] = os.getenv("GEMINI_API_KEY", "")
        if data.get("llm") is not None and not data["llm"].get("api_key"):
            provider = str(data["llm"].get("provider") or "").lower()
            if provider in ("ollama", "local"):
                data["llm"]["api_key"] = os.getenv("LLM_API_KEY") or "ollama"
            else:
                data["llm"]["api_key"] = (
                    os.getenv("LLM_API_KEY")
                    or (data.get("gemini") or {}).get("api_key")
                    or os.getenv("GEMINI_API_KEY", "")
                )
        return cls(data)
