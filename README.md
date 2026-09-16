# SC2 Lobby Fact-Checker Bot

**Precise, evidence-based fact-checking for StarCraft II lobby chat.**

This is a separate bot from the general SC2 chatbot. It keeps the same OCR + pipeline architecture but replaces personality chatter with rigorous claim detection and multi-source research.

> Educational / research use only. Live client OCR + keyboard automation may violate Blizzard Terms of Service and can result in account action. Use at your own risk.

## What it does

1. **OCR chat capture** (or simulated backend for testing)  
   Polls a configured screen region, parses `[N. Channel] Player: message` lines, joins continuations, deduplicates.

2. **Claim detection**  
   Triggers research when messages contain factual assertions, numbers, “studies show”, “prove it”, sources requests, etc. Skips pure banter and insults with no claim.

3. **Multi-source research pipeline**  
   - Claim extraction (1–3 atomic claims)  
   - Query generation (neutral + debunk-style)  
   - Parallel-ish fetches: DuckDuckGo, Wikipedia, Google News RSS, Fact Check tools, optional Bible API  
   - Evidence compression into a short RESEARCH BRIEF with support / contradict / confidence  
   - TTL cache so the same claim isn’t re-researched every spam

4. **Verdict replies**  
   Short lowercase lobby style:  
   `mixed evidence on that — reuters and factcheck.org disagree on the numbers`  
   Never invents sources. Says “unverified” when evidence is thin.

## Quick start (Windows)

```bat
start.bat
```

Or:

```bat
python -m pip install -r requirements.txt
copy config\config.example.yaml config\config.yaml
# edit config.yaml → set llm.api_key + owner names + (optional) OCR region
python main.py
```

## Config highlights

See `config/config.example.yaml`:

- `research.*` — timeout, cache TTL, trigger substrings, max claims
- `factcheck.*` — reply on unverified, min confidence to call something false
- `personality.custom_prompt` — already set to the fact-checker system prompt
- `chat_backend: "simulated"` for safe testing, `"sc2_stub"` for live OCR

## OCR / live mode

1. Install Tesseract and put it on PATH (or set `sc2_stub.tesseract_cmd`).
2. Run StarCraft II in Windowed / Borderless.
3. Measure the chat region: `python tools/measure_chat_region.py`
4. Set `chat_backend: "sc2_stub"`, `ocr_enabled: true`, and the region in config.
5. Restart the bot.

## Architecture (kept from the original chatbot)

- `src/chat/sc2_stub.py` — OCR + window focus + paste/type send path  
- `src/decision_engine.py` — anti-spam → research → LLM → post-process  
- `src/research.py` — multi-source evidence gathering  
- `src/llm_client.py` — Gemini / OpenAI-compatible / Ollama  
- YAML-driven config, owner commands (`!reload`, mute, etc.)

## Differences from the general chatbot

| Feature              | Chatbot                  | Fact-Checker                     |
|----------------------|--------------------------|----------------------------------|
| Personality          | troll / propaganda / custom | **Fact-checker only**           |
| Reply trigger        | probability + mentions   | Claim / evidence request first  |
| Research             | optional light research  | **Always strong multi-source**  |
| Tone                 | playful / aggressive     | Calm, precise, non-partisan     |
| Invented sources     | possible in troll modes  | **Strictly forbidden**          |

## License

MIT (same as the sibling chatbot). Educational use only.
