# SC2 Lobby Fact-Checker Bot

**Only corrects lies and false claims — with credible sources.**

This bot watches StarCraft II lobby chat, detects factual claims that look false or misleading, researches them using high-credibility sources, and replies with a short correction plus a named source.

It does **not** chatter, troll, or reply to pure opinions / banter.

> Educational / research use only. Live client OCR + keyboard automation may violate Blizzard Terms of Service.

## Behavior

1. **OCR / simulated chat capture** — same pipeline as the general SC2 chatbot.
2. **Claim detection** — only messages that look like factual assertions, absolute claims, “studies show”, numbers, “prove it”, etc.
3. **Multi-source research** with credibility ranking:
   - Prefer fact-checkers, wire services (Reuters, AP), major news, .gov / .edu, Wikipedia
   - Down-rank blogs, social media, low-quality sites
4. **Reply only when evidence supports a correction**
   - Format: `thats false. [what actually happened]. source: reuters`
   - Or: `mixed — [nuance]. (ap / factcheck.org)`
   - Never invent a source name
5. **Silence** on pure banter, insults without claims, and unverifiable noise (configurable).

## Quick start (Windows)

```bat
start.bat
```

Or:

```bat
python -m pip install -r requirements.txt
copy config\config.example.yaml config\config.yaml
# set llm.api_key + owner names
python main.py
```

## Key config

```yaml
research:
  enabled: true
  timeout_sec: 12
  max_chars: 1200
  cache_ttl_sec: 600
  max_claims: 3
  prefer_domains: []          # optional extra boost

factcheck:
  enabled: true
  reply_on_unverified: true   # set false to stay silent when no good sources
  min_confidence_to_call_false: "medium"

behaviour:
  reply_probability: 0.25     # low — bot prefers silence unless correcting
```

## Live OCR

1. Install Tesseract.
2. Windowed / borderless SC2.
3. `python tools/measure_chat_region.py`
4. Set `chat_backend: "sc2_stub"`, `ocr_enabled: true`, and the region.

## Architecture

- `src/chat/sc2_stub.py` — OCR + send
- `src/research.py` — claim extraction, multi-query search, credibility filter, ranked brief
- `src/decision_engine.py` — only replies when research supports a correction
- `src/llm_client.py` — Gemini / OpenAI-compatible / Ollama

## License

MIT. Educational use only.
