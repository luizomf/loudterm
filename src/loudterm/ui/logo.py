from loudterm.ui.styles import Styles

LOGO: tuple[tuple[str, str], ...] = (
    ("▄                     ▄", "                       "),
    ("█     █▀▀▀█ █   █ █▀▀▀█", "▀▀█▀▀ █▀▀▀█ █▀▀▀█ █▀█▀▄"),
    ("█     █   █ █   █ █   █", "  █   █▀▀▀▀ █▀▀█▀ █ █ █"),
    ("▀▀▀▀▀ ▀▀▀▀▀ ▀▀▀▀  ▀▀▀▀▀", "  ▀   ▀▀▀▀▀ ▀  ▀  ▀ ▀ ▀"),
)
NEW_LINE = "\n"
PAD_CHAR = " "
LOGO_WIDTH = len(LOGO[0][0]) * 2
EMPTY_LINE = LOGO_WIDTH * PAD_CHAR


def build_logo(
    *,
    fg: tuple[str, str] = (Styles.light_fg, Styles.primary_fg),
    bg: tuple[str, str] = ("", ""),
    pad_x: tuple[int, int, int, int] = (2, 1, 1, 2),
    pad_y: tuple[int, int] = (1, 1),
) -> str:
    """Build loudterm logo with padding and color options.

    Args:
        fg: The ANSI foreground colors for "loud" and "term" as a tuple.
        bg: The ANSI background colors for "loud" and "term" as a tuple.
        pad_x: Number of spaces for "loud" and "term" left and right (four ints)
        pad_y: Number of lines for top and bottom as a tuple (two ints)

    Returns:
        The logo string.
    """
    output: list[str] = []
    x1, x2, x3, x4 = pad_x
    y1, y2 = pad_y

    pad_left1 = x1 * PAD_CHAR
    pad_right1 = x2 * PAD_CHAR
    pad_left2 = x3 * PAD_CHAR
    pad_right2 = x4 * PAD_CHAR

    fg_left, fg_right = fg
    bg_left, bg_right = bg

    reset = Styles.reset

    if y1 > 0:
        output.append(y1 * "\n")

    for line in LOGO:
        output.append(reset)
        output.extend([bg_left, fg_left, pad_left1, line[0], pad_right1])
        output.append(reset)
        output.extend([bg_right, fg_right, pad_left2, line[1], pad_right2])
        output.append(reset)
        output.append(NEW_LINE)

    if y2 > 0:
        output.append(y2 * "\n")

    return "".join(output)


if __name__ == "__main__":
    original_logo = build_logo()
    print(original_logo, end="")
    changed_logo = build_logo(
        bg=(Styles.dark_bg, Styles.light_bg),
        fg=(Styles.light_fg, Styles.dark_fg),
        pad_x=(2, 2, 2, 2),
        pad_y=(1, 1),
    )
    print(changed_logo, end="")
