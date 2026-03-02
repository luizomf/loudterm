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
        choices=["a", "p"],
        default="a",
        help="The language",
    )

    args = parser.parse_args()
    text = args.text

    if args.stdin and isinstance(args.stdin, io.TextIOBase):
        text = args.stdin.read()
        args.stdin.close()

    if not text:
        print("Error: text missing. Use --help to see options.")
        sys.exit(1)

    run_pipeline(args.language, text)


def run_pipeline(lang_code: str, text: str) -> None:
    sr = 24000  # sample rate

    langs = {
        "a": "af_heart",
        "p": "pf_dora",
    }

    voice = langs[lang_code]

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
        generator = pipeline(text, voice=voice)

        for i, (_gs, _ps, audio) in enumerate(generator):
            if not isinstance(audio, (torch.Tensor, torch.FloatTensor)):
                continue

            # print(_gs)
            # print("-" * 80)
            # print(_ps)

            audio_parts.append(audio)
            output_file = OUTPUT_DIR / f"{voice}_{filename_ts}_part{i}.wav"
            sf.write(output_file, audio, sr)  # type: ignore[reportUnknownMemberType]

            sd.play(audio, sr, blocking=True)  # type: ignore[reportUnknownMemberType]

            # print("-" * 80)

    if audio_parts:
        final_audio = torch.cat(audio_parts, dim=0).float()
        output_file = OUTPUT_DIR / f"{voice}_{filename_ts}_full.wav"
        sf.write(output_file, final_audio, sr)  # type: ignore[reportUnknownMemberType]


if __name__ == "__main__":
    run()
