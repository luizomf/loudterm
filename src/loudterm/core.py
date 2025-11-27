from dataclasses import dataclass
from typing import Protocol


@dataclass(slots=True)
class AudioResult:
    """Represents an in-memory audio buffer"""

    samples: str  # this will be np.ndarray[np.float32]
    sample_rate: int


class TTSBackend(Protocol):
    """Interface for any TTS backend implementation."""

    def synthesize(
        self,
        text: str,
        *,
        voice: str | None = None,
        lang: str | None = None,
        speed: float = 1.0,
    ) -> AudioResult: ...
