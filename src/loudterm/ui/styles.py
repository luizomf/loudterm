CSI = "\x1b["
FG256 = f"{CSI}38;5;"
BG256 = f"{CSI}48;5;"
RESET_ALL = f"{CSI}0m"


class Colors:
    black = "0m"
    white = "15m"
    primary = "120m"
    grey = "245m"


class Styles:
    light_fg = f"{FG256}{Colors.white}"
    dark_fg = f"{FG256}{Colors.black}"

    light_bg = f"{BG256}{Colors.white}"
    dark_bg = f"{BG256}{Colors.black}"

    primary_fg = f"{FG256}{Colors.primary}"
    primary_bg = f"{BG256}{Colors.primary}{FG256}{Colors.black}"

    dim = f"{CSI}2m"

    reset = RESET_ALL


if __name__ == "__main__":
    print(Styles.primary_fg, "Hello world", Styles.reset, " Nice ", sep="")
    print(Styles.primary_bg, "Hello world", Styles.reset, " Nice ", sep="")
