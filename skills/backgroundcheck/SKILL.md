---
name: backgroundcheck
description: Faz background check (due diligence reputacional) de uma pessoa física a partir do nome completo. Consulta processos judiciais públicos (STF, STJ, TST/PJe-JT, TJDFT, TJSP, Escavador, CNJ), mídia, redes sociais, conselhos profissionais, sanções (CGU/CEIS, TCU) e gera dossiê em .docx com identidade Singular, contendo links de cada fonte e análise de risco. Use quando o usuário digitar /backgroundcheck, ou pedir "background check", "dossiê de fulano", "due diligence reputacional", "checa o histórico do X", "puxa processos do Y", "investiga reputação de Z".
---

# /backgroundcheck — Dossiê reputacional + processos públicos

Recebe **nome completo** (e CPF opcional, se o usuário tiver) e gera um dossiê `.docx` com
todos os links de busca e uma análise consolidada da pessoa, baseada nas fontes públicas.

Output: arquivo `.docx` em `C:\Users\teste\Desktop\backgroundcheck\` com identidade visual
Singular (mesmo template do `/documento`, `/ata`, `/pop`).

## Limites legais e éticos (LER PRIMEIRO)

Esta skill consulta **APENAS fontes públicas** e usa **APENAS dados que o titular já
disponibilizou ou que estão em registros públicos**. Casos de uso legítimos:

- Due diligence pré-contratual (parceiro, fornecedor, embaixador, prestador)
- Verificação reputacional de candidato a vaga sênior (com transparência ao candidato)
- Auto-consulta — o próprio usuário sobre si mesmo
- Compliance Singular (PEP, sanção, lista negativa)

**NÃO USAR para:**
- Stalking, perseguição, retaliação
- Coleta massiva sem propósito legítimo (LGPD art. 7º)
- Vazar dados pessoais sensíveis a terceiros

Se o usuário pedir background check de alguém **e o motivo soar duvidoso**, pergunte o
propósito antes de gerar. Se for terceiro (não o próprio usuário), avise no chat:
"⚠️ LGPD: o titular tem direito de saber. Confirma que a base legal cobre essa consulta?"

## Quando usar

Invoque quando o usuário:
- Digitar `/backgroundcheck NOME COMPLETO` (com ou sem CPF)
- Pedir "background check de X", "dossiê de X", "due diligence do X"
- Pedir "checa os processos do X", "vê se X tem ficha", "investiga histórico do X"
- Pedir auto-consulta: "puxa meus processos", "background check meu"

**Não usar quando:**
- For consulta de empresa/CNPJ (criar skill separada `/empresacheck`)
- Já tiver número de processo específico (consulta direta no tribunal)
- Pedir só LISTA de fontes sem análise — responder direto no chat

## Fluxo de execução (6 passos)

### Passo 1 — Coletar input

```
[BG-CHECK] Me passa:
- Nome completo:
- CPF (opcional, melhora o match):
- Propósito (DD parceiro, candidato, auto-consulta, compliance):
- Profundidade (rápido = só links / completo = busca ativa + análise):
```

Se o usuário já passou o nome no comando, não perguntar de novo — só confirmar e
seguir. Profundidade default: **completo**.

### Passo 2 — Rodar o script de busca multi-fonte

```bash
python ~/.claude/skills/backgroundcheck/scripts/search.py "NOME COMPLETO" \
  --cpf "000.000.000-00" \
  --out /tmp/bgcheck-<slug>.json
```

Equivalente Windows:

```powershell
python "$env:USERPROFILE\.claude\skills\backgroundcheck\scripts\search.py" "NOME" `
  --out "$env:TEMP\bgcheck-<slug>.json"
```

O script consulta:
- **Escavador** (HTTP real) — busca pública por nome
- **Link tribunais** (STF, STJ, TST/PJe-JT, TJDFT, TJSP) — URLs prontas pra UI
- **Link CNJ Consulta Pública Unificada**
- **Link DataJud** (info — API pública não permite busca por nome por LGPD)
- **Link Receita/CNPJ** (vínculo societário via Google dork em `cnpj.biz` + `receita.fazenda.gov.br`)
- **Google dorks** — mídia, LinkedIn, notícias, .gov.br, DOU, conselhos profissionais (OAB/CRM/CRO/CRC), CVM/B3
- **Sanções públicas** — Portal da Transparência (CEIS/CNEP), TCU inelegíveis

Saída: JSON com `identidade`, `fontes_consultadas` (cada uma com `fonte`, `url_consulta`,
`status`, `achados`, `observacao`) e `resumo`.

### Passo 3 — Enriquecer com busca ativa (Claude faz no chat)

A partir do JSON, o Claude usa as próprias ferramentas pra ir além do que o script puxou.

**3a — Varredura societária (OBRIGATÓRIA, não pode pular)**

Toda execução do /backgroundcheck precisa ter uma seção dedicada a vínculos societários — atuais e históricos. Mesmo que o solicitante peça pra "ignorar que é empresário", manter a seção (só ajustar destaque na narrativa). Vínculos societários públicos são fonte primária pra DD.

Ordem de fontes (gratuitas e estáveis primeiro):

1. **consultasocio.com** — busca por nome com sócios já indexados.
   - URL: `https://www.consultasocio.com/q/sa/<slug-do-nome-em-kebab-case>`
   - Ex.: `https://www.consultasocio.com/q/sa/claudia-andreia-da-conceicao-fernandes`
   - WebFetch retorna lista de empresas com CNPJ, papel, cidade, status
2. **minhareceita.org** — API JSON pública e gratuita (sem auth) com dados completos de cada CNPJ.
   - URL: `https://minhareceita.org/<CNPJ_sem_pontuacao>`
   - Retorna: razão social, nome fantasia, situação cadastral, datas, capital, CNAE, endereço, **QSA completo** (todos os sócios + qualificação + data entrada)
3. **cnpj.biz** e **cnpja.com** — backup. Costumam dar 402 (paywall) ou 429 (rate limit). Não insistir.

Pra cada empresa achada na consultasocio, OBRIGATORIAMENTE cruzar com minhareceita.org pra confirmar:
- Situação cadastral (ATIVA / BAIXADA / INAPTA / SUSPENSA)
- Demais sócios (revela rede societária)
- Capital social e endereço (consistência com perfil declarado)
- Data de baixa (se inativa) — histórico revela padrão

Listar tanto empresas **ativas** quanto **baixadas/inativas** em tabela separada — abandono ou falência repetida é sinal.

**3b — Demais buscas (web aberta, mídia, processos)**

1. **WebSearch** ou **mcp__serpapi__search** com queries do tipo:
   - `"NOME COMPLETO"`
   - `"NOME COMPLETO" linkedin`
   - `"NOME COMPLETO" processo`
   - `"NOME COMPLETO" OAB OR CRM OR CRC`
   - `"NOME COMPLETO" trabalhista OR reclamação`
   - `"NOME COMPLETO" dívida OR penhora OR protesto`
2. **WebFetch** nos links do Escavador que retornaram match (passo 2) pra extrair perfil resumido.
3. Se houver CPF, montar query `"NOME" "CPF parcial"` (ex.: `"048.***.781-**"`).

Limitar a 8-12 buscas web no total (custo de contexto). Anotar achados:
- **Vínculos societários** (atuais + históricos) — seção dedicada obrigatória
- Vínculos profissionais públicos
- Educação / formação
- Mídia (entrevistas, prêmios, reportagens)
- Conselhos profissionais (registro ativo?)
- Sinais de alerta (sanções, processos públicos, controvérsias)

### Passo 4 — Montar JSON do dossiê (schema do `/documento`)

Reusa o `build.py` do `/documento` — mesmo template Singular. Schema esperado:

```json
{
  "titulo_curto": "BACKGROUND CHECK",
  "titulo": "<NOME COMPLETO>",
  "subtitulo": "Dossiê reputacional — <propósito>",
  "empresa": "Singular",
  "autor": "Pedro Miranda — CTO Singular Group",
  "data": "<data por extenso>",
  "tldr": "<2-4 frases: panorama geral — limpo? sinais de alerta? recomendação>",
  "secoes": [
    {
      "titulo": "1. Identidade & dados públicos",
      "paragrafos": ["Nome completo, idade aparente, cidade, profissão (se identificada na busca)."],
      "tabelas": [
        {
          "colunas": ["Campo", "Valor", "Fonte"],
          "linhas": [
            ["Nome", "<nome>", "informado"],
            ["Profissão", "<inferida>", "<link>"],
            ["Cidade base", "<inferida>", "<link>"],
            ["LinkedIn", "<url>", "Google"],
            ["Conselho", "<OAB/CRM/...>", "<link>"]
          ]
        }
      ]
    },
    {
      "titulo": "2. Processos judiciais — varredura por instância",
      "paragrafos": ["Resultado da consulta automatizada e dos links pra busca manual em cada tribunal. Após LGPD (2020), busca por nome em 1º grau é restrita em vários TJs — links levam ao formulário onde o usuário pode completar com CPF."],
      "tabelas": [
        {
          "colunas": ["Tribunal/Fonte", "Status", "Achados", "Link"],
          "linhas": [
            ["Escavador", "<ok|vazio|links-only>", "<n>", "<url>"],
            ["STF", "links-only", "—", "<url>"],
            ["STJ", "links-only", "—", "<url>"],
            ["TST/PJe-JT (Trabalhista)", "links-only", "—", "<url>"],
            ["TJDFT", "links-only", "—", "<url>"],
            ["TJSP e-SAJ", "links-only", "—", "<url>"],
            ["CNJ Consulta Unificada", "links-only", "—", "<url>"]
          ]
        }
      ],
      "destaque": "<se Escavador retornou matches, citar os principais aqui>"
    },
    {
      "titulo": "3. Mídia, redes e presença pública",
      "paragrafos": ["Resumo do que apareceu em Google/notícias/LinkedIn/etc."],
      "listas": [
        {"tipo": "bullet", "itens": ["LinkedIn — <url>", "Notícia X — <url>", "Entrevista Y — <url>"]}
      ]
    },
    {
      "titulo": "4. Vínculos societários & profissionais (OBRIGATÓRIO)",
      "paragrafos": ["Varredura via consultasocio.com (busca por nome) + minhareceita.org (detalhes por CNPJ). Listar TODAS as empresas — ativas e baixadas — com QSA completo, situação cadastral, capital, datas e endereços."],
      "tabelas": [
        {
          "colunas": ["Razão social", "Nome fantasia", "CNPJ", "Papel", "Status", "Início", "Capital", "Cidade/UF"],
          "linhas": [
            ["<razao social>", "<fantasia>", "<cnpj>", "<sócio-administrador>", "ATIVA", "<dd/mm/aaaa>", "R$ <valor>", "<cidade/uf>"]
          ]
        }
      ],
      "listas": [
        {"tipo": "bullet", "itens": ["Demais sócios das PJs ativas: <nome — qualificação>", "Empresas baixadas/inativas: <CNPJ + data baixa>", "Conselhos profissionais (OAB/CRM/CRC/etc.): <status>"]}
      ],
      "destaque": "<observação relevante: única sócia? mesma data de constituição em múltiplas PJs? rede societária com mesmo grupo de sócios? padrão de baixas?>"
    },
    {
      "titulo": "5. Sanções, listas restritivas e PEP",
      "paragrafos": ["Verificação em CEIS, CNEP, TCU inelegíveis, PEP."],
      "tabelas": [
        {
          "colunas": ["Lista", "Status", "Link"],
          "linhas": [
            ["Portal Transparência — CEIS", "<sem registro / com registro>", "<url>"],
            ["Portal Transparência — CNEP", "<...>", "<url>"],
            ["TCU — Inelegíveis", "<...>", "<url>"],
            ["PEP (politicamente exposta)", "<...>", "—"]
          ]
        }
      ]
    },
    {
      "titulo": "6. Análise consolidada",
      "paragrafos": [
        "Avaliação geral: limpo / sinais de atenção / sinais críticos.",
        "Pontos a confirmar com o titular antes de fechar contrato/parceria/contratação."
      ],
      "destaque": "<recomendação em uma frase: 'Prosseguir', 'Prosseguir com salvaguardas', 'Não prosseguir sem esclarecimento prévio'>"
    },
    {
      "titulo": "7. Fontes consultadas (todos os links)",
      "paragrafos": ["Lista completa pra reprodutibilidade da pesquisa. Cada link foi consultado em <data> e o estado pode ter mudado."],
      "tabelas": [
        {
          "colunas": ["#", "Fonte", "URL"],
          "linhas": [["1", "<fonte>", "<url>"]]
        }
      ]
    }
  ],
  "proximos_passos": [
    "Se DD parceiro: confirmar dúvidas com o titular antes de assinar.",
    "Se candidato vaga: levar pontos de atenção pra entrevista final.",
    "Reexecutar a busca em 6 meses se a relação seguir."
  ]
}
```

### Passo 5 — Gerar o .docx

```bash
mkdir -p ~/Desktop/backgroundcheck
python ~/.claude/skills/documento/build.py /tmp/bgcheck-<slug>.json \
  ~/Desktop/backgroundcheck/bgcheck-<slug>.docx
```

Onde `<slug>` é o nome em kebab-case sem acento (ex: "Pedro Roberto Miranda" →
`pedro-roberto-miranda`).

### Passo 6 — Entregar no chat

Resposta curta:

```
✅ Background check gerado: <NOME>

Arquivo: C:\Users\teste\Desktop\backgroundcheck\bgcheck-<slug>.docx
Fontes consultadas: <N>  |  Achados ativos: <M>  |  Sinais de alerta: <K>

Veredito: <prosseguir | atenção | não prosseguir>
TL;DR: <frase única>
```

**NÃO faz upload automático pro Drive Zel** (diferente do `/contrato` e `/documento`).
Background check pode ter dado sensível — usuário decide se quer compartilhar. Se pedir,
seguir passo 6 do `/documento` (upload + share + WhatsApp).

## Regras críticas

**Conteúdo:**
- NUNCA inventar achado. Se não retornou nada, escrever "Sem matches públicos — reexecutar manualmente nos links abaixo".
- NUNCA marcar alguém como PEP/sancionado sem o link da fonte oficial.
- Sempre citar **data da consulta** — fontes mudam.
- Quando ambíguo (homônimo): listar TODOS os matches plausíveis e marcar `[possível homônimo]`.

**Privacidade:**
- O `.docx` fica local. NÃO subir pro Drive sem confirmação explícita do usuário.
- NÃO incluir CPF completo no documento — usar `***.***.***-XX` mascarado.
- NUNCA logar CPF no chat — só no JSON local.

**Limitações conhecidas (documentar no relatório):**
- API pública DataJud não permite busca por nome (LGPD)
- TJs estaduais pós-LGPD frequentemente exigem CPF além do nome
- Escavador free tier limita matches públicos (paid tier dá detalhe completo)
- Homônimos são problema real — sem CPF, é melhor pedir
- Diários da Justiça antigos (pré-2015) têm cobertura irregular

## Arquivos da skill

```
~/.claude/skills/backgroundcheck/
├── SKILL.md                    (este arquivo)
├── scripts/
│   └── search.py               (busca multi-fonte; saída JSON)
└── example-output.json         (referência de schema do dossiê)
```

Reusa do `/documento`:
- `~/.claude/skills/documento/build.py` — gerador .docx
- `~/.claude/skills/pop/template.docx` — template oficial Singular
- `~/.claude/skills/documento/assets/logo-singular.png` — logo

## Diferença das skills irmãs

| Skill | Foco |
|-------|------|
| `/contrato` | Geração de contrato jurídico Singular |
| `/prospect` | Prospecção comercial de empresas em quadra |
| `/documento` | Documento formal genérico (estratégia, memo) |
| `/backgroundcheck` | **Dossiê reputacional de pessoa física** |

## Referências externas (para consulta manual)

- Escavador: https://www.escavador.com
- CNJ Consulta Unificada: https://www.cnj.jus.br/consultas-publicas/
- DataJud Wiki: https://datajud-wiki.cnj.jus.br/api-publica/
- Portal Transparência (sanções): https://portaldatransparencia.gov.br/sancoes
- TCU inelegíveis: https://contas.tcu.gov.br/ords/f?p=INABILITADO:5
