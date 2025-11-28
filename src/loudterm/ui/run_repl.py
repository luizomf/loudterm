import asyncio
import builtins
import logging
import time
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from prompt_toolkit import HTML, PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

from loudterm.audio.player import AudioPlayer
from loudterm.audio.writer import AudioWriter
from loudterm.backend.kokoro import KokoroGenerator
from loudterm.config import AppConfig
from loudterm.core import AudioResult
from loudterm.ui.completer import VOICES, LoudTermCompleter
from loudterm.ui.logo import build_logo
from loudterm.ui.styles import Styles

logger = logging.getLogger(__name__)


def print(*values: object) -> None:  # noqa: A001
    builtins.print(Styles.dim, *values, Styles.reset, sep="")


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

    print(f"Processing {len(text)} chars...")

    # Use Kokoro's internal generator which handles splitting
    try:
        audio_stream = generator.generate(
            text,
            voice=config.voice or "af_heart",
            speed=config.speed,
        )

        for i, audio_result in enumerate(audio_stream):
            print(f"  [Chunk {i + 1}] Playing...")

            # Play Stream
            player.play(audio_result)

            # Accumulate for saving
            full_audio_chunks.append(audio_result.samples)

    except Exception:
        logger.exception("Error during generation")
        print("Error during generation. Check logs for details.")
        return

    # Save Final Result
    if full_audio_chunks and config.auto_save:
        final_samples = np.concatenate(full_audio_chunks)
        final_result = AudioResult(samples=final_samples, sample_rate=sample_rate)

        filename = f"output_{int(time.time())}.wav"
        output_path = config.output_dir / filename

        print(f"Saving to {output_path}...")
        writer.save(final_result, output_path)
        print("Done.")


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
    print(build_logo())
    print("Initializing Kokoro engine (this may take a moment to download weights)...")

    # Initialize Kokoro once
    try:
        # Map config lang to Kokoro lang code if needed, defaulting to 'a' (en-us)
        lang_code = config.lang if config.lang else "a"
        generator = KokoroGenerator(lang_code=lang_code)
        print("Engine ready!")
    except Exception as e:  # noqa: BLE001
        print(f"Failed to initialize Kokoro engine: {e}")
        return

    print("\nType your text and press [Meta+Enter] or [Esc] then [Enter] to submit.")
    print("Commands: Type '@' to see options for voice/language.")
    print("Press [Ctrl+C] or /exit [Meta+Enter] to exit.\n")

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
                    text = await session.prompt_async(
                        HTML("<St fg='#87ff87'>loudterm</St> <St>></St> "),
                        multiline=True,
                    )

                text = text.strip()
                if not text:
                    continue

                # Handle Configuration Commands
                if text.startswith("@"):
                    cmd = text.lower()

                    # Handle Language Change
                    if cmd in VOICES:
                        new_lang_data = VOICES[cmd]
                        lang_code = new_lang_data["language_code"]
                        desc = new_lang_data["desc"]

                        print(f"Voice changed to: {cmd[1:]}...")
                        print(f"Switching language to {desc}...")

                        config.voice = cmd[1:]
                        config.lang = lang_code

                        # Re-initialize generator
                        try:
                            generator = KokoroGenerator(lang_code=lang_code)
                            print("Engine reloaded successfully!")
                        except Exception as e:  # noqa: BLE001
                            print(f"Error reloading engine: {e}")
                        continue

                    # Handle Voice Change
                    if cmd in VOICES:
                        voice_name = cmd[1:]  # remove @
                        config.voice = voice_name
                        print(f"Voice changed to: {VOICES[cmd]}")
                        continue

                    print(f"Unknown command: {text}")
                    continue

                if text.lower().strip() in ("/exit", "/quit", "/q", "/bye"):
                    break

                # Offload processing to avoid freezing the UI
                await process_input(text, executor, config, generator)

            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except EOFError:
                break
            except Exception as e:
                logger.exception("An error occurred during REPL execution")
                print(f"Error: {e}")
