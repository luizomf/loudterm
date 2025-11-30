from loudterm.backend.kokoro82m.pipeline import (
    load_kokoro_generator,
)
from loudterm.config import AppConfig
from loudterm.ui.loop import run_worker
from loudterm.ui.prints import (
    print_description,
    print_error,
    print_header,
)


async def run_repl(app_config: AppConfig) -> None:
    """Runs the main REPL loop."""
    print_header()
    print_description()

    try:
        kokoro_generator = load_kokoro_generator(app_config)
    except Exception as e:  # noqa: BLE001
        print_error("Failed to load kokoro:", e)
    else:
        await run_worker(app_config, kokoro_generator)
