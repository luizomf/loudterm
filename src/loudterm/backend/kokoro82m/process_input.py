import asyncio
from concurrent.futures import ThreadPoolExecutor

from loudterm.backend.kokoro82m.generator import KokoroGenerator
from loudterm.backend.kokoro82m.pipeline import kokoro_blocking_pipeline
from loudterm.config import AppConfig


async def kokoro_process_input(
    text: str,
    executor: ThreadPoolExecutor,
    app_config: AppConfig,
    kokoro_generator: KokoroGenerator,
) -> None:
    """
    Handles the user input in a separate thread to avoid blocking the event loop.
    """
    loop = asyncio.get_running_loop()

    await loop.run_in_executor(
        executor,
        kokoro_blocking_pipeline,
        text,
        app_config,
        kokoro_generator,
    )
