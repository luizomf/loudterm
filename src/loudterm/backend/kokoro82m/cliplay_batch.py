# ruff: noqa: ERA001
"""
Streaming batch TTS: watches a directory for chunk_N.txt files as they arrive
from ollama, generates audio and plays each chunk immediately.

Usage:
    cliplay_batch -d /tmp/tts_workdir -n 33 [-l a] [-v af_heart]

Runs in parallel with the ollama xargs process. As each chunk_N.txt appears,
it generates audio via Kokoro and plays it. No waiting for all chunks.
"""
import argparse
import sys
import textwrap
import time
import warnings
from concurrent.futures import ThreadPoolExecutor, Future
from pathlib import Path

import sounddevice as sd
import torch
from kokoro import KPipeline


def run() -> None:
    parser = argparse.ArgumentParser(
        "cliplay_batch",
        description=textwrap.dedent("""
            Streaming batch TTS: watches for chunks and plays as they arrive.
        """),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-d", "--dir",
        required=True,
        help="Directory where chunk_N.txt files will appear.",
    )
    parser.add_argument(
        "-n", "--total",
        type=int,
        required=True,
        help="Total number of chunks to expect.",
    )
    parser.add_argument(
        "-l", "--language",
        default="a",
        help="Language code (default: 'a' for American English).",
    )
    parser.add_argument(
        "-v", "--voice",
        help="Voice name (e.g., 'af_heart', 'pf_dora').",
    )

    args = parser.parse_args()
    workdir = Path(args.dir)

    if not workdir.is_dir():
        print(f"Error: {workdir} is not a directory.", file=sys.stderr)
        sys.exit(1)

    stream_and_play(workdir, args.total, args.language, args.voice)


def stream_and_play(
    workdir: Path,
    total: int,
    lang_code: str,
    voice_name: str | None = None,
) -> None:
    from loudterm.backend.kokoro82m.voices import KOKORO_VOICES

    sr = 24000

    if voice_name:
        voice_key = f"@{voice_name}"
        if voice_key in KOKORO_VOICES:
            voice = voice_name
            lang_code = KOKORO_VOICES[voice_key]["language_code"]
        else:
            print(f"Warning: Voice '{voice_name}' not found. Falling back to defaults.")
            voice = "af_heart"
            lang_code = lang_code or "a"
    else:
        langs = {
            "a": "af_heart",
            "p": "pf_dora",
            "b": "bf_emma",
            "j": "jf_alpha",
            "z": "zf_xiaoxiao",
            "e": "ef_dora",
            "f": "ff_siwis",
            "h": "hf_alpha",
            "i": "if_sara",
        }
        voice = langs.get(lang_code, "af_heart")

    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            category=FutureWarning,
            module="torch.nn.utils.weight_norm",
        )
        warnings.filterwarnings(
            "ignore",
            message=".*dropout option adds dropout.*",
            category=UserWarning,
            module="torch.nn.modules.rnn",
        )

        pipeline = KPipeline(lang_code=lang_code, repo_id="hexgrad/Kokoro-82M")

        def wait_and_generate(idx: int) -> tuple[int, str, torch.Tensor | None]:
            """Wait for chunk file, then generate audio."""
            chunk_file = workdir / f"chunk_{idx}.txt"

            while not chunk_file.exists():
                time.sleep(0.2)
            time.sleep(0.05)

            text = chunk_file.read_text().strip()
            if not text:
                return idx, "", None

            audio_parts: list[torch.Tensor] = []
            for _gs, _ps, audio in pipeline(text, voice=voice):
                if isinstance(audio, (torch.Tensor, torch.FloatTensor)):
                    audio_parts.append(audio)

            if audio_parts:
                return idx, text, torch.cat(audio_parts, dim=0).float()
            return idx, text, None

        # pre-generate one chunk ahead while playing current
        with ThreadPoolExecutor(max_workers=1) as executor:
            # kick off first chunk
            next_future: Future[tuple[int, str, torch.Tensor | None]] | None = executor.submit(wait_and_generate, 1)

            for idx in range(1, total + 1):
                # get current chunk result
                current_idx, text, audio = next_future.result()

                # immediately start generating next chunk
                if idx < total:
                    next_future = executor.submit(wait_and_generate, idx + 1)

                if audio is not None:
                    print(f"[{current_idx}/{total}] {text[:80]}...")
                    sd.play(audio, sr, blocking=True)


if __name__ == "__main__":
    run()
