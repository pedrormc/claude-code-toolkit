---
name: documento
bu: backoffice-tech
cross_bu: [consultorio-operacional, consultorio-comercial]
description: Transforma texto livre (notas, draft, brain-dump, conversa de WhatsApp, copy de email) em um documento formal .docx com identidade visual da Singular (fonte Urbanist, logo no topo, paleta preto/branco). Schema flexível para qualquer tipo de documento — estratégia, briefing, memo, plano, decisão, análise, RFC, one-pager. Aplica norma culta do português. Use quando o usuário digitar /documento, ou pedir "monta um documento", "organiza isso num doc", "transforma em documento", "documento bonito da Singular".
---

# /documento — Documento Formal Singular (genérico)

Converte texto livre, brain-dump, anotações ou rascunho em um **documento formal em .docx**
com a identidade visual da Singular. Diferente de `/ata` (reunião) e `/pop` (processo),
o `/documento` é o **schema genérico** — serve para estratégia, briefing, memo, plano,
análise, RFC, one-pager, decisão, ou qualquer outro doc que precise sair limpo e
com a marca.

## Quando usar

Invoque quando o usuário:
- Digitar `/documento` seguido de texto a estruturar
- Pedir "monta um documento", "organiza isso num doc", "transforma em documento formal"
- Entregar um brain-dump bagunçado e pedir versão limpa pra cliente / sócio / equipe
- Quiser um doc com a cara da Singular para qualquer finalidade que NÃO seja ata ou POP

**Não usar quando:**
- For ata de reunião → `/ata`
- For POP (processo operacional padrão) → `/pop`
- For contrato → `/contrato`
- For tese de investimento → `/tese-investimento`

## Como a skill funciona

1. Você **analisa** o texto e infere a estrutura natural (tipo, seções, tópicos)
2. Você **escreve** `content.json` com a estrutura
3. Você **corrige acentuação** aplicando norma culta
4. Você **executa** `python build.py content.json doc-saida.docx`
5. O `build.py` reaproveita o `template.docx` oficial (compartilhado com `/pop` e `/ata`)
   e reconstrói o documento preservando header/footer/identidade visual

## Arquivos da skill

```
~/.claude/skills/documento/
├── SKILL.md              (este arquivo)
├── build.py              (gerador .docx — não editar sem testar)
├── example-content.json  (exemplo de JSON válido — referência de estrutura)
├── assets/
│   ├── logo-singular.png     (logo oficial — embutida no topo)
│   ├── logo-singular.svg     (versão vetorizada — referência)
│   └── isotipo-singular.png  (variação compacta, reserva)
└── references/
    └── accents.md        (ponteiro para ~/.claude/skills/pop/references/accents.md)
```

Template `.docx` compartilhado: `~/.claude/skills/pop/template.docx`
(mesma seção/margens/fonte Urbanist da `/ata` e `/pop`).

## Fluxo de execução (7 passos — NÃO pule etapas)

### Passo 1 — Inferir o tipo e estrutura

A partir do texto livre, identifique:

| Inferência | Como detectar |
|------------|---------------|
| `tipo` | "estratégia", "briefing", "memo", "plano", "análise", "RFC", "decisão", "one-pager", "diagnóstico", "proposta" |
| `titulo_curto` | Etiqueta no topo (ex.: "ESTRATÉGIA", "BRIEFING", "MEMO") — derivada do tipo |
| `titulo` | Nome principal do documento |
| `subtitulo` | Linha secundária (opcional) |
| `autor` | Quem escreve (default: nome do usuário, se conhecido) |
| `destinatario` | Pra quem é (opcional) |
| `data` | Data do doc — se omisso, data atual por extenso |
| `tldr` | Frase ou parágrafo curto que resume tudo (sempre tente extrair) |
| `secoes` | Blocos lógicos do documento — discussão, dados, decisões, planos |

**Regra crítica:** campos não presentes no texto → omitir do JSON. NUNCA invente
nomes, datas, números ou conclusões. Se faltar info crítica, marque `"A definir"`
e sinalize ao usuário na entrega.

### Passo 2 — Aplicar norma culta do português

Antes de gravar o JSON, revise toda redação corrigindo acentuação conforme
`~/.claude/skills/pop/references/accents.md`.

**Smart quotes:** use aspas tipográficas (`"` e `"`).
Use travessão (`—`) para inserções/pausas, não dois hifens (`--`).

### Passo 3 — Escrever o JSON

Schema completo (todos os campos exceto `titulo` e `secoes` são opcionais):

```json
{
  "titulo_curto": "ESTRATÉGIA",
  "titulo": "Singular Group — Donos, Células & Metas",
  "subtitulo": "Estrutura organizacional para o próximo trimestre",
  "empresa": "Singular",
  "autor": "Pedro Miranda — CEO",
  "destinatario": "Sócios e líderes de célula",
  "data": "3 de maio de 2026",
  "tldr": "Frase curta ou parágrafo resumindo a tese central do documento.",
  "secoes": [
    {
      "titulo": "1. Decisão central",
      "paragrafos": [
        "Texto corrido do parágrafo 1.",
        "Texto corrido do parágrafo 2."
      ],
      "listas": [
        {
          "tipo": "bullet",
          "itens": ["item A", "item B", "item C"]
        }
      ],
      "tabelas": [
        {
          "colunas": ["Frente", "Dono", "Meta"],
          "linhas": [
            ["Marketing", "Adonai", "30 clientes"],
            ["Consultório", "Pedro Rocha", "150 clientes"]
          ]
        }
      ],
      "destaque": "Texto curto que vira callout em caixa cinza — para enfatizar a decisão.",
      "subsecoes": [
        {
          "titulo": "1.1 Subsecção",
          "paragrafos": ["..."]
        }
      ]
    }
  ],
  "conclusao": "Parágrafo de fechamento com a tese final.",
  "proximos_passos": [
    "Ação 1 — responsável — prazo",
    "Ação 2 — responsável — prazo"
  ],
  "referencias": [
    "Doc relacionado 1 — link ou caminho",
    "Doc relacionado 2"
  ],
  "autor_rodape": "Pedro Miranda — CEO Singular Group · 03/05/2026"
}
```

**Tipos de lista:** `"bullet"` (default) ou `"numbered"`.

**Nomenclatura e estilo:**
- Títulos de seção: numere quando houver mais de 3 seções (`1.`, `2.`, `3.`)
- Parágrafos curtos (2-5 frases) — preferir quebrar a empilhar texto longo
- Use `destaque` para callouts importantes (decisão final, frase-chave)
- Use `tabelas` quando houver dados comparativos (donos × metas, antes × depois)
- `tldr` é a primeira coisa que aparece — não deixe vazio se conseguir extrair

**Seções opcionais:** `subtitulo`, `autor`, `destinatario`, `tldr`, `conclusao`,
`proximos_passos`, `referencias`, `autor_rodape`. Cada seção pode ter qualquer
combinação de `paragrafos`, `listas`, `tabelas`, `destaque`, `subsecoes`.

**NÃO use bloco de "Assinaturas" com linhas de assinatura (`____`) em documentos
internos** — isso é feio e desnecessário em estratégia/memo/briefing. Use
`autor_rodape` para uma linha discreta no final ("Pedro Miranda — CEO · 03/05/2026").
Bloco formal de assinaturas só faz sentido em ata/contrato — usar `/ata` ou `/contrato`.

### Passo 4 — Executar o gerador

No diretório de trabalho do usuário:

```bash
python ~/.claude/skills/documento/build.py content.json doc-<slug>.docx
```

Onde `<slug>` é o título em kebab-case sem acentos
(ex.: "Singular Group — Donos & Células" → `doc-singular-donos-celulas.docx`).

**Alternativas de invocação:**
- Windows bash: `python /c/Users/teste/.claude/skills/documento/build.py content.json doc-X.docx`
- PowerShell: `python "$env:USERPROFILE\.claude\skills\documento\build.py" content.json doc-X.docx`

**Dependência:** `python-docx` (já instalado globalmente no ambiente).

### Passo 5 — Validar

- [ ] Arquivo `.docx` criado com tamanho > 50KB
- [ ] Nenhum erro na stdout (exceto "Gerado: ...")
- [ ] Sem campos "A definir" não-sinalizados

### Passo 6 — Upload Drive na pasta Zel (com auto-share OBRIGATÓRIO)

O MCP `google-drive` está conectado na conta de serviço `techsingulargroup@gmail.com`,
não na conta pessoal do Pedro. Sem auto-share, o link retorna "acesso negado".

**Antes do upload:** ler `~/.claude/skills/documento/secrets.local.json` para
pegar `drive.zel_folder_id`, `drive.auto_share_email`, e a config de WhatsApp
do passo 7. Esse arquivo está fora do git e contém credenciais — não logue
o conteúdo.

**Sequência fixa, sem exceção:**

1. **Upload** via `mcp__google-drive__uploadFile`:
   - `localPath`: path absoluto do `.docx`
   - `parentFolderId`: valor de `drive.zel_folder_id` (pasta Zel — atual: `10ARKUMWyFzVkdaPEWLYC9OXWqm0ywS6e`)
   - `convertToGoogleFormat: false`
   - Capturar o `fileId` e o `link` retornados
2. **Compartilhar** imediatamente via `mcp__google-drive__shareFile`:
   - `fileId`: id do passo 1
   - `emailAddress`: valor de `drive.auto_share_email`
   - `role: "writer"`
   - `sendNotificationEmail: false`

Não subir o `content.json` intermediário.

### Passo 7 — Enviar link via WhatsApp (Evolution API · instância Zel3)

Disparar mensagem com o link do Drive automaticamente após o upload.
Lê config de `secrets.local.json` → `whatsapp.*`.

**Comando (PowerShell-friendly):**

```powershell
$cfg = Get-Content "$env:USERPROFILE\.claude\skills\documento\secrets.local.json" | ConvertFrom-Json
$env:EVOLUTION_API_URL = $cfg.whatsapp.evolution_api_url
$env:EVOLUTION_INSTANCE = $cfg.whatsapp.evolution_instance
$env:EVOLUTION_API_KEY  = $cfg.whatsapp.evolution_api_key
node "$env:USERPROFILE\.claude\scripts\whatsapp-send.js" text `
  --number $cfg.whatsapp.destination_number `
  --message "📄 <Título do doc>`n<link>"
```

**Comando equivalente em bash:**

```bash
CFG=~/.claude/skills/documento/secrets.local.json
EVOLUTION_API_URL=$(jq -r .whatsapp.evolution_api_url $CFG) \
EVOLUTION_INSTANCE=$(jq -r .whatsapp.evolution_instance $CFG) \
EVOLUTION_API_KEY=$(jq -r .whatsapp.evolution_api_key $CFG) \
node ~/.claude/scripts/whatsapp-send.js text \
  --number "$(jq -r .whatsapp.destination_number $CFG)" \
  --message "📄 <Título>\n<link Drive>"
```

**Mensagem padrão (formato fixo):**

```
📄 <titulo do documento>
<link Drive>

(<tipo>, <N> seções)
```

**Regras de segurança:**
- NUNCA logar `EVOLUTION_API_KEY` na resposta — passe só por env var
- NUNCA mandar conteúdo do `secrets.local.json` por WhatsApp
- Se o doc tiver dados sensíveis (financeiro confidencial, dados pessoais),
  PERGUNTAR antes de mandar
- Se o número de destino for ambíguo (`destination_label` ainda diz "confirmar"),
  PERGUNTAR antes de enviar

### Passo 8 — Entregar ao usuário no chat

Resposta curta em 4 linhas:
1. Caminho absoluto do `.docx` gerado
2. **Link Drive (pasta Zel)**
3. Confirmação do envio WhatsApp (✅ enviado para <número> via Zel3, ou ❌ falhou + motivo)
4. Resumo: tipo, título, nº de seções, campos "A definir" se houver

## Regras críticas

**Identidade visual (não negociável):**
- Usa o `template.docx` oficial compartilhado (`/pop`, `/ata`, `/documento`)
- Logo Singular vetorizada inserida centralizada no topo (1.8 polegadas)
- Paleta: corpo preto sobre branco, callouts em cinza claro, cabeçalho de tabela
  preto (`#1C1C1C`) com texto branco
- Fonte: **Urbanist** em todo o corpo (ascii/hAnsi/cs/eastAsia)
- **NÃO editar o template nem substituir a logo**

**Conteúdo:**
- NUNCA inventar nomes, números, datas ou afirmações factuais
- Resumir e estruturar — não inflar nem inventar
- Corrigir APENAS ortografia/acentuação, preservar voz original
- Se o texto tiver linguagem informal forte (gírias, palavrão), suavize sem
  esterilizar (ex.: "tá ferrado" → "está em risco crítico")
- Quando houver ambiguidade, marcar `[verificar com autor]` inline no JSON

**Limites:**
- Mínimo: título + 1 seção com pelo menos 1 parágrafo
- Máximo recomendado: 12 seções (acima disso considerar dividir em múltiplos docs)
- Uma seção com >5 parágrafos longos → dividir em subseções

## Diferença das skills irmãs

| Skill | Saída | Quando |
|-------|-------|--------|
| `/ata` | .docx | Reunião com participantes, decisões e encaminhamentos |
| `/pop` | .docx | Processo Operacional Padrão com passo-a-passo executável |
| `/contrato` | .docx | Documento jurídico (NDA, MOU, prestação) |
| `/tese-investimento` | .docx | Tese de investimento estruturada |
| `/documento` | .docx | **Tudo o resto editável** — estratégia, memo, briefing, plano, análise |
| `/pdf` | **.pdf** | **Documento final pra apresentar a cliente / sócio / fornecedor** — mesmo schema do `/documento`, saída imutável |

## Referência

- Exemplo completo: `example-content.json`
- Acentuação: `~/.claude/skills/pop/references/accents.md`
- Template oficial: `~/.claude/skills/pop/template.docx` (imutável)
