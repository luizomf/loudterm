import warnings
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any, Optional

from kokoro import KPipeline
from torch import FloatTensor, Tensor

from loudterm.core import AudioResult


@contextmanager
def kokoro_warning_filter() -> Generator[None]:
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            category=FutureWarning,
            module="torch.nn.utils.weight_norm",
        )
        warnings.filterwarnings(
            "ignore",
            message=".*dropout option adds dropout.*",
            category=UserWarning,
            module="torch.nn.modules.rnn",
        )
        warnings.filterwarnings("ignore", module="jieba")
        yield


class KokoroGenerator:
    """Wrapper for the Kokoro TTS pipeline."""

    def __init__(self, lang_code: str = "a", device: Optional[str] = None) -> None:
        """
        Initialize the Kokoro pipeline.

        Args:
            lang_code: Language code (e.g., 'a' for American English, 'b' for British).
        """
        # KPipeline loads the model weights (can be ~300MB download on first run)
        # We suppress noisy warnings from torch/internals here
        with kokoro_warning_filter():
            self.pipeline = KPipeline(
                lang_code=lang_code,
                repo_id="hexgrad/Kokoro-82M",
                device=device,
            )

    def generate(
        self,
        text: str,
        voice: str = "af_heart",
        speed: float = 1.0,
        split_pattern: str = r"\n+",
    ) -> Generator[AudioResult, Any]:
        """
        Generate audio chunks from text.

        Yields:
            AudioResult: A chunk of generated audio.
        """
        generator = self.pipeline(
            text,
            voice=voice,
            speed=speed,
            split_pattern=split_pattern,
        )

        for graphemes, phonemes, raw_audio in generator:
            samples = raw_audio

            if isinstance(samples, (FloatTensor, Tensor)):
                yield AudioResult(
                    samples=samples,
                    graphemes=str(graphemes),
                    phonemes=str(phonemes),
                    sample_rate=24000,
                )
