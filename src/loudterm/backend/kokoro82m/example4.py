# ruff: noqa: RUF001

# Usei os fonemas do exemplo3.py. Qualquer voz fala português, mas fica com
# sotaque.

import sounddevice as sd
from kokoro import KPipeline

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

voice = "af_bella"  # Voz do inglês americano (vai ficar com sotaque)
lang_code = "p"  # Idioma português do brasil
sr = 24000

# Sem model
pipeline = KPipeline(lang_code=lang_code, repo_id="hexgrad/Kokoro-82M")

# MÁXIMO DE 510 CARACTERES
# O split é só pra garantir frases menores. Se você receber isso do próprio
# Kokoro, já vem no tamanho certo (ver exemplo3.py).
for phonemes in PHONEMES.strip().split("\n"):
    phoneme = phonemes.strip()
    if not phoneme:
        continue

    for _, ps, audio in pipeline.generate_from_tokens(
        tokens=phoneme,
        voice=str(voice),
        speed=1,
    ):
        print(ps)
        print("-" * 80)
        sd.play(audio, samplerate=sr)  # type: ignore[reportUnknownMemberType]
        sd.wait()
