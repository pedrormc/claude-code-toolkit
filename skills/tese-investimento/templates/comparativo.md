# Template: Comparativo (slides para apresentação multi-opção)

> Use quando o caso for `tipo=comparativo` (ex: PowerCoff vs sóbrio Simon). Resultado: 8 slides padrão + 1 slide por sub-tese (modular).

## Estrutura dos slides

### Slide 1: Capa

- One-liner da apresentação
- Logo Singular (ver `Desktop/dondon/pop` pra brand assets)
- Nome do investidor
- Data
- Apresentador: Pedro Roberto (Robertinho)

### Slide 2: Resumo executivo

- "Aqui estão 2 opções na mesa pra os R$ X que você confiou pra gestão"
- Ambas em 1 frase cada
- Sem números detalhados ainda — só posicionamento

### Slide 3: Critério de decisão

- O que importa pra esse investidor? (perfil + horizonte + tolerância a risco)
- Tabela de critérios ponderados (ex: preservação 40%, retorno 30%, liquidez 20%, alinhamento 10%)
- Conexão com a relação operador-investidor (se há confiança alta, a opção arriscada vira mais aceitável)

### Slide 4: Opção A — tese resumida

(Aqui vai 1 sub-tese — em geral a sóbria, pelo princípio de mostrar primeiro o conservador)

- Tese em 1 frase
- Mecânica em 3 bullets (o quê, como, quando)
- Retorno esperado (número)
- Risco principal (1 frase)

### Slide 5: Opção B — tese resumida

(A outra sub-tese — em geral a arriscada, depois de plantar a alternativa segura)

- Mesmo formato do slide 4
- Destacar o upside vs Opção A
- Mas sem esconder o risco

### Slide 6: (Opção N — opcional, se houver mais sub-teses)

Mesmo formato.

### Slide 7: Tabela comparativa side-by-side

| Critério | Opção A | Opção B | (Opção N) |
|---|---|---|---|
| Retorno esperado | X% a.a. | Multiplicador 2-4x | ... |
| Risco principal | Drawdown | Falha de execução | ... |
| Horizonte | 5+ anos | 24 meses | ... |
| Liquidez | Alta (resgate 30d) | Baixa (saída via venda) | ... |
| Tributação | Y% IR | Z% IR ganho de capital | ... |
| Alinhamento operador | Indireto (gestor terceiro) | Direto (Pedro é o operador) | ... |

### Slide 8: Recomendação + próximo passo

- Recomendação justificada **com número** (não só argumento qualitativo)
- Próximo passo concreto: "Você decide se topa a opção, parcialmente, ou totalmente. Posso operar a partir de quando?"
- 3 perguntas claras pro investidor responder na hora

## Como gerar `slides.md` a partir deste template

Pra cada slide acima, escrever em `slides.md`:

```markdown
## Slide N: <Título do slide>

**Prompt pra IA de design:**

Contexto: [explicar o contexto específico deste slide pra investidor próximo de cheque pessoal — não pra VC institucional]

Layout sugerido: [específico — colunas, alinhamento, hierarquia tipográfica]

Dados a colocar: [bullets ou números reais — vir do brief]

Tom: [profissional mas próximo, sem jargão tech-bro]

Tipografia: [sans-serif, hierarquia clara, números em destaque]

Footer/Disclaimer: [quando aplicável]

Visual mood: [específico — sóbrio, otimista, comparativo, etc]
```

## Heurísticas de tom

- Investidor próximo (não institucional) → sem jargão, sem termos em inglês desnecessários, sem "TAM/SAM/SOM".
- Investidor com confiança alta no operador → reforçar relação (slide 3 e 8 podem mencionar histórico)
- Cheque pequeno (R$ 10-30k) → não pomposo. Slides simples, diretos.
- Apresentação pessoal (não Zoom/cold pitch) → assumir que vai conversar entre slides — slides são guia, não autoexplicativos.

## Exemplo concreto de output (pega da spec §5.4)

Ver spec `docs/superpowers/specs/2026-04-28-tese-investimento-design.md` §5.4 — exemplo completo do Slide 7 (Cenários PowerCoff).
