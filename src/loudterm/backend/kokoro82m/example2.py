# EXAMPLE USING KokoroGenerator
import time

import soundfile as sf
import torch

from loudterm.backend.kokoro82m.generator import KokoroGenerator
from loudterm.backend.kokoro82m.text_examples import TEXT_EXAMPLES
from loudterm.backend.kokoro82m.voices import KOKORO_VOICES
from loudterm.config import OUTPUT_DIR

for voice_key, voice_data in KOKORO_VOICES.items():
    audio_parts: list[torch.Tensor] = []
    lang_code = voice_data["language_code"]

    if lang_code not in TEXT_EXAMPLES:
        print("Missing text for language:", voice_data["desc"])
        print("-" * 80)
        continue

    text = TEXT_EXAMPLES[lang_code]

    filename_ts = f"{time.time():.0f}"
    kokoro = KokoroGenerator(lang_code=lang_code)
    audio_result = None
    voice = voice_key[1:]

    for audio_result in kokoro.generate(
        text=text,
        voice=voice,
    ):
        print(voice)
        print(audio_result.graphemes)
        print("-" * 80)
        print()
        audio_parts.append(audio_result.samples)

    if audio_parts and audio_result:
        output_file = OUTPUT_DIR / f"{filename_ts}_{voice}_full.wav"
        sf.write(  # type: ignore[reportUnknownMemberType]
            output_file,
            torch.cat(audio_parts, dim=0).float(),
            samplerate=audio_result.sample_rate,
        )
