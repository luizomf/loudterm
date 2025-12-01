# loudterm — TTS playground in your terminal

![loudterm](./assets/loudterm-logo-medium.png)

Interactive REPL that turns text into speech using the Kokoro 82M model. Pick
voices/languages, stream audio, auto‑play, and auto‑save WAVs without leaving
the terminal.

## Features

- Kokoro 82M multi‑language voices (English, Portuguese, Spanish, Japanese,
  Chinese, French, Hindi, Italian).
- Streaming generation with optional auto‑play and auto‑save to `output/`.
- Fast voice switching with inline completions (`@af_heart`, `@pf_dora`, etc.).
- Prompt Toolkit UI with Meta+Enter submission, bottom toolbar state, and
  vim/emacs editing modes.
- Simple commands (`/exit`) plus Ctrl+S / Ctrl+P toggles for save/play.

## Requirements

- Python 3.13+.
- Audio deps: `sounddevice` (PortAudio) and `soundfile` (libsndfile). Install
  via your package manager if not provided by wheels.
- First run downloads ~300 MB Kokoro weights from Hugging Face.
- Optional (Japanese voices): `uv run -m unidic download` to fetch dictionaries.

## Installation

Using [uv](https://docs.astral.sh/uv/):

```bash
uv python install 3.13.9
uv python pin 3.13.9
uv sync
# Optional for Japanese voices
uv run -m unidic download
```

With pip (slower to resolve extras):

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
python -m unidic download  # only if you want Japanese voices
```

## Running

```bash
uv run loudterm
# or
python -m loudterm.cli
```

On first launch, wait for Kokoro weights to download; you’ll see a “Engine
ready!” message when loaded.

## Usage

- Type or paste text, then submit with `Meta+Enter` (Alt+Enter) or `Esc` then
  `Enter`.
- Change voice/language inline: type `@` and use tab completion, e.g. `@pf_dora`
  (pt-BR), `@bf_emma` (en-GB), `@jf_alpha` (ja), `@zf_xiaoxiao` (zh).
- Exit: `/exit`, `/quit`, `/q`, or `/bye`.
- Toggles during the session:
  - `Ctrl+S`: toggle `auto_save` (writes timestamped WAVs to `output/`).
  - `Ctrl+P`: toggle `auto_play`.
- Bottom toolbar shows current toggles + voice.

Generated files live in `output/` as `<timestamp>_<voice>.wav`.

## Development

- Lint/type-check: `uv run ruff check .` and `uv run pyright`.
- Tests (none yet besides placeholder): `uv run pytest`.
- Convenience with just:
  - `just run` — clear terminal and start loudterm.
  - `just setup` — install/pin Python 3.13.9 and sync deps.

## Troubleshooting

- “No default output device” → configure your OS audio output or pass
  `sd.default.device` environment vars.
- Model download slow/fails → verify network access to Hugging Face; rerun after
  connectivity is stable.
- Japanese voices raising tokenizer errors → run `uv run -m unidic download` (or
  the pip equivalent) once.
