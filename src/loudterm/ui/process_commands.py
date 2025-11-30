from dataclasses import dataclass
from typing import Any, Literal

from loudterm.backend.kokoro82m.generator import KokoroGenerator
from loudterm.backend.kokoro82m.pipeline import load_kokoro_generator
from loudterm.backend.kokoro82m.voices import KOKORO_VOICES
from loudterm.config import AppConfig
from loudterm.ui.prints import print_dim, print_error, print_exit, print_success


@dataclass(frozen=True, slots=True)
class LoopControl:
    loop_action: Literal["continue", "break", "pass"]
    data: Any


async def process_commands(
    text: str,
    app_config: AppConfig,
    kokoro_generator: KokoroGenerator,
) -> LoopControl:
    min_text_length = 10

    if not text:
        print_error("No text found\n")
        return LoopControl("continue", None)

    command = text.lower()

    if command in KOKORO_VOICES:
        language_data = KOKORO_VOICES[command]
        language_code = language_data["language_code"]
        description = language_data["desc"]

        print_dim(f"Voice changed to: {command[1:]}...")
        print_dim(f"Switching language to {description}...\n")

        app_config.voice = command[1:]
        app_config.lang = language_code

        try:
            new_generator = load_kokoro_generator(app_config)

            if new_generator is None:
                msg = "Failed to load Kokoro."
                raise RuntimeError(msg)

            del kokoro_generator
            kokoro_generator = new_generator

        except Exception as e:  # noqa: BLE001
            print_success(f"Error reloading engine: {e}\n")
        return LoopControl("continue", kokoro_generator)

    if text.lower().strip() in ("/exit", "/quit", "/q", "/bye"):
        print_exit()
        return LoopControl("break", None)

    if len(text) < min_text_length:
        print_error(f"Try {min_text_length} chars or more...\n")
        return LoopControl("continue", None)

    return LoopControl("pass", None)
