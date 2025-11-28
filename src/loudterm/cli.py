import asyncio
import sys

from loudterm.config import load_config
from loudterm.ui.run_repl import run_repl


def main() -> None:
    config = load_config(lang="p", voice="pf_dora")

    try:
        asyncio.run(run_repl(config))
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
