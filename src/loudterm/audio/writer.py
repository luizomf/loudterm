from pathlib import Path

import soundfile as sf

from loudterm.core import AudioResult


class AudioWriter:
    """High-level audio writer API using soundfile."""

    def save(self, audio: AudioResult, path: Path) -> None:
        """Save audio to disk."""
        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)
        sf.write(path, audio.samples, audio.sample_rate)  # type: ignore[reportUnknownMemberType]
