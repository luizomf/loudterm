# ruff: noqa: ERA001

# SUGESTÃO DO @WillianSandro-z6z
# Juntar vozes para formar uma nova

# import sounddevice as sd
import soundfile as sf
import torch
from kokoro import KPipeline

from loudterm.backend.kokoro82m.text_examples import TEXT_EXAMPLES
from loudterm.config import OUTPUT_DIR

lang_code = "p"  # Idioma português do brasil
sr = 24000

# Sem model
pipeline = KPipeline(lang_code=lang_code, repo_id="hexgrad/Kokoro-82M")

# MMMMEEEEUUUU DEUUUUUUUUSSSS - ISSSOOOO FOIIII CAGAAAADAAA
# FICOU MUITO BOM
# Vozes (faça o valor dar 1.0 para ficar normalizado)
voices = {
    "pf_dora": 0.25,  # Deixo as vozes do PT-BR mais pesadas
    "pm_santa": 0.25,  # Isso também é PT-BR
    "af_bella": 0.1,  # Voz americana (dá um pouquinho de sotaque)
    "if_sara": 0.1,  # Voz americana (dá um pouquinho de sotaque)
    "af_heart": 0.2,  # Voz americana (dá um pouquinho de sotaque)
    "ff_siwis": 0.1,  # Voz americana (dá um pouquinho de sotaque)
}
# Multiplica a voz pelo peso e soma todas as vozes
mixed = sum(pipeline.load_voice(k) * v for k, v in voices.items())
new_voice = mixed / torch.norm(mixed)  # type: ignore[reportUnknownMemberType]

final_audio: list[torch.Tensor] = []

for gs, ps, audio in pipeline(text=TEXT_EXAMPLES[lang_code], voice=mixed, speed=1):  # type: ignore[reportArgumentType]
    print(gs)
    print("-" * 80)
    print(ps)
    print("-" * 80)
    # sd.play(audio, samplerate=sr)  # type: ignore[reportUnknownMemberType]
    # sd.wait()

    if isinstance(audio, torch.FloatTensor):
        final_audio.append(audio)

if final_audio:
    sf.write(  # type: ignore[reportUnknownMemberType]
        OUTPUT_DIR / "sample.wav",
        torch.cat(final_audio, dim=0).float(),
        samplerate=sr,
    )
