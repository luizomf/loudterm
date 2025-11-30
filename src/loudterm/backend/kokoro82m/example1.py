# EXAMPLE USING Kokoro alone


import soundfile as sf
from kokoro import KPipeline

from loudterm.config import ROOT_DIR

CONFIG_FILENAME = "config.json"
CONFIG_PATH = ROOT_DIR / "src" / "loudterm" / "backend" / "kokoro82m" / CONFIG_FILENAME


voice = "af_heart"
lang_code = "a"

# model = KModel(
#     config=str(CONFIG_PATH),
#     model="kokoro-v1_1-zh.pth",
#     repo_id="hexgrad/Kokoro-82M",
# )


pipeline = KPipeline(lang_code=lang_code, repo_id="hexgrad/Kokoro-82M")

text = """
[Kokoro](/kˈOkəɹO/) is an open-weight TTS model with 82 million parameters. \
Despite its lightweight architecture, it delivers comparable quality to larger \
models while being significantly faster and more cost-efficient. With \
Apache-licensed weights, [Kokoro](/kˈOkəɹO/) can be deployed anywhere from production \
environments to personal projects.
"""  # noqa: RUF001

text = """
新しい声を聞くと、なぜかこころが少しだけ落ち着きます。ゆっくりしたテンポで話してくれると、その言葉がまっすぐこころに入ってくる感じがします。そして、その声に気持ちが重なると、自分のこころも優しくなるような気がします。
    """

generator = pipeline(text, voice=voice)
for i, (gs, ps, audio) in enumerate(generator):
    print(gs)
    print(ps)
    sf.write(f"output/{i}.wav", audio, 24000)  # type: ignore[reportUnknownMemberType]

pipeline = None
del pipeline
