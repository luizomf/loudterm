from loudterm.ui.logo import build_logo
from loudterm.ui.styles import STYLES

styles = STYLES


def to_str(*values: object, sep: str = " ") -> str:
    return sep.join(map(str, values))


def print_(
    *values: object,
    end: str = "\n",
    sep: str = " ",
    flush: bool = True,
) -> None:
    print(*values, end=end, sep=sep, flush=flush)


def print_info(
    *values: object,
    end: str = "\n",
    sep: str = " ",
    flush: bool = True,
) -> None:
    tag_clrs = STYLES.fg("info")
    tag = STYLES.apply(f"{tag_clrs}INFO:", ["bold"])
    text = STYLES.apply(to_str(*values), ["dim", "italic"])
    print_(tag, text, end=end, sep=sep, flush=flush)


def print_warning(
    *values: object,
    end: str = "\n",
    sep: str = " ",
    flush: bool = True,
) -> None:
    tag_clrs = STYLES.fg("warning")
    tag = STYLES.apply(f"{tag_clrs}WARNING:", ["bold"])
    text_clrs = STYLES.fg("warning")
    text = STYLES.apply(f"{text_clrs}{to_str(*values)}", ["italic"])
    print_(tag, text, end=end, sep=sep, flush=flush)


def print_error(
    *values: object,
    end: str = "\n",
    sep: str = " ",
    flush: bool = True,
) -> None:
    tag_clrs = STYLES.fg("danger")
    tag = STYLES.apply(f"{tag_clrs}ERROR:", ["bold"])
    text_clrs = STYLES.fg("danger")
    text = STYLES.apply(f"{text_clrs}{to_str(*values)}", ["italic"])
    print_(tag, text, end=end, sep=sep, flush=flush)


def print_success(
    *values: object,
    end: str = "\n",
    sep: str = " ",
    flush: bool = True,
) -> None:
    tag_clrs = STYLES.fg("success")
    tag = STYLES.apply(f"{tag_clrs}SUCCESS:", ["bold"])
    text_clrs = STYLES.fg("success")
    text = STYLES.apply(f"{text_clrs}{to_str(*values)}", ["italic"])
    print_(tag, text, end=end, sep=sep, flush=flush)


def print_primary(
    *values: object,
    end: str = "\n",
    sep: str = " ",
    flush: bool = True,
) -> None:
    text_clrs = STYLES.fg("primary")
    text = STYLES.apply(f"{text_clrs}{to_str(*values)}", [])
    print_(text, end=end, sep=sep, flush=flush)


def print_primary_inv(
    *values: object,
    end: str = "\n",
    sep: str = " ",
    flush: bool = True,
) -> None:
    text_clrs = STYLES.fg("primary")
    text = STYLES.apply(f"{text_clrs}{to_str(*values)}", ["inverse"])
    print_(text, end=end, sep=sep, flush=flush)


def print_dim(
    *values: object,
    end: str = "\n",
    sep: str = " ",
    flush: bool = True,
) -> None:
    text = STYLES.apply(f"{to_str(*values)}", ["dim"])
    print_(text, end=end, sep=sep, flush=flush)


def print_text(
    *values: object,
    end: str = "\n",
    sep: str = " ",
    flush: bool = True,
) -> None:
    print_(*values, end=end, sep=sep, flush=flush)


if __name__ == "__main__":
    text = "This is an example text"

    print(build_logo())
    print_primary(text)
    print_info("Hello world", 123, 456)
    print_info(f"Processing {len(text)} chars...", 123, 456)
    print_warning("Hello world", 123, 456)
    print_info("Hello world", 123, 456)
    print_info(f"Processing {len(text)} chars...", 123, 456)
    print_info("Hello world", 123, 456)
    print_info(f"Processing {len(text)} chars...", 123, 456)
    print_warning("Hello world", 123, 456)
    print_info("Hello world", 123, 456)
    print_error(f"Processing {len(text)} chars...", 123, 456)
    print_success("Hello world", 123, 456)
    print_info(f"Processing {len(text)} chars...", 123, 456)
    print_warning("Hello world", 123, 456)
    print_info("Hello world", 123, 456)
    print_info(f"Processing {len(text)} chars...", 123, 456)
    print_info("Hello world", 123, 456)
    print_info(f"Processing {len(text)} chars...", 123, 456)
    print_warning("Hello world", 123, 456)
    print_info("Hello world", 123, 456)
    print_info(f"Processing {len(text)} chars...", 123, 456)
    print_info("Hello world", 123, 456)
    print_info(f"Processing {len(text)} chars...", 123, 456)
    print_warning("Hello world", 123, 456)
    print_info("Hello world", 123, 456)
    print_error(f"Processing {len(text)} chars...", 123, 456)
    print_info("Hello world", 123, 456)
    print_info(f"Processing {len(text)} chars...", 123, 456)
    print_warning("Hello world", 123, 456)
    print_info("Hello world", 123, 456)
    print_info(f"Processing {len(text)} chars...", 123, 456)
