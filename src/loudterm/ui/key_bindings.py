from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent

from loudterm.config import AppConfig


def make_key_bindings(app_config: AppConfig) -> KeyBindings:
    key_bindings = KeyBindings()

    @key_bindings.add("c-s")
    def _(_: KeyPressEvent) -> None:
        app_config.auto_save = not app_config.auto_save

    @key_bindings.add("c-p")
    def _(_: KeyPressEvent) -> None:
        app_config.auto_play = not app_config.auto_play

    return key_bindings
