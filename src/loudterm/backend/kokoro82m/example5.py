# ruff: noqa: RUF001, ERA001

# SUGESTÃO DO @WillianSandro-z6z
# Juntar vozes para formar uma nova

# import sounddevice as sd
import soundfile as sf
import torch
from kokoro import KPipeline

from loudterm.config import OUTPUT_DIR

# Estes fonemas vieram do próprio Kokoro (exemplo3.py), eu só juntei eles em
# uma única string e agora estou com preguiça de fazer uma lista.
PHONEMES = """\
tˌeɲʊ trˌabaljˈadʊ nˈɛsæ ˌidˈɛɪæ ʒˈa faz ũŋ tˈAmpʊ, i tˈodæ vˈes ky vˈɔltʊ pra \
ˈɛlæ, pˌeɾəsˈebw ˌWɡˈumæ kˈoɪzæ nˈɔvæ. aːz vˈezyz ɛ ũŋ dˌetˈaljy pˌekˈenʊ, aːz \
vˈezyz ɛ ũŋ trˈeʃw ˌiŋtˈAɾʊ ky, dʊ nˈadæ, pˈasæ a fazˌer sˌAŋʧˈidʊ. ɛ \
ˌAŋɡrasˈadʊ kˌomʊ ʊ sˈɛɾebrʊ fˌũŋsiˈonæ — ˌely prˌeˈAŋʃj az lˌakˈunæz mˈezmʊ \
kwˈɐ̃ŋdw a ʒˈAŋʧy nˌɐ̃ʊ̃ tˈa prˌestˈɐ̃ŋdw ˌatAŋsˈɐ̃ʊ̃. ˈɛ, sˌiŋseɾæmˈAŋʧy, ɛ ˈisʊ ky \
dˈAʃæ ˌesi prˌoʒˈɛtʊ tˈɐ̃ʊ̃ ˌAmpowɡˈɐ̃ŋʧy pra mˈiŋ.

kwˈɐ̃ŋdw ˌimaʒˈinʊ kˌomʊ ˈisʊ dˌeveɾˈiæ soˈar, pˈAŋsʊ nˌumæ vˈɔs kˈWmæ, \
ˌestˈaveʊ, mas sˈAŋ akˌɛlæ mˌonotonˈiæ ʃˈatæ. ˌumæ fˈalæ ky vI ʤj ũŋ \
pˌAŋsæmˈAŋtʊ prʊ ˈowtrʊ sˈAŋ prˈɛsæ, koŋ xˌespiɾasˈɐ̃ʊ̃ ˈAŋtri az ˌidˈɛɪæs. \
nˈadæ foɾəmˈW demˈIs, nˈadæ sˈowtʊ demˈIs. sˈɔ ũŋ xˈitmʊ nˌatuɾˈW. sj ʊ \
tˌetˌeˈɛsy kˌoŋseɡˈir peɡˈaɾ ʊ sˌAŋʧimˈAŋtʊ, aˈi sˈiŋ eʊ sˈA ky tˈo nʊ \
kˌæmˈiɲʊ sˈɛɾətʊ.

klˈaɾʊ ky ˌaˈiŋdæ tAŋ mwˈiŋtæ kˈoɪzæ pra testˈar. ˌWɡˈumæs frˈazys fˈikɐ̃ʊ̃ \
ˈɔʧimæs, ˌAŋkwˈɐ̃ŋtw ˈowtræs sˈoɐ̃ʊ̃ mˈAʊ dˈuɾæs, kwˈazy mˌekˈɐ̃nikæs. noɾəmˈW. \
tˈodʊ mˌodˈelʊ tAŋ sˌuæz mˌænˈiæs, i pˈaɾəʧy da brˌiŋkadˈAɾæ ɛ ˌaprAŋdˈeɾ a \
ˌeskrevˈer ʤj ũŋ ʒˈAtʊ ky xˌeˈWsj ʊ ky ˌely tAŋ ʤy meljˈɔr. koŋ tˈAmpʊ, \
ˌaʒˈusʧyz i ˌespeɾimˈAŋtʊs, a vˈɔs kˌomˈɛsæ a pˌaɾesˈer mˈenʊz ˌumæ mˈakinæ i \
mˈIz WɡˈAŋ kˌoŋtˈɐ̃ŋdw ˌumæ ˌistˈɔɾjæ.
"""

# O texto abaixo também veio do exemplo3.py
TEXT = """\
Tenho trabalhado nessa ideia já faz um tempo, e toda vez que volto pra ela, \
percebo alguma coisa nova. Às vezes é um detalhe pequeno, às vezes é um trecho \
inteiro que, do nada, passa a fazer sentido. É engraçado como o cérebro \
funciona — ele preenche as lacunas mesmo quando a gente não tá prestando \
atenção. E, sinceramente, é isso que deixa esse projeto tão empolgante pra mim.

Quando imagino como isso deveria soar, penso numa voz calma, estável, mas sem \
aquela monotonia chata. Uma fala que vai de um pensamento pro outro sem pressa\
, com respiração entre as ideias. Nada formal demais, nada solto demais. Só um \
ritmo natural. Se o TTS conseguir pegar o sentimento, aí sim eu sei que tô no \
caminho certo.

Claro que ainda tem muita coisa pra testar. Algumas frases ficam ótimas, \
enquanto outras soam meio duras, quase mecânicas. Normal. Todo modelo tem suas \
manias, e parte da brincadeira é aprender a escrever de um jeito que realce o \
que ele tem de melhor. Com tempo, ajustes e experimentos, a voz começa a \
parecer menos uma máquina e mais alguém contando uma história.
"""

lang_code = "p"  # Idioma português do brasil
sr = 24000

# Sem model
pipeline = KPipeline(lang_code=lang_code, repo_id="hexgrad/Kokoro-82M")

# Vozes (o total dos valores precisa dar 1)
voices = {
    "pf_dora": 1,  # Deixo as vozes do PT-BR mais pesadas (acima de 0.5)
    # "pm_santa": 0.2,  # Isso também é PT-BR (total 0.6)
    # "af_heart": 0.4,  # Voz americana (dá um pouquinho de sotaque)
}
# Multiplica a voz pelo peso e soma todas as vozes
new_voice = sum([pipeline.load_voice(k) * v for k, v in voices.items()])

final_audio: list[torch.Tensor] = []

for gs, ps, audio in pipeline(text=TEXT, voice=new_voice, speed=1):  # type: ignore[reportArgumentType]
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
