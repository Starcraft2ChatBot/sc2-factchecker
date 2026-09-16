# SC2 Lobby Fact-Checker

Corrects false claims in StarCraft II lobby chat using live web research and real source URLs.

> Educational use only. Live OCR + keyboard automation may violate Blizzard ToS.

## Instant deploy (ZIP download)

1. **Download ZIP** from GitHub → Code → Download ZIP → extract
2. **Install Python 3.10+** and (for live mode) [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
3. Open a terminal in the extracted folder:

```bat
python -m pip install -r requirements.txt
```

4. Edit **`config/config.yml`**:
   - Set `llm.api_key` (Gemini or other provider)
   - Set `owner.names` and `live.self_name` to your Battle.net / in-game name
5. **Test without SC2:**

```bat
start.bat
```

   (`chat_backend: "simulated"` is the default)

6. **Live lobby mode:**
   - Run SC2 windowed / borderless
   - `python tools/measure_chat_region.py` → paste `chat_region` into `config/config.yml`
   - Set `chat_backend: "live"` and `live.ocr_enabled: true`
   - Run `start.bat` again

## What it does

- Detects factual claims / "prove it" / "studies show" style messages
- Searches the web (news, Wikipedia, fact-checkers, DuckDuckGo)
- Keeps only credible sources that have a real URL
- Replies only when evidence supports a correction, e.g.
  `thats false. [correction]. https://www.reuters.com/...`
- Stays silent on pure banter and opinions

## Config

All settings live in **`config/config.yml`** (only config file).

| Key | Meaning |
|-----|---------|
| `chat_backend` | `simulated` or `live` |
| `live` | OCR window region, Tesseract, self name (live mode only) |
| `research` | triggers, timeouts, require_url |
| `factcheck` | full URLs, reply_on_unverified |

## Requirements

See `requirements.txt`. Optional live deps: `pyautogui`, `mss`, `Pillow`, `pytesseract`, `pyperclip`.

## License

MIT. Educational use only.
