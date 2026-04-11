from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from prompt_toolkit.enums import EditingMode

ROOT_DIR = Path(__file__).parent.parent.parent
OUTPUT_DIR = ROOT_DIR / "output"


@dataclass(slots=True)
class AppConfig:
    voice: str = "af_heart"
    lang: str = "a"
    speed: float = 1.0
    output_dir: Path = OUTPUT_DIR
    auto_save: bool = True
    auto_play: bool = True
    editing_mode: EditingMode = EditingMode.VI
    device: Optional[str] = None


def load_config(  # noqa: PLR0913
    voice: str,
    lang: str,
    *,
    output_dir: Path | None = None,
    speed: float = 1.0,
    auto_save: bool = True,
    auto_play: bool = True,
    editing_mode: EditingMode = EditingMode.VI,
    device: Optional[str] = None,
) -> AppConfig:
    return AppConfig(
        voice=voice,
        lang=lang,
        output_dir=output_dir or OUTPUT_DIR,
        speed=speed,
        auto_save=auto_save,
        auto_play=auto_play,
        editing_mode=editing_mode,
        device=device,
    )
