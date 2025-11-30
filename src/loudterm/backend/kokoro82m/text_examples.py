from loudterm.backend.kokoro82m.text_examples_hindi import HINDI

english = """
I've been working on this idea for a while, and every time I come back to it, \
I notice something new. Sometimes it's a small detail, sometimes it's a whole \
section that suddenly makes more sense. It's funny how the brain works like \
that — always filling the gaps, even when we're not paying attention. And \
honestly, that's what keeps this project exciting for me.

When I imagine how this should sound, I picture a calm voice, steady but not \
monotone, moving from one thought to the next without rushing. A natural rhythm \
— not too formal, not too casual. Just enough space between ideas so the \
listener can breathe a little. If the TTS can capture that feeling, then I know \
I'm on the right track.

Of course, there's still a lot to test. Some sentences work beautifully, while \
others feel stiff, almost mechanical. That's normal. Every model has its quirks, \
and part of the fun is learning how to write in a way that brings out its \
strengths. Eventually, with enough tweaks and experiments, the voice starts \
sounding less like a machine and more like someone telling a story.
"""

portuguese = """
Tenho trabalhado nessa ideia já faz um tempo, e toda vez que volto pra ela, \
percebo alguma coisa nova. Às vezes é um detalhe pequeno, às vezes é um trecho \
inteiro que, do nada, passa a fazer sentido. É engraçado como o cérebro funciona \
— ele preenche as lacunas mesmo quando a gente não tá prestando atenção. E, \
sinceramente, é isso que deixa esse projeto tão empolgante pra mim.

Quando imagino como isso deveria soar, penso numa voz calma, estável, mas sem \
aquela monotonia chata. Uma fala que vai de um pensamento pro outro sem pressa, \
com respiração entre as ideias. Nada formal demais, nada solto demais. Só um \
ritmo natural. Se o TTS conseguir pegar o sentimento, aí sim eu sei que tô no \
caminho certo.

Claro que ainda tem muita coisa pra testar. Algumas frases ficam ótimas, \
enquanto outras soam meio duras, quase mecânicas. Normal. Todo modelo tem suas \
manias, e parte da brincadeira é aprender a escrever de um jeito que realce o \
que ele tem de melhor. Com tempo, ajustes e experimentos, a voz começa a \
parecer menos uma máquina e mais alguém contando uma história.
"""

# need:
# uv add pyopenjtalk 'fugashi[unidic-lite]' jaconv mojimoji unidic
# uv run -m unidic download
japanese = """\
このアイデアにはずっと取り組んでいて、時々ふと戻ってくるたびに、新しい発見があります。\
小さな気づきの時もあれば、急に全体がつながって見える瞬間もあります。\
人間の頭って本当に不思議ですよね。意識していなくても、勝手に穴を埋めてくれる。\
だからこそ、このプロジェクトはいつもワクワクできるんです。

これがどんな声で聞こえるべきかを想像すると、落ち着いた声がゆっくりと、\
でも単調にならずに進んでいくイメージです。急がず、でも止まりすぎない。\
その間に少しだけ呼吸の余裕があるような、自然なリズム。\
TTS がこの雰囲気をつかんでくれたら、きっとうまくいくと思います。

もちろん、まだ試すことはたくさんあります。うまく読める文章もあれば、\
どうしても機械っぽく聞こえてしまう文章もあります。でも、それは普通のことです。\
どのモデルにもクセがあって、そのクセを理解して書き方を調整するのも楽しみの一つです。\
何度か試していくうちに、だんだん“人の声”みたいに聞こえてくるようになります。
"""

# need:
# uv add ordered_set pypinyin cn2an jieba
chinese = """\
这个想法我已经研究了一段时间了。每次回头再看的时候，总会发现一些新的东西。\
有时候是很小的细节，有时候是一整段突然变得清晰起来。人的大脑真的很神奇，\
即使不注意，它也会自己把空白补上。也正因为这样，这个项目才一直让我觉得有意思。

我想象中的声音应该是平静、稳定的，但是不能太单调。说话的节奏要自然，\
从一个想法慢慢过渡到下一个，中间留一点呼吸的空间。不需要特别正式，\
也不需要太随意，就是一种舒服、自然的节奏。如果 TTS 能抓住这种感觉，那就说明方向是对的。

当然，还有很多地方需要测试。有些句子听起来很好，但有些还是会有点机械感。\
这很正常。每个模型都有自己的习惯，了解它、配合它，也是测试过程的一部分。\
慢慢调整、多试几次之后，声音就会开始像真人讲故事一样自然起来。
"""  # noqa: RUF001

french = """\
Je travaille sur cette idée depuis un bon moment, et chaque fois que j’y \
reviens, je découvre quelque chose de nouveau. Parfois c’est un petit détail, \
parfois une partie entière qui devient soudain plus claire. Le cerveau est \
vraiment étrange : même quand on n’y fait pas attention, il complète les vides \
tout seul. Et c’est exactement pour ça que ce projet reste aussi motivant pour \
moi.

Quand j’imagine la façon dont cela devrait sonner, je vois une voix calme, \
stable, mais jamais monotone. Une voix qui passe d’une idée à l’autre sans se \
presser, en laissant un peu d’espace pour respirer entre les phrases. Pas trop \
formelle, pas trop détendue non plus. Juste un rythme naturel. Si le TTS \
réussit à capter cette ambiance, alors je sais que je suis sur la bonne voie.

Bien sûr, il reste encore beaucoup à tester. Certaines phrases passent très \
bien, et d’autres sonnent un peu rigides, presque mécaniques. C’est normal. \
Chaque modèle a ses petites habitudes, et apprendre à écrire en tenant compte \
de ces nuances fait partie du jeu. Avec quelques ajustements et un peu d’\
expérience, la voix finit par sembler moins artificielle et plus proche d’un \
vrai récit.
"""  # noqa: RUF001

italian = """\
Sto lavorando a questa idea da un bel po’, e ogni volta che ci ritorno trovo \
qualcosa di nuovo. A volte è un piccolo dettaglio, altre volte un’intera parte \
che improvvisamente diventa più chiara. Il cervello è davvero strano: anche \
quando non ci facciamo caso, continua a colmare i vuoti da solo. Ed è proprio \
questo che rende il progetto sempre interessante per me.

Quando immagino come dovrebbe suonare tutto questo, penso a una voce calma e \
stabile, ma non monotona. Una voce che passa da un pensiero all’altro senza \
correre, lasciando un po’ di spazio per respirare. Niente di troppo formale, \
niente di troppo informale. Solo un ritmo naturale. Se il TTS riesce a \
catturare questa sensazione, allora significa che siamo sulla strada giusta.

Ovviamente c’è ancora molto da testare. Alcune frasi suonano benissimo, mentre \
altre risultano un po’ rigide, quasi meccaniche. È normale. Ogni modello ha le \
sue abitudini, e imparare a scrivere tenendole in considerazione fa parte del \
processo. Con un po’ di pazienza e qualche aggiustamento, la voce comincia a \
sembrare meno artificiale e più simile a una vera narrazione.
"""  # noqa: RUF001

spanish = """\
He estado trabajando en esta idea desde hace tiempo, y cada vez que vuelvo a \
revisarla descubro algo nuevo. A veces es un pequeño detalle, y otras veces es \
una parte entera que de repente se vuelve más clara. El cerebro es realmente \
curioso: incluso cuando no prestamos atención, sigue completando los espacios \
por su cuenta. Y por eso este proyecto siempre me mantiene motivado.

Cuando imagino cómo debería sonar todo esto, pienso en una voz tranquila y \
estable, pero sin caer en la monotonía. Una voz que pasa de una idea a otra \
sin prisa, dejando un poco de espacio para respirar entre las frases. Nada \
demasiado formal, pero tampoco demasiado relajado. Solo un ritmo natural. Si \
el TTS logra captar esa sensación, entonces estamos yendo por buen camino.

Por supuesto, todavía queda mucho por probar. Algunas frases suenan muy bien, \
mientras que otras se sienten un poco rígidas, casi mecánicas. Es normal. Cada \
modelo tiene sus particularidades, y aprender a escribir teniendo eso en \
cuenta también forma parte del proceso. Con unos cuantos ajustes y un poco de \
práctica, la voz empieza a sonar menos artificial y mucho más como un relato real.
"""

TEXT_EXAMPLES = {
    "a": english,
    "b": english,
    "e": spanish,
    "f": french,
    "h": HINDI,
    "i": italian,
    "j": japanese,
    "p": portuguese,
    "z": chinese,
}
