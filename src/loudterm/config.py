from dataclasses import dataclass
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent
OUTPUT_DIR = ROOT_DIR / "output"


@dataclass(slots=True)
class AppConfig:
    voice: str | None = None
    lang: str | None = None
    speed: float = 1.0
    output_dir: Path = OUTPUT_DIR
    auto_save: bool = True


def load_config(
    voice: str,
    lang: str,
    *,
    output_dir: Path | None = None,
    speed: float = 1.0,
    auto_save: bool = True,
) -> AppConfig:
    return AppConfig(
        voice=voice,
        lang=lang,
        output_dir=output_dir or OUTPUT_DIR,
        speed=speed,
        auto_save=auto_save,
    )
