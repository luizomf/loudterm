import asyncio
from typing import TYPE_CHECKING

from prompt_toolkit.application import create_app_session
from prompt_toolkit.enums import EditingMode
from prompt_toolkit.input import create_pipe_input
from prompt_toolkit.output import DummyOutput

from loudterm.config import AppConfig
from loudterm.ui import prompt

if TYPE_CHECKING:
    from pathlib import Path

    import pytest


def test_first_submission_persists_history_without_audio(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    output_dir = tmp_path / "output"
    monkeypatch.setattr(prompt, "OUTPUT_DIR", output_dir)
    config = AppConfig(auto_save=False, editing_mode=EditingMode.EMACS)

    async def submit(text: str) -> str | None:
        with (
            create_pipe_input() as pipe,
            create_app_session(input=pipe, output=DummyOutput()),
        ):
            pipe.send_text(text + "\x1b\r")
            return await asyncio.wait_for(prompt.get_input(config), timeout=3)

    assert asyncio.run(submit("first submission")) == "first submission"
    assert "first submission" in (output_dir / "text_history.txt").read_text()
    assert asyncio.run(submit("second submission")) == "second submission"
    history = (output_dir / "text_history.txt").read_text()
    assert "first submission" in history
    assert "second submission" in history
