# ruff: noqa: SIM102
import asyncio
import logging
import time
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from prompt_toolkit import PromptSession, print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.shortcuts import clear

from loudterm.audio.player import AudioPlayer
from loudterm.audio.writer import AudioWriter
from loudterm.backend.kokoro import KokoroGenerator
from loudterm.backend.kokoro_voices import VOICES
from loudterm.config import AppConfig
from loudterm.core import AudioResult
from loudterm.ui.completer import LoudTermCompleter
from loudterm.ui.logo import build_logo
from loudterm.ui.prints import (
    print_dim,
    print_error,
    print_info,
    print_primary,
    print_success,
    print_text,
)
from loudterm.ui.styles import STYLES

logger = logging.getLogger(__name__)


def blocking_pipeline(
    text: str,
    config: AppConfig,
    generator: KokoroGenerator,
) -> None:
    """
    The synchronous pipeline that runs in a worker thread.
    It handles Chunking > Generation > Playback > Saving.
    """
    player = AudioPlayer()
    writer = AudioWriter()

    # Buffer to store all chunks for the final file
    full_audio_chunks: list[np.ndarray] = []
    sample_rate = 24000  # Kokoro default

    print_info(f"Processing {len(text)} chars...")

    # Use Kokoro's internal generator which handles splitting
    try:
        audio_stream = generator.generate(
            text,
            voice=config.voice or "af_heart",
            speed=config.speed,
        )

        for i, audio_result in enumerate(audio_stream):
            print_info(f"> [Chunk {i + 1}] Playing...")

            # Play Stream
            player.play(audio_result)

            # Accumulate for saving
            full_audio_chunks.append(audio_result.samples)
        print()

    except Exception:
        logger.exception("Error during generation")
        print_error("Error during generation. Check logs for details.\n")
        return

    # Save Final Result
    if full_audio_chunks and config.auto_save:
        final_samples = np.concatenate(full_audio_chunks)
        final_result = AudioResult(samples=final_samples, sample_rate=sample_rate)

        filename = f"output_{int(time.time())}.wav"
        output_path = config.output_dir / filename

        print_success(f"Saving to {output_path}...")
        writer.save(final_result, output_path)
        print_success("Done.\n")


async def process_input(
    text: str,
    executor: ThreadPoolExecutor,
    config: AppConfig,
    generator: KokoroGenerator,
) -> None:
    """
    Handles the user input in a separate thread to avoid blocking the event loop.
    """
    loop = asyncio.get_running_loop()
    # Run the blocking pipeline in the thread pool
    await loop.run_in_executor(executor, blocking_pipeline, text, config, generator)


async def run_repl(config: AppConfig) -> None:
    """Runs the main REPL loop."""
    clear()
    print(build_logo(), end="", flush=True)
    print_dim(
        "Initializing Kokoro engine (this may take a moment to download weights)...",
    )
    print()

    # Initialize Kokoro once
    try:
        # Map config lang to Kokoro lang code if needed, defaulting to 'a' (en-us)
        lang_code = config.lang if config.lang else "a"
        generator = KokoroGenerator(lang_code=lang_code)
        print_success("Engine ready!\n")
    except Exception as e:  # noqa: BLE001
        print_error(f"Failed to initialize Kokoro engine: {e}\n")
        return

    print_primary(
        "Type your text and press [Meta+Enter] or [Esc] then [Enter] to submit.",
    )
    print_dim("Commands: Type '@' to see options for voice/language.")
    print_text("Press [Ctrl+C] or /exit [Meta+Enter] to exit.\n")

    session: PromptSession[str] = PromptSession(
        completer=LoudTermCompleter(),
        complete_while_typing=True,
    )

    # Create a thread pool for audio operations
    # We use a thread pool because sounddevice/soundfile are blocking I/O
    # and numpy/TTS generation might be CPU heavy but release GIL often.
    with ThreadPoolExecutor(max_workers=2) as executor:
        while True:
            try:
                with patch_stdout():
                    primary_clr_hex = STYLES.get_color("primary").hex

                    prompt_txt = FormattedText(
                        [
                            ("fg:white", "loud"),
                            (f"fg:{primary_clr_hex}", "term"),
                            ("dim", " >"),
                        ],
                    )
                    print_formatted_text(prompt_txt)
                    text = await session.prompt_async(
                        multiline=True,
                        placeholder=FormattedText(
                            [("dim italic", "Type or paste your text here...")],
                        ),
                    )

                print()
                text = text.strip()
                if not text:
                    print_error("Not text found\n")
                    continue

                # Handle Configuration Commands
                if text.startswith(("@", "/")):
                    cmd = text.lower()

                    if cmd.startswith("@"):
                        # Handle Language Change
                        if cmd in VOICES:
                            new_lang_data = VOICES[cmd]
                            lang_code = new_lang_data["language_code"]
                            desc = new_lang_data["desc"]

                            print_dim(f"Voice changed to: {cmd[1:]}...")
                            print_dim(f"Switching language to {desc}...\n")

                            config.voice = cmd[1:]
                            config.lang = lang_code

                            # Re-initialize generator
                            try:
                                generator = KokoroGenerator(lang_code=lang_code)
                                print_success("Engine reloaded successfully!\n")
                            except Exception as e:  # noqa: BLE001
                                print_success(f"Error reloading engine: {e}\n")
                            continue

                    if cmd.startswith("/"):
                        if text.lower().strip() in ("/exit", "/quit", "/q", "/bye"):
                            print_success("Exiting...\n")
                            break

                    print_error(f"Unknown command: {text}\n")
                    continue

                # Offload processing to avoid freezing the UI
                await process_input(text, executor, config, generator)

            except KeyboardInterrupt:
                print_success("Exiting...\n")
                break
            except EOFError:
                break
            except Exception as e:
                logger.exception("An error occurred during REPL execution")
                print_error(f"Error: {e}\n")
