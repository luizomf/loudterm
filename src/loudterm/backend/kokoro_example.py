import soundfile as sf
import torch

from loudterm.backend.kokoro_generator import KokoroGenerator
from loudterm.backend.kokoro_voices import KOKORO_VOICES

english = """
For some days after that evening, Mr. Heathcliff shunned meeting us at meals; yet he would not consent formally to exclude Hareton and Cathy. He had an aversion to yielding so completely to his feelings, choosing rather to absent himself; and eating once in twenty-four hours seemed sufficient sustenance for him.

One night, after the family were in bed, I heard him go downstairs, and out at the front door. I did not hear him re-enter, and in the morning I found he was still away. We were in April then: the weather was sweet and warm, the grass as green as showers and sun could make it, and the two dwarf apple-trees near the southern wall in full bloom. After breakfast, Catherine insisted on my bringing a chair and sitting with my work under the fir-trees at the end of the house; and she beguiled Hareton, who had perfectly recovered from his accident, to dig and arrange her little garden, which was shifted to that corner by the influence of Joseph’s complaints. I was comfortably revelling in the spring fragrance around, and the beautiful soft blue overhead, when my young lady, who had run down near the gate to procure some primrose roots for a border, returned only half laden, and informed us that Mr. Heathcliff was coming in. “And he spoke to me,” she added, with a perplexed countenance.

“What did he say?” asked Hareton.

“He told me to begone as fast as I could,” she answered. “But he looked so different from his usual look that I stopped a moment to stare at him.”

“How?”, he inquired.

“Why, almost bright and cheerful. No, almost nothing—very much excited, and wild, and glad!” she replied.
"""  # noqa: E501

portuguese = """
Do titulo.
Uma noite destas, vindo da cidade para o Engenho Novo, encontrei no trem da Central um rapaz aqui do bairro, que eu conheço de vista e de chapéo. Comprimentou-me, sentou-se ao pé de mim, falou da lua e dos ministros, e acabou recitando-me versos. A viagem era curta, e os versos póde ser que não fossem inteiramente maus. Succedeu, porém, que como eu estava cançado, fechei os olhos tres ou quatro vezes; tanto bastou para que elle interrompesse a leitura e mettesse os versos no bolso.

—Continue, disse eu accordando.

—Já acabei, murmurou elle.

—São muito bonitos.

Vi-lhe fazer um gesto para tiral-os outra vez do bolso, mas não passou do gesto; estava amuado. No dia seguinte entrou a dizer de mim nomes feios, e acabou alcunhando-me Dom Casmurro. Os visinhos, que não gostam dos meus habitos reclusos e calados, deram curso á alcunha, que afinal pegou. Nem por isso me zanguei. Contei a anecdota aos amigos da cidade, e elles, por graça, chamam-me assim, alguns em bilhetes: «Dom Casmurro, domingo vou jantar com você.»—«Vou para Petropolis, Dom Casmurro; a casa é a mesma da Rhenania; vê se deixas essa caverna do Engenho Novo, e vae lá passar uns quinze dias commigo.»—«Meu caro Dom Casmurro, não cuide que o dispenso do theatro amanhã; venha e dormirá aqui na cidade; dou-lhe camarote, dou-lhe chá, dou-lhe cama; só não lhe dou moça.»

Não consultes diccionarios. Casmurro não está aqui no sentido que elles lhe dão, mas no que lhe poz o vulgo de homem calado e mettido comsigo. Dom veiu por ironia, para attribuir-me fumos de fidalgo. Tudo por estar cochilando! Tambem não achei melhor titulo para a minha narração; se não tiver outro d'aqui até ao fim do livro, vae este mesmo. O meu poeta do trem ficará sabendo que não lhe guardo rancor. E com pequeno esforço, sendo o titulo seu, poderá cuidar que a obra é sua. Ha livros que apenas terão isso dos seus autores; alguns nem tanto.

II
Do livro.
Agora que expliquei o titulo, passo a escrever o livro. Antes disso, porém, digamos os motivos que me põem a penna na mão.

Vivo só, com um creado. A casa em que moro é propria; fil-a construir de proposito, levado de um desejo tão particular que me vexa imprimil-o, mas vá lá. Um dia, ha bastantes annos, lembrou-me reproduzir no Engenho Novo a casa em que me criei na antiga rua de Matacavallos, dando-lhe o mesmo aspecto e economia daquella outra, que desappareceu. Constructor e pintor entenderam bem as indicações que lhes fiz: é o mesmo predio assobradado, tres janellas de frente, varanda ao fundo, as mesmas alcovas e salas. Na principal destas, a pintura do tecto e das paredes é mais ou menos egual, umas grinaldas de flores miudas e grandes passaros que as tomam nos bicos, de espaço a espaço. Nos quatro cantos do tecto as figuras das estações, e ao centro das paredes os medalhões de Cesar, Augusto, Nero e Massinissa, com os nomes por baixo... Não alcanço a razão de taes personagens. Quando fomos para a casa de Matacavallos, já ella estava assim decorada; vinha do decennio anterior. Naturalmente era gosto do tempo metter sabor classico e figuras antigas em pinturas americanas. O mais é tambem analogo e parecido. Tenho chacarinha, flôres, legume, uma casuarina, um poço e lavadouro. Uso louça velha e mobilia velha. Emfim, agora, como outr'ora, ha aqui o mesmo contraste da vida interior, que é pacata, com a exterior, que é ruidosa.

O meu fim evidente era atar as duas pontas da vida, e restaurar na velhice a adolescencia. Pois, senhor, não consegui recompor o que foi nem o que fui. Em tudo, se o rosto é egual, a physionomia é differente. Se só me faltassem os outros, vá; um homem consola-se mais ou menos das pessoas que perde; mas falto eu mesmo, e esta lacuna é tudo. O que aqui está é, mal comparando, semelhante á pintura que se põe na barba e nos cabellos, e que apenas conserva o habito externo, como se diz nas autopsias; o interno não aguenta tinta. Uma certidão que me desse vinte annos de edade poderia enganar os extranhos, como todos os documentos falsos, mas não a mim. Os amigos que me restam são de data recente; todos os antigos foram estudar a geologia dos campos santos. Quanto ás amigas, algumas datam de quinze annos, outras de menos, e quasi todas creem na mocidade. Duas ou tres fariam crer nella aos outros, mas a lingua que falam obriga muita vez a consultar os diccionarios, e tal frequencia é cançativa.

Entretanto, vida differente não quer dizer vida peor; é outra cousa. A certos respeitos, aquella vida antiga apparece-me despida de muitos encantos que lhe achei; mas é tambem exacto que perdeu muito espinho que a fez molesta, e, de memoria, conservo alguma recordação doce e feiticeira. Em verdade, pouco appareco e menos falo. Distracções raras. O mais do tempo é gasto em hortar, jardinar e ler; como bem e não durmo mal.

Ora, como tudo cança, esta monotonia acabou por exhaurir-me tambem. Quiz variar, e lembrou-me escrever um livro. Jurisprudencia, philosophia e politica acudiram-me, mas não me acudiram as forças necessarias. Depois, pensei em fazer uma Historia dos Suburbios, menos secca que as memorias do padre Luiz Gonçalves dos Santos, relativas á cidade; era obra modesta, mas exigia documentos e datas, como preliminares, tudo arido e longo. Foi então que os bustos pintados nas paredes entraram a falar-me e a dizer-me que, uma vez que elles não alcançavam reconstituir-me os tempos idos, pegasse da penna e contasse alguns. Talvez a narração me désse a illusão, e as sombras viessem perpassar ligeiras, como ao poeta, não o do trem, mas o do Fausto: Ahi vindes outra vez, inquietas sombras...?

Fiquei tão alegre com esta ideia, que ainda agora me treme a penna na mão. Sim, Nero, Augusto, Massinissa, e tu, grande Cesar, que me incitas a fazer os meus commentarios, agradeço-vos o conselho, e vou deitar ao papel as reminiscencias que me vierem vindo. Deste modo, viverei o que vivi, e assentarei a mão para alguma obra de maior tomo. Eia, comecemos a evocação por uma celebre tarde de Novembro, que nunca me esqueceu. Tive outras muitas, melhores, e peores, mas aquella nunca se me apagou do espirito. É o que vás entender, lendo.
"""  # noqa: E501

TEXTS = {
    "a": english,
    "b": english,
    "p": portuguese,
}

for voice, data in KOKORO_VOICES.items():
    all_chunks: list[torch.Tensor] = []
    lang = data["language_code"]

    if lang not in TEXTS:
        continue

    text = TEXTS[lang]

    kokoro = KokoroGenerator(lang_code=lang)

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
