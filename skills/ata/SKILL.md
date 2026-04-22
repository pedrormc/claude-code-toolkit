---
name: ata
description: Transforma texto livre (transcrição, notas, resumo) de uma reunião em Ata de Reunião formatada como .docx espelhando o template oficial da Singular (fonte Urbanist, header/footer com logo, paleta preto/branco). Organiza em tópicos importantes com decisões, encaminhamentos (responsável + prazo) e próxima reunião. Aplica norma culta do português. Use quando o usuário digitar /ata seguido de texto sobre uma reunião, ou pedir "criar ata", "documentar reunião", "transformar essas notas em ata".
---

# /ata — Ata de Reunião (Singular)

Converte texto livre sobre uma reunião (transcrição, anotações, resumo oral) em uma
**Ata de Reunião** profissional em **.docx**, espelhando o template oficial da Singular
e aplicando norma culta do português.

## Quando usar

Invoque quando o usuário:
- Digitar `/ata` seguido de texto descrevendo uma reunião
- Pedir para "criar ata", "documentar essa reunião", "fazer ata de reunião"
- Entregar transcrições/notas/áudio transcrito que precisem virar ata formal
- Resumir uma call em tópicos importantes com decisões e encaminhamentos

## Como a skill funciona

1. Você **analisa** o texto e extrai estrutura de reunião (participantes, tópicos, decisões, ações)
2. Você **escreve um arquivo JSON** (`content.json`) com a estrutura
3. Você **corrige acentuações** no JSON aplicando norma culta
4. Você **executa** `python build.py content.json ata-saida.docx`
5. O script `build.py` abre o template oficial da Singular (herdado de `/pop`), limpa o
   corpo, e reconstrói o documento com a ata, preservando header/footer/identidade visual

## Arquivos da skill

```
~/.claude/skills/ata/
├── SKILL.md              (este arquivo)
├── build.py              (gerador .docx — não editar sem testar)
├── example-content.json  (exemplo de JSON válido — referência de estrutura)
├── assets/
│   ├── template.docx         (template oficial Singular — fonte Urbanist, header/footer)
│   ├── logo-singular.png     (logo oficial Singular — fundo claro, embutida no topo)
│   ├── logo-singular.svg     (versão vetorizada — referência)
│   └── isotipo-singular.png  (isotipo — variação compacta, reserva)
└── references/
    └── accents.md        (referência de acentuação PT-BR — norma culta)
```

Template `.docx` em `assets/template.docx` (fonte Urbanist, margens e seção da
identidade Singular). A logo vetorizada é inserida programaticamente pelo
`build.py` no topo de cada ata, usando `assets/logo-singular.png`.

## Fluxo de execução (6 passos — NÃO pule etapas)

### Passo 1 — Analisar o texto de entrada

Extraia do texto fornecido:

| Campo JSON | O que buscar no texto |
|------------|----------------------|
| `titulo` | Assunto da reunião (ex.: "Alinhamento de Produto Q2") |
| `data` | Data da reunião — se omisso, data atual por extenso |
| `hora_inicio` / `hora_fim` | Horários — omita se não mencionado |
| `local` | Sala física, Google Meet, Zoom, Teams etc. |
| `tipo_reuniao` | Alinhamento, diário, kickoff, retrospectiva etc. |
| `participantes.presentes` | Lista "Nome — Cargo/Empresa" |
| `participantes.ausentes` | Lista com "(justificado)" ou "(não justificado)" |
| `pauta` | Itens que seriam discutidos (se mencionado) |
| `topicos` | Cada tópico importante discutido com discussão + decisões |
| `encaminhamentos` | Ações concretas com responsável e prazo |
| `proxima_reuniao` | Data/hora/pauta prevista (opcional) |
| `observacoes` | Texto livre final (opcional) |

**Regra crítica:** campos não presentes no texto → omitir do JSON. NUNCA invente
nomes, datas ou decisões. Se faltar informação crítica (data, participantes),
marque `"A definir"` e sinalize ao usuário na entrega.

### Passo 2 — Aplicar norma culta do português

Antes de gravar o JSON, revise toda a redação corrigindo acentuação conforme
`references/accents.md`.

**Palavras frequentes em ata que SEMPRE conferir:**
reunião, decisão, discussão, ação, encaminhamento, próxima, pauta, presentes,
ausentes, justificado, responsável, prazo, estratégia, objetivo, relatório,
deliberação, análise, síntese, até, já, só, também, será, serão, após, está,
três, você, atribuições.

**Smart quotes:** use aspas tipográficas (`"` e `"`) nos textos em português.
Use travessão (`—`) para inserções/pausas, não dois hifens (`--`).

### Passo 3 — Escrever o JSON

Escreva `content.json` no diretório de trabalho do usuário seguindo esta estrutura
(veja `example-content.json` para modelo completo):

```json
{
  "titulo_curto": "ATA",
  "titulo": "Reunião de [ASSUNTO]",
  "empresa": "Singular",
  "data": "16 de abril de 2026",
  "hora_inicio": "14:00",
  "hora_fim": "15:30",
  "local": "Google Meet",
  "tipo_reuniao": "Alinhamento de produto",
  "objetivo": "Frase curta que explica o propósito da reunião.",
  "participantes": {
    "presentes": ["Nome — Cargo", "Nome — Cargo"],
    "ausentes": ["Nome — Cargo (justificado)"]
  },
  "pauta": ["Tópico 1", "Tópico 2", "Tópico 3"],
  "topicos": [
    {
      "titulo": "Tópico 1 — Nome do Assunto",
      "discussao": ["parágrafo que resume a discussão", "outro parágrafo"],
      "decisoes": ["decisão tomada 1", "decisão tomada 2"],
      "tabelas": [
        {
          "colunas": ["Item", "Status"],
          "linhas": [["a", "b"]]
        }
      ]
    }
  ],
  "encaminhamentos": {
    "titulo": "Encaminhamentos",
    "linhas": [
      ["Ação", "Responsável", "Prazo"],
      ["Preparar briefing", "Pedro", "23/04"]
    ]
  },
  "proxima_reuniao": {
    "data": "23 de abril de 2026",
    "hora": "14:00",
    "local": "Google Meet",
    "pauta_prevista": ["Revisar briefing", "Definir stack"]
  },
  "observacoes": "Texto livre final, opcional.",
  "assinaturas": ["Pedro Roberto — CTO", "Fulano — PM"]
}
```

**Nomenclatura e estilo:**
- Títulos de tópico: `Tópico N — Nome Curto` (travessão `—`)
- Decisões começam com verbo no passado/imperativo: "Aprovado…", "Definido…", "Adiar…"
- Encaminhamentos: sempre com responsável nomeado e prazo concreto (data ou "sem prazo")
- Discussão em parágrafos curtos (1-3 frases) — resumir, não transcrever
- Se houver consenso explícito, registrar; se houver divergência, registrar também

**Seções opcionais:** `pauta`, `proxima_reuniao`, `observacoes`, `assinaturas`,
`tabelas` dentro de tópico — omita do JSON se não fizer sentido.

### Passo 4 — Executar o gerador

No diretório de trabalho do usuário:

```bash
python ~/.claude/skills/ata/build.py content.json ata-<slug>.docx
```

Onde `<slug>` é o assunto em kebab-case sem acentos
(ex.: "Alinhamento de Produto Q2" → `ata-alinhamento-produto-q2.docx`).

**Alternativas de invocação:**
- Windows bash: `python /c/Users/teste/.claude/skills/ata/build.py content.json ata-X.docx`
- PowerShell: `python "$env:USERPROFILE\.claude\skills\ata\build.py" content.json ata-X.docx`

**Dependência:** `python-docx` (já instalado globalmente no ambiente).

### Passo 5 — Validar

Após gerar, confirme:

- [ ] Arquivo `.docx` criado com tamanho > 50KB
- [ ] Nenhum erro na stdout (exceto o print "Gerado: ...")
- [ ] JSON não tem campos "A definir" desnecessários — se houver, sinalize

### Passo 6 — Entregar ao usuário

Resposta curta em 3 linhas:
1. Caminho absoluto do `.docx` gerado
2. Resumo: assunto, data, nº de tópicos, nº de encaminhamentos, campos "A definir"
3. Sugestão de próximo passo (abrir no Word, enviar aos participantes, converter para PDF)

## Regras críticas

**Identidade visual (não negociável):**
- Usa o mesmo `template.docx` de `/pop` (seção/margens/fonte Urbanist da Singular)
- Logo oficial vetorizada (`assets/logo-singular.png`, convertida do SVG oficial
  em `Desktop/dondon/pop/[SG] SINGULAR/LOGO SVG/`) inserida centralizada no topo
  pelo `build.py` via `run.add_picture(width=1.8in)`
- **NÃO editar o template nem substituir a logo** — mudanças quebram a identidade
- Paleta: cabeçalho de tabela preto (`#1C1C1C`) + texto branco, corpo preto sobre branco
- Fonte: Urbanist em todo o corpo (ascii/hAnsi/cs/eastAsia)

**Conteúdo:**
- NUNCA inventar nomes de participantes, datas, decisões ou prazos
- Resumir discussões em parágrafos curtos — ata não é transcrição literal
- Corrigir APENAS ortografia/acentuação, não alterar sentido das falas registradas
- Divergências devem ser registradas quando relevantes, não apagadas
- Quando houver ambiguidade, marcar `[verificar com autor]` inline no JSON

**Limites:**
- Mínimo: título + data + pelo menos 1 tópico
- Máximo recomendado: 10 tópicos (se for mais, considerar dividir em 2 atas)
- Tabela de encaminhamentos com mais de 12 linhas quebra visualmente — dividir

## Referência

- Exemplo completo: `example-content.json`
- Acentuação: `references/accents.md`
- Template oficial: `assets/template.docx` (imutável — use via `build.py`)
