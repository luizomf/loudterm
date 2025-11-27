from pathlib import Path

from loudterm.core import AudioResult


class AudioWriter:
    """High-level audio writer API

    Later this will wrap soundfile or similar.
    """

    def save(self, audio: AudioResult, path: Path) -> None:
        msg = (
            "Audio writing is not implemented yet."
            "This is a placeholder for the loudterm audio writer."
        )
        raise NotImplementedError(msg)
