import asyncio
import sys
from typing import Optional

from loudterm.config import load_config
from loudterm.ui.run_repl import run_repl


def main() -> None:
    
    device: Optional[str] = None
    for arg in sys.argv[1:]:
        if arg.startswith("device="):
            device = arg.split("=", 1)[1]

    config = load_config(lang="p", voice="pf_dora", device=device)

    try:
        asyncio.run(run_repl(config))
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
