# ruff: noqa: ERA001
import argparse
import io
import sys
import textwrap
import time
import warnings

import sounddevice as sd
import soundfile as sf
import torch
from kokoro import KPipeline

from loudterm.config import OUTPUT_DIR


def run() -> None:
    parser = argparse.ArgumentParser(
        "cliplay",
        description=textwrap.dedent("""
            Use this to play and save audio from text.
        """),
        epilog=textwrap.dedent("""
            Examples:

            # American English
            cliplay -t "This text will produce an audio file and play it."

            # American English
            cliplay -l "a" -t "This text will produce an audio file and play it."

            # Brazilian Portuguese
            cliplay -l "p" -t "Este texto vai produzir um arquivo de áudio e tocar."

            # STDIN - American English
            cliplay -i - "This text will produce an audio file and play it."

            # STDIN - American English
            echo "This text will produce an audio." | cliplay -l "a" --stdin -

            # STDIN - Brazilian Portuguese
            echo "Este texto vai produzir um arquivo de áudio." | cliplay -l "p" -i -
        """),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-t",
        "--text",
        nargs="?",
        required=False,
        metavar="TEXT",
        help="Text to generate audio.",
    )

    parser.add_argument(
        "-i",
        "--stdin",
        type=argparse.FileType("r"),
        nargs="?",
        required=False,
        default=None,
        metavar="STDIN",
        help="Text to generate audio from stdin.",
    )

    parser.add_argument(
        "-l",
        "--language",
        help="The language code (e.g., 'a' for American English, 'p' for Portuguese).",
    )

    parser.add_argument(
        "-v",
        "--voice",
        help=(
            "Specific voice to use (e.g., 'af_heart', 'pf_dora'). "
            "You can also mix voices with commas, for example "
            "'pf_dora,pm_alex,af_bella'."
        ),
    )

    parser.add_argument(
        "-s",
        "--speed",
        type=float,
        default=1.0,
        help="Speech speed. Lower values usually sound less rushed (e.g., 0.9).",
    )

    parser.add_argument(
        "--show-tokens",
        action="store_true",
        help="Print graphemes and phonemes for each generated chunk.",
    )

    args = parser.parse_args()
    text = args.text

    if args.stdin and isinstance(args.stdin, io.TextIOBase):
        text = args.stdin.read()
        args.stdin.close()

    if not text:
        print("Error: text missing. Use --help to see options.")
        sys.exit(1)

    run_pipeline(args.language, text, args.voice, args.speed, args.show_tokens)


def _normalize_voice_names(voice_name: str) -> list[str]:
    return [part.strip() for part in voice_name.split(",") if part.strip()]


def _resolve_voice_and_lang(
    lang_code: str | None,
    voice_name: str | None,
    available_voices: dict[str, dict[str, str]],
) -> tuple[str, str]:
    default_voices_by_lang = {
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

    if voice_name:
        voice_parts = _normalize_voice_names(voice_name)
        if not voice_parts:
            raise ValueError("Voice list is empty.")

        invalid_voices = [
            part for part in voice_parts if f"@{part}" not in available_voices
        ]
        if invalid_voices:
            invalid = ", ".join(invalid_voices)
            raise ValueError(f"Unknown voice(s): {invalid}")

        if not lang_code:
            lang_code = available_voices[f"@{voice_parts[0]}"]["language_code"]

        return lang_code, ",".join(voice_parts)

    resolved_lang = lang_code or "a"
    return resolved_lang, default_voices_by_lang.get(resolved_lang, "af_heart")


def _iter_chunk_debug(
    show_tokens: bool,
    graphemes: str,
    phonemes: str,
) -> None:
    if not show_tokens:
        return

    print(graphemes)
    print("-" * 80)
    print(phonemes)
    print("-" * 80)


def run_pipeline(
    lang_code: str | None,
    text: str,
    voice_name: str | None = None,
    speed: float = 1.0,
    show_tokens: bool = False,
) -> None:
    from loudterm.backend.kokoro82m.voices import KOKORO_VOICES

    sr = 24000  # sample rate

    if speed <= 0:
        print("Error: speed must be greater than 0.")
        sys.exit(1)

    try:
        lang_code, voice = _resolve_voice_and_lang(
            lang_code=lang_code,
            voice_name=voice_name,
            available_voices=KOKORO_VOICES,
        )
    except ValueError as exc:
        print(f"Error: {exc}")
        sys.exit(1)

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
        filename_ts = f"{time.time():.0f}"

        audio_parts: list[torch.Tensor] = []
        generator = pipeline(text, voice=voice, speed=speed)

        for i, (graphemes, phonemes, audio) in enumerate(generator):
            if not isinstance(audio, (torch.Tensor, torch.FloatTensor)):
                continue

            _iter_chunk_debug(
                show_tokens=show_tokens,
                graphemes=str(graphemes),
                phonemes=str(phonemes),
            )

            audio_parts.append(audio)
            # output_file = OUTPUT_DIR / f"{voice}_{filename_ts}_part{i}.wav"
            # sf.write(output_file, audio, sr)  # type: ignore[reportUnknownMemberType]

            sd.play(audio, sr, blocking=True)  # type: ignore[reportUnknownMemberType]

            # print("-" * 80)

    if audio_parts:
        final_audio = torch.cat(audio_parts, dim=0).float()
        output_file = OUTPUT_DIR / f"{voice}_{filename_ts}_full.wav"
        sf.write(output_file, final_audio, sr)  # type: ignore[reportUnknownMemberType]


if __name__ == "__main__":
    run()
