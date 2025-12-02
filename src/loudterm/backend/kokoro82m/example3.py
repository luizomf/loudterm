# ruff: noqa: ERA001
# Este exemplo foi gerado após eu ter gravado o vídeo. Talvez eu gere outros.
# Aqui, vou subir o Kokoro sem model, isso vai me permitir pegar grafemas e
# fonemas. Pode ser necessário fazer isso antes de gerar o áudio por vários
# motivos.

from pathlib import Path

from kokoro import KPipeline

from loudterm.backend.kokoro82m.text_examples import TEXT_EXAMPLES

# OFFLINE
# Comente isso se você não baixou a voz (estou usando vozes locais)
voice = (
    Path("..").resolve() / "offline_files" / "kokoro" / "voices" / "pt" / "af_heart.pt"
)


# ONLINE (NORMAL)
# Se comentar acima, descomente abaixo
# voice = "af_heart"

lang_code = "p"
text = TEXT_EXAMPLES[lang_code]

# Sem model
pipeline = KPipeline(model=False, lang_code=lang_code, repo_id="hexgrad/Kokoro-82M")

# Agora não vem nada no áudio (None)
for gs, ps, _ in pipeline(text=text, voice=str(voice), speed=1, split_pattern="\n+"):
    print(gs)
    print("-" * 80)
    print(ps)
    print("-" * 80)
