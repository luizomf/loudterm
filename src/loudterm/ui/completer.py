from collections.abc import Iterable

from prompt_toolkit.completion import CompleteEvent, Completer, Completion
from prompt_toolkit.document import Document

from loudterm.backend.kokoro_voices import VOICES
from loudterm.ui.commands import COMMANDS


class LoudTermCompleter(Completer):
    def get_completions(
        self,
        document: Document,
        complete_event: CompleteEvent,
    ) -> Iterable[Completion]:
        cmd_chr = "/"
        voice_cmd_chr = "@"
        commands = (cmd_chr, voice_cmd_chr)

        word = document.get_word_before_cursor(WORD=True)

        # Only trigger if the word starts with @
        if not word.startswith(commands):
            return

        if word.startswith(voice_cmd_chr):
            for voice, data in VOICES.items():
                if voice.startswith(word):
                    yield Completion(
                        voice,
                        start_position=-len(word),
                        display=f"{voice} ",
                        display_meta=f"{data['desc']} / {data['voice']}",
                    )
        elif word.startswith(cmd_chr):
            for cmd, data in COMMANDS.items():
                if cmd.startswith(word):
                    yield Completion(
                        cmd,
                        start_position=-len(word),
                        display=f"{cmd}",
                        display_meta=data["desc"],
                    )
