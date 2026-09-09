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

- Python 3.14+ (the checkout pins 3.14).
- Audio deps: `sounddevice` (PortAudio) and `soundfile` (libsndfile). Install
  via your package manager if not provided by wheels.
- First run downloads ~300 MB Kokoro weights from Hugging Face.
- Japanese voices require the `japanese` extra and a dictionary download (below).

## Installation

Using [uv](https://docs.astral.sh/uv/):

```bash
uv python install 3.14
uv python pin 3.14
uv sync
# Optional for Japanese voices (adds mojimoji)
uv sync --extra japanese
uv run --extra japanese -m unidic download
```

With pip (slower to resolve extras):

Prefer the uv checkout workflow above if `curated-tokenizers` needs a source
build: pip does not apply the project's uv build constraint (see Troubleshooting).

```bash
python3.14 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
# Optional for Japanese voices
pip install -e '.[japanese]'
python -m unidic download
```

## Running

```bash
uv run loudterm
# For Japanese voices, retain the extra when running:
uv run --extra japanese loudterm
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
For a source checkout, this is the repository's `output/` directory, not the
current working directory. With a tool installation, it is relative to the
installed package: for example, `~/.local/share/uv/tools/loudterm/lib/python3.14/output/`
on the macOS setup reported in [issue #4](https://github.com/luizomf/loudterm/issues/4).
Back up recordings before removing or reinstalling the tool environment.

## Kokoro Notes

Tem uma nota prática e humana sobre Kokoro em
[`docs/kokoro-notes.md`](./docs/kokoro-notes.md). Ela cobre:

- como deixar a fala menos monótona
- mistura de vozes
- uso de `speed`
- inspeção de tokens com `--show-tokens`
- o que parece funcionar em inglês, mas não encaixa tão bem em PT-BR

## Development

- Lint/type-check: `uv run ruff check .` and `uv run pyright`.
- Tests (none yet besides placeholder): `uv run pytest`.
- Convenience with just:
  - `just run` — clear terminal and start loudterm.
  - `just setup` — install/pin Python 3.14 and sync deps.

## Troubleshooting

- Python version errors during installation → this project requires Python
  3.14 or newer. Older README versions incorrectly instructed users to pin
  3.13.9. In the checkout, run `uv python install 3.14`, `uv python pin 3.14`,
  then `uv sync`.
- `curated-tokenizers` build fails with `Compiler crash in OptimizeBuiltinCalls`
  → update your checkout and run `uv sync --locked`. The project constrains
  isolated builds to Cython 3.2.4 because 3.3.0 crashes on this dependency.
  Installing Cython into `.venv` does not control an isolated build. This
  constraint applies to the checkout's uv workflow, not automatically to pip
  or `uv tool install`.
- “No default output device” → configure your OS audio output or pass
  `sd.default.device` environment vars.
- Model download slow/fails → verify network access to Hugging Face; rerun after
  connectivity is stable.
- Japanese voices raising tokenizer errors → install with `uv sync --extra japanese`,
  run `uv run --extra japanese -m unidic download` once, then use
  `uv run --extra japanese loudterm`. Default installs omit `mojimoji`, which
  Misaki imports for Japanese; existing Japanese users must opt into the extra.
  This extra only moves `mojimoji`, not all Japanese dependencies.

---

## Kokoro Instructions and Acknowledgements

The text below was copied directly from the
[Kokoro repository](https://github.com/hexgrad/kokoro/blob/main/README.md).
These are upstream model examples, not loudterm installation instructions;
loudterm still requires Python 3.14+, including when using Conda.

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
