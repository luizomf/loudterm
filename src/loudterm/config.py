from dataclasses import dataclass
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent
OUTPUT_DIR = ROOT_DIR / "output"


@dataclass(slots=True)
class AppConfig:
    engine: str = "kokoro"
    voice: str | None = None
    lang: str | None = None
    speed: float = 1.0
    output_dir: Path = OUTPUT_DIR
    auto_save: bool = True


def load_config() -> AppConfig:
    return AppConfig()
