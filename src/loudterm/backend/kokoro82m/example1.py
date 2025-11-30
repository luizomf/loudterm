# EXAMPLE USING Kokoro alone


import soundfile as sf
from kokoro import KPipeline

voice = "af_heart"
lang_code = "a"


pipeline = KPipeline(lang_code=lang_code, repo_id="hexgrad/Kokoro-82M")

text = """
[Kokoro](/kˈOkəɹO/) is an open-weight TTS model with 82 million parameters. \
Despite its lightweight architecture, it delivers comparable quality to larger \
models while being significantly faster and more cost-efficient. With \
Apache-licensed weights, [Kokoro](/kˈOkəɹO/) can be deployed anywhere from production \
environments to personal projects.
"""  # noqa: RUF001

generator = pipeline(text, voice=voice)
for i, (gs, ps, audio) in enumerate(generator):
    print(gs)
    print(ps)
    sf.write(f"output/{i}.wav", audio, 24000)  # type: ignore[reportUnknownMemberType]
