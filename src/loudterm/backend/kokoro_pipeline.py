import time

import torch

from loudterm.audio.player import AudioPlayer
from loudterm.audio.writer import AudioWriter
from loudterm.backend.kokoro import KokoroGenerator
from loudterm.config import AppConfig
from loudterm.core import AudioResult
from loudterm.ui.prints import print_error, print_info, print_success


def kokoro_blocking_pipeline(
    text: str,
    app_config: AppConfig,
    generator: KokoroGenerator,
) -> None:
    """Synchronous pipeline to run on worker thread."""
    audio_player: AudioPlayer | None = AudioPlayer() if app_config.auto_play else None
    audio_writer: AudioWriter | None = AudioWriter() if app_config.auto_save else None

    all_audio_chunks: list[torch.Tensor] = []
    sample_rate: int | None = None

    print_info(f"Processing {len(text)} chars...")

    try:
        audio_stream = generator.generate(
            text=text,
            voice=app_config.voice or "af_heart",
            speed=app_config.speed,
        )

        for i, audio_result in enumerate(audio_stream, start=1):
            if sample_rate is None:
                sample_rate = audio_result.sample_rate

            if audio_player is not None:
                print_info(f"> [Chunk {i}] Playing...")
                audio_player.play(audio_result)

            if audio_writer is not None:
                all_audio_chunks.append(audio_result.samples)

        print()

    except Exception:  # noqa: BLE001
        print_error("Error during generation. Check logs for details.\n")
        return

    if audio_writer is not None and all_audio_chunks and sample_rate is not None:
        final_samples = torch.cat(all_audio_chunks, dim=0).float()

        final_result = AudioResult(
            samples=final_samples,
            sample_rate=sample_rate,
        )

        filename = f"output_{int(time.time())}.wav"
        output_path = app_config.output_dir / filename

        print_success(f"Saving to {output_path}...")
        audio_writer.save(final_result, output_path)
        print_success("Done.\n")


def load_kokoro_generator(app_config: AppConfig) -> KokoroGenerator | None:
    try:
        generator = KokoroGenerator(lang_code=app_config.lang)
        print_success("Engine ready!\n")
    except Exception as e:  # noqa: BLE001
        print_error(f"Failed to initialize Kokoro engine: {e}\n")
        return None
    else:
        return generator
