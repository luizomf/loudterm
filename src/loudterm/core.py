from dataclasses import dataclass

from torch import Tensor


@dataclass(slots=True)
class AudioResult:
    """Represents an in-memory audio buffer"""

    samples: Tensor
    sample_rate: int
