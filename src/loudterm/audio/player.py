import sounddevice as sd

from loudterm.core import AudioResult


class AudioPlayer:
    """High-level audio playback API using sounddevice."""

    def play(self, audio: AudioResult) -> None:
        """Play audio blocking until finished."""
        sd.play(audio.samples, audio.sample_rate, blocking=True)  # type: ignore[reportUnknownMemberType]
