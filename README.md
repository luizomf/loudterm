# loudterm — TTS playground in your terminal

![loudterm](./assets/loudterm-logo-medium.png)

Interactive REPL that turns text into speech using the
[Kokoro 82M model](https://github.com/hexgrad/kokoro). Pick voices/languages,
stream audio, auto‑play, and auto‑save WAVs without leaving the terminal.

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

---

## Kokoro Instructions and Acknowledgements

The text below was copied directly from the
[Kokoro repository](https://github.com/hexgrad/kokoro/blob/main/README.md).

### Windows Installation

To install espeak-ng on Windows:

1. Go to [espeak-ng releases](https://github.com/espeak-ng/espeak-ng/releases)
2. Click on **Latest release**
3. Download the appropriate `*.msi` file (e.g.
   **espeak-ng-20191129-b702b03-x64.msi**)
4. Run the downloaded installer

For advanced configuration and usage on Windows, see the
[official espeak-ng Windows guide](https://github.com/espeak-ng/espeak-ng/blob/master/docs/guide.md)

### MacOS Apple Silicon GPU Acceleration

On Mac M1/M2/M3/M4 devices, you can explicitly specify the environment variable
`PYTORCH_ENABLE_MPS_FALLBACK=1` to enable GPU acceleration.

```bash
PYTORCH_ENABLE_MPS_FALLBACK=1 python run-your-kokoro-script.py
```

### Conda Environment

Use the following conda `environment.yml` if you're facing any dependency
issues.

```yaml
name: kokoro
channels:
  - defaults
dependencies:
  - python==3.9
  - libstdcxx~=12.4.0 # Needed to load espeak correctly. Try removing this if you're facing issues with Espeak fallback.
  - pip:
      - kokoro>=0.3.1
      - soundfile
      - misaki[en]
```

### Acknowledgements

- 🛠️ [@yl4579](https://huggingface.co/yl4579) for architecting StyleTTS 2.
- 🏆 [@Pendrokar](https://huggingface.co/Pendrokar) for adding Kokoro as a
  contender in the TTS Spaces Arena.
- 📊 Thank you to everyone who contributed synthetic training data.
- ❤️ Special thanks to all compute sponsors.
- 👾 Discord server: https://discord.gg/QuGxSWBfQy
- 🪽 Kokoro is a Japanese word that translates to "heart" or "spirit". Kokoro is
  also a
  [character in the Terminator franchise](https://terminator.fandom.com/wiki/Kokoro)
  along with
  [Misaki](https://github.com/hexgrad/misaki?tab=readme-ov-file#acknowledgements).
