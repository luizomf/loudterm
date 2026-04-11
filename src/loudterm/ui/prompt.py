from prompt_toolkit import PromptSession, print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.history import FileHistory
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.styles import Style

from loudterm.backend.kokoro82m.voices import KOKORO_VOICES
from loudterm.config import OUTPUT_DIR, AppConfig
from loudterm.ui.completer import LoudTermCompleter
from loudterm.ui.key_bindings import make_key_bindings
from loudterm.ui.styles import STYLES

primary = STYLES.get_color("primary").hex


def make_style() -> Style:
    return Style.from_dict(
        {
            "bottom-toolbar": (f"fg:black bg:{primary} noreverse"),
        },
    )


def make_bootom_toolbar(app_config: AppConfig) -> FormattedText:
    voice_data = KOKORO_VOICES["@" + app_config.voice]
    return FormattedText(
        [
            (f"fg:black bg:{primary}", " Save: "),
            (f"bg:black fg:{primary}", f" {app_config.auto_save} "),
            (f"fg:black bg:{primary}", " | "),
            (f"fg:black bg:{primary}", " Play: "),
            (f"bg:black fg:{primary}", f" {app_config.auto_play} "),
            (f"fg:black bg:{primary}", " | "),
            (f"fg:black bg:{primary}", " Device: "),
            (f"bg:black fg:{primary}", f" @{app_config.device} "),
            (f"fg:black bg:{primary}", " | "),
            (f"fg:black bg:{primary}", " Voice: "),
            (f"bg:black fg:{primary}", f" @{app_config.voice} "),
            (f"bg:black fg:{primary}", f"{voice_data['desc']} "),
        ],
    )


async def get_input(app_config: AppConfig) -> str | None:
    history = FileHistory(OUTPUT_DIR / "text_history.txt")

    session: PromptSession[str] = PromptSession(
        completer=LoudTermCompleter(),
        complete_while_typing=True,
        key_bindings=make_key_bindings(app_config),
        history=history,
        enable_history_search=False,
    )

    with patch_stdout():
        primary_clr_hex = STYLES.get_color("primary").hex

        prompt_txt = FormattedText(
            [
                ("fg:white", "loud"),
                (f"fg:{primary_clr_hex}", "term"),
                ("dim", " >"),
            ],
        )
        print_formatted_text(prompt_txt)
        text = await session.prompt_async(
            multiline=True,
            placeholder=FormattedText(
                [("dim italic", "Type or paste your text here...")],
            ),
            editing_mode=app_config.editing_mode,
            refresh_interval=1,
            bottom_toolbar=lambda: make_bootom_toolbar(app_config),
            style=make_style(),
        )

    print()

    return text
