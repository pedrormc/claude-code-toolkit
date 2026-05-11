# Checklist Default (modo B) — 10 itens

> Skill cobre estes 10 itens antes de gerar `tese.md` + `slides.md`. Em v0.5 a cobertura é mental (Claude tracked, Pedro confirma quando perguntado). Em v1 vira gate bloqueante via `meta.yaml > checklist`.

## Os 10 itens

| # | Item | Operação (ex: PowerCoff) | Aplicação (ex: sóbrio Simon) |
|---|---|---|---|
| 1 | Tese (o quê + por quê) | "Investir R$ X em equity da Y porque Z" | "Alocar R$ X em previdência+FII porque Z" |
| 2 | Retorno esperado | Múltiplo / IRR / payback (com nº) | Yield % a.a. + cenário composto (com nº) |
| 3 | Risco principal | Falha de execução, mercado, regulatório | Volatilidade, drawdown, juros, default |
| 4 | Horizonte | Meses até saída/dividendo | Anos até resgate / sem resgate |
| 5 | Unit economics / mecânica | CMV, margem bruta, LTV, CAC, payback | Yield, taxa adm, tributação, drawdown histórico |
| 6 | Cenários (otim/base/pess) | 3 trajetórias com nº | 3 trajetórias com nº |
| 7 | Mitigação de risco | O que reduz o risco do #3 | Diversificação, gatilhos de saída |
| 8 | Comparáveis / benchmarks | Outras cafeterias, marcas similares | CDI, IPCA+, peers do FII |
| 9 | Perfil + relação investidor | Tolerância a risco, confiança no operador | Idem |
| 10 | Exit / saída | Como ele recebe de volta (recompra, dividendo, venda) | Liquidez, prazo de resgate |

## Como conduzir a coleta (v0.5)

1. Pedir contexto livre primeiro. Não interromper — deixar Pedro contar a história da tese.
2. Após contexto inicial, perguntar item por item, na ordem:
   - "Qual a tese central — em uma frase?" (#1)
   - "Que retorno você espera, em número, e em quanto tempo?" (#2 + #4)
   - "Qual o risco principal? E como você mitigaria?" (#3 + #7)
   - "Me passa unit economics / mecânica do investimento" (#5)
   - "Otimista, base, pessimista — me dá número pra cada um" (#6)
   - "Quais comparáveis te servem de benchmark?" (#8)
   - "Quem é o investidor — tolerância a risco e nível de confiança em ti?" (#9)
   - "Como ele sai do investimento?" (#10)
3. Se Pedro deixar buraco em algum item, anotar e perguntar antes de gerar slides.
4. Em modo `forçar geração`, pular pra Síntese sem cobrir tudo (e marcar lacunas no `tese.md`).

## Estados do item (v1, não usado em v0.5)

- `vazio` — não foi tocado
- `parcial` — mencionado mas sem profundidade
- `preenchido` — tem informação concreta (idealmente número)

## Comparativo (sub-teses)

Se `tipo=comparativo`, **cada sub-tese tem seu próprio checklist**. Coletar 10 itens pra cada sub-tese antes de produzir o slide comparativo.
