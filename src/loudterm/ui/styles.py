from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Literal

CSI = "\x1b["
FG256 = f"{CSI}38;5;"
BG256 = f"{CSI}48;5;"
RESET_ALL = f"{CSI}0m"


type AvailableStyles = Literal[
    "bg",
    "fg",
    "bold",
    "dim",
    "italic",
    "underline",
    "blinking",
    "inverse",
    "hidden",
    "strike",
]

type AvailableColors = Literal[
    "bg",
    "surface",
    "surface_alt",
    "border",
    "text",
    "text_muted",
    "primary",
    "primary_soft",
    "primary_strong",
    "success",
    "warning",
    "danger",
    "info",
    "neutral0",
    "neutral1",
    "neutral2",
    "neutral3",
    "neutral4",
]


def ansi_fg(index: int) -> str:
    return f"{CSI}38;5;{index}m"


def ansi_bg(index: int) -> str:
    return f"{CSI}48;5;{index}m"


def ansi(parameters: str, csi: str = CSI) -> str:
    return f"{csi}{parameters}"


@dataclass(frozen=True)
class Color:
    hex: str  # Ex.: "#00bcd4"
    xterm: int  # Ex.: 0-255

    def ansi_fg(self) -> str:
        return f"{CSI}38;5;{self.xterm}m"

    def ansi_bg(self) -> str:
        return f"{CSI}48;5;{self.xterm}m"


@dataclass(kw_only=True, frozen=True, slots=True)
class ThemeColors:
    bg: Color = field(default_factory=lambda: Color("#000000", 0))
    surface: Color = field(default_factory=lambda: Color("#080808", 232))
    surface_alt: Color = field(
        default_factory=lambda: Color("#121212", 233),
    )
    border: Color = field(default_factory=lambda: Color("#5f5f5f", 59))
    text: Color = field(default_factory=lambda: Color("#ffffff", 15))
    text_muted: Color = field(
        default_factory=lambda: Color("#878787", 102),
    )
    primary: Color = field(default_factory=lambda: Color("#87ff87", 120))
    primary_soft: Color = field(
        default_factory=lambda: Color("#87ffaf", 121),
    )
    primary_strong: Color = field(
        default_factory=lambda: Color("#00ff87", 48),
    )
    success: Color = field(default_factory=lambda: Color("#00ffaf", 49))
    warning: Color = field(default_factory=lambda: Color("#ffff5f", 227))
    danger: Color = field(default_factory=lambda: Color("#ff5f5f", 203))
    info: Color = field(default_factory=lambda: Color("#00afff", 39))
    neutral0: Color = field(default_factory=lambda: Color("#1c1c1c", 234))
    neutral1: Color = field(default_factory=lambda: Color("#5f5f5f", 59))
    neutral2: Color = field(default_factory=lambda: Color("#878787", 102))
    neutral3: Color = field(default_factory=lambda: Color("#afafaf", 145))
    neutral4: Color = field(default_factory=lambda: Color("#afd7d7", 152))


class TextStyles:
    def __init__(self, theme_colors: ThemeColors | None = None) -> None:
        self.theme = theme_colors or ThemeColors()

    def bg(self, color: AvailableColors = "bg") -> str:
        return getattr(self.theme, color).ansi_bg()

    def fg(self, color: AvailableColors = "text") -> str:
        return getattr(self.theme, color).ansi_fg()

    def reset(self) -> str:
        return RESET_ALL

    def bold(self) -> str:
        return ansi("1m")

    def dim(self) -> str:
        return ansi("2m")

    def italic(self) -> str:
        return ansi("3m")

    def underline(self) -> str:
        return ansi("4m")

    def blinking(self) -> str:
        return ansi("5m")

    def inverse(self) -> str:
        return ansi("7m")

    def hidden(self) -> str:
        return ansi("8m")

    def strike(self) -> str:
        return ansi("9m")

    def apply(self, text: str, styles: Sequence[AvailableStyles]) -> str:
        parsed_styles = "".join([getattr(self, s)() for s in styles])
        return f"{self.reset()}{parsed_styles}{text}{self.reset()}"

    def get_color(self, color: AvailableColors) -> Color:
        return getattr(self.theme, color)


STYLES = TextStyles()

if __name__ == "__main__":
    pass
