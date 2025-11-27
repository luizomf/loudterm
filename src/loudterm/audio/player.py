from loudterm.core import AudioResult


class AudioPlayer:
    """High-level audio playback API

    Later this will wrap sounddevice or other backend.
    """

    def play(self, audio: AudioResult) -> None:
        msg = (
            "Audio playback is not implemented yet."
            "This is a placeholder for the loudterm audio engine."
        )
        raise NotImplementedError(msg)
