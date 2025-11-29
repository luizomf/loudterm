from concurrent.futures import ThreadPoolExecutor

from loudterm.backend.kokoro import KokoroGenerator
from loudterm.backend.kokoro_process_input import kokoro_process_input
from loudterm.config import AppConfig
from loudterm.ui.prints import print_error, print_exit, print_success
from loudterm.ui.process_commands import process_commands
from loudterm.ui.prompt import get_input


async def main_loop(
    app_config: AppConfig,
    generator: KokoroGenerator,
    executor: ThreadPoolExecutor,
) -> None:
    while True:
        try:
            text = await get_input(app_config)

            if text is None:
                print_exit()
                break

            text = text.strip()

            control = await process_commands(text, app_config, generator)

            if isinstance(control.data, KokoroGenerator):
                # Reload generator with new voice
                generator = control.data

            if control.loop_action == "continue":
                continue
            if control.loop_action == "break":
                break

            await kokoro_process_input(text, executor, app_config, generator)

        except KeyboardInterrupt:
            print_success("Exiting...\n")
            break
        except EOFError:
            break
        except Exception as e:  # noqa: BLE001
            print_error(f"Error: {e}\n")


async def run_worker(config: AppConfig, generator: KokoroGenerator) -> None:
    with ThreadPoolExecutor(max_workers=1) as executor:
        await main_loop(config, generator, executor)
