# ruff: noqa: ERA001
import time
import warnings

import soundfile as sf
import torch
from kokoro import KPipeline

from loudterm.backend.kokoro82m.text_examples import TEXT_EXAMPLES
from loudterm.config import OUTPUT_DIR

voice = "af_heart"
lang_code = "a"

text = TEXT_EXAMPLES[lang_code]
sr = 24000

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
    # warnings.filterwarnings("ignore", module="jieba") # se usar chinês

    pipeline = KPipeline(lang_code=lang_code, repo_id="hexgrad/Kokoro-82M")
    filename_ts = f"{time.time():.0f}"

    audio_parts: list[torch.Tensor] = []
    generator = pipeline(text, voice=voice)

    for i, (gs, ps, audio) in enumerate(generator):
        if not isinstance(audio, (torch.Tensor, torch.FloatTensor)):
            continue

        print(gs)
        print("-" * 80)
        print(ps)

        audio_parts.append(audio)
        output_file = OUTPUT_DIR / f"{voice}_{filename_ts}_part{i}.wav"
        sf.write(output_file, audio, sr)  # type: ignore[reportUnknownMemberType]

        print("-" * 80)

if audio_parts:
    final_audio = torch.cat(audio_parts, dim=0).float()
    output_file = OUTPUT_DIR / f"{voice}_{filename_ts}_full.wav"
    sf.write(output_file, final_audio, sr)  # type: ignore[reportUnknownMemberType]
