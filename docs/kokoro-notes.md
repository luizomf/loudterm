# Kokoro na prática

Esse arquivo existe porque quase ninguém sabe dessas coisas de cabeça. Eu,
você, a galera em volta... ninguém vai adivinhar isso sozinho.

A ideia aqui não é explicar TTS como se fosse artigo acadêmico. É deixar
anotado o que descobrimos usando o Kokoro no mundo real, especialmente no
nosso fluxo com `cliplay`.

---

## Resumo curto

Se a voz do Kokoro estiver muito reta ou meio sem vida, as alavancas mais úteis
que encontramos foram:

- baixar um pouco o `speed`
- misturar vozes
- escrever o texto de um jeito mais falável
- quebrar frases longas
- usar `--show-tokens` para inspecionar o que o modelo entendeu

O que **não** pareceu funcionar bem em PT-BR foi sair enfiando fonema manual,
stress marker e markup pensado pro caminho inglês.

---

## O que melhorou de verdade

### 1. `speed` mais baixo

O padrão `1.0` funciona, mas às vezes deixa a fala corrida e meio reta. Em
português, algo entre `0.88` e `0.95` costuma soar melhor.

Exemplo:

```bash
cliplay -l p -s 0.9 -t "Esse texto tende a sair um pouco menos apressado."
```

### 2. Mistura de vozes

O Kokoro aceita mistura de vozes. No nosso `cliplay`, isso agora funciona com
vírgulas no `--voice`.

Exemplo:

```bash
cliplay -l p -v 'pf_dora,pm_alex,af_bella' -s 0.9 \
  -t "Isso aqui costuma ficar menos reto do que usar só uma voz."
```

Esse foi um achado muito bom. A mistura acima ficou mais interessante do que
`pf_dora` sozinha.

### 3. Texto mais falável

Isso parece óbvio, mas faz muita diferença.

Melhor:

```text
Bom. Agora a gente vai testar outra coisa.
Se isso funcionar, ótimo.
Se não funcionar, a gente ajusta.
```

Pior:

```text
Bom agora a gente vai testar outra coisa se isso funcionar ótimo se não funcionar a gente ajusta
```

Pra TTS, vírgula, ponto e quebra de frase não são perfumaria. São direção.

### 4. Inspecionar tokens

Quando você quiser entender por que a fala saiu estranha, use:

```bash
cliplay -l p -v 'pf_dora,pm_alex,af_bella' -s 0.9 --show-tokens \
  -t "Texto de teste aqui."
```

Isso imprime:

- o texto do chunk
- os fonemas/tokens que o modelo usou

É muito útil pra descobrir quando o modelo "entendeu" alguma palavra de um jeito
esquisito.

---

## O que parece ser mais inglês do que português

A documentação e a comunidade do Kokoro mencionam coisas assim:

```text
[Kokoro](/kˈOkəɹO/)
ˈ
ˌ
(+2)
(-1)
```

Isso **existe mesmo** no ecossistema do Kokoro. Não foi invenção de interface.

Mas, no nosso teste com PT-BR, isso não encaixou bem com `pf_dora`. Em vez de
melhorar a fala, a voz começou a ler/engolir as marcações de um jeito torto.
Ficou aquela coisa meio "cahua", "karrô", bagunçado mesmo.

Então, por enquanto, a regra prática é:

- inglês: vale testar markup fonético e stress manual
- português: não confie nisso como solução principal

Pra PT-BR, o ganho parece vir mais de:

- direção do texto
- `speed`
- mistura de vozes
- chunking melhor

---

## O que sabemos tecnicamente

Esses pontos valem guardar:

- O `config.json` do modelo inclui tokens como `ˈ`, `ˌ`, `↓`, `→`, `↗`, `↘`.
- O `VOICES.md` avisa que vozes podem piorar em trechos muito curtos e podem
  correr em trechos longos.
- A issue `#286` do `Kokoro-FastAPI` sugere tentar fonemas customizados e
  stress/intonation, mas não mostra uma fórmula mágica que resolva tudo.
- Na prática, a própria comunidade parece estar explorando isso por tentativa,
  erro e ouvido.

Links:

- [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M)
- [config.json](https://huggingface.co/hexgrad/Kokoro-82M/raw/main/config.json)
- [VOICES.md](https://huggingface.co/hexgrad/Kokoro-82M/raw/main/VOICES.md)
- [SAMPLES.md](https://huggingface.co/hexgrad/Kokoro-82M/raw/main/SAMPLES.md)
- [Issue 286](https://github.com/remsky/Kokoro-FastAPI/issues/286)
- [Space oficial do Kokoro](https://huggingface.co/spaces/hexgrad/Kokoro-TTS)

---

## Preset prático que vale testar primeiro

Se você só quer um ponto de partida melhor, sem filosofar:

```bash
cliplay -l p -v 'pf_dora,pm_alex,af_bella' -s 0.9 \
  -t "Texto aqui"
```

Se estiver muito frio:

- baixe pra `0.88`
- deixe o texto mais respirável
- quebre frases grandes

Se estiver muito lento:

- suba pra `0.93` ou `0.95`

---

## Próximo passo provável

O próximo ganho grande provavelmente não vem de forçar mais fonema manual em
português.

Vem de fazer um pré-processamento melhor de texto pra TTS em PT-BR, por
exemplo:

- quebrar frases longas
- trocar pontuação ruim por pontuação falável
- limpar markdown
- evitar sequências que saem estranhas em voz
- talvez criar um preset `natural-pt`

Isso pode virar skill depois. Por enquanto, o objetivo desta nota é simples:
não deixar esse achado sumir.
