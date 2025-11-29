from loudterm.backend.kokoro_pipeline import (
    load_kokoro_generator,
)
from loudterm.config import AppConfig
from loudterm.ui.loop import run_worker
from loudterm.ui.prints import (
    print_description,
    print_header,
)


async def run_repl(app_config: AppConfig) -> None:
    """Runs the main REPL loop."""
    print_header()
    print_description()

    kokoro_generator = load_kokoro_generator(app_config)

    if kokoro_generator:
        await run_worker(app_config, kokoro_generator)
