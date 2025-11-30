# EXAMPLE USING KokoroGenerator
import soundfile as sf
import torch

from loudterm.backend.kokoro82m.generator import KokoroGenerator
from loudterm.backend.kokoro82m.text_examples import KOKORO_TEXT_EXAMPLES
from loudterm.backend.kokoro82m.voices import KOKORO_VOICES

for voice, data in KOKORO_VOICES.items():
    all_chunks: list[torch.Tensor] = []
    language_code = data["language_code"]

    if language_code not in KOKORO_TEXT_EXAMPLES:
        continue

    text = KOKORO_TEXT_EXAMPLES[language_code]

    kokoro = KokoroGenerator(lang_code=language_code)

    result = None

    for result in kokoro.generate(
        text=text,
        voice=voice[1:],
    ):
        print()
        print(voice[1:])
        print(result.graphemes)
        print(80 * "#")
        print()
        all_chunks.append(result.samples)

    if all_chunks and result:
        sf.write(  # type: ignore[reportUnknownMemberType]
            f"output/{voice[1:]}.wav",
            torch.cat(all_chunks, dim=0).float(),
            samplerate=result.sample_rate,
        )
