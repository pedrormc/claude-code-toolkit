---
name: pdf
description: Transforma texto livre (notas, draft, brain-dump, áudio transcrito, conversa de WhatsApp) em um documento PDF final com identidade visual da Singular (logo no topo de cada página, fonte Urbanist, paleta preto/branco/cinza). Schema flexível para qualquer tipo de documento — relatório, proposta, dossiê, briefing, memo, análise, decisão, one-pager. Aplica norma culta do português. Use quando o usuário digitar /pdf, ou pedir "gera um PDF", "monta um PDF", "PDF da Singular", "PDF pra cliente", "PDF pra apresentar", "manda em PDF".
---

# /pdf — Documento PDF final com identidade Singular

Converte texto livre, brain-dump, anotações, áudio transcrito ou rascunho em um
**documento PDF final** com a identidade visual da Singular. É a versão
"apresentável" — pronto pra cliente, sócio, fornecedor ou board.

Compartilha o **mesmo schema** da skill `/documento` (.docx), mas produz PDF
imutável em vez de .docx editável.

## Quando usar `/pdf` vs `/documento`

| Caso | Use |
|------|-----|
| Documento interno colaborativo, ainda em revisão | `/documento` (.docx) |
| Versão final para apresentar a cliente / sócio / fornecedor | **`/pdf`** |
| Relatório, dossiê, proposta comercial | **`/pdf`** |
| Memo, brainstorm, RFC, decisão interna | `/documento` |
| Algo que precisa ser editado depois | `/documento` |
| Algo que precisa ser imutável e ter aparência polida | **`/pdf`** |

Os dois usam o mesmo `content.json` — se mudar de ideia, pode gerar o outro
formato sem refazer o JSON.

## Quando usar

Invoque quando o usuário:
- Digitar `/pdf` seguido de texto a estruturar
- Pedir "gera um PDF", "monta um PDF", "manda em PDF"
- Pedir "PDF da Singular", "PDF pra cliente", "PDF pra apresentar"
- Pedir um relatório, dossiê, proposta ou análise para apresentação externa
- Entregar um áudio/transcrição/brain-dump e pedir versão pronta pra cliente

**Não usar quando:**
- For documento editável colaborativo → `/documento`
- For ata de reunião → `/ata` (gera .docx, converter depois se precisar PDF)
- For POP (processo operacional padrão) → `/pop` (gera .docx)
- For contrato → `/contrato`
- For tese de investimento → `/tese-investimento`
- For apresentação de slides → `/slide`

## Como a skill funciona

1. Você **analisa** o texto e infere a estrutura natural (tipo, seções, tópicos)
2. Você **escreve** `content.json` com a estrutura
3. Você **corrige acentuação** aplicando norma culta
4. Você **executa** `python build.py content.json saida.pdf`
5. O `build.py` renderiza o PDF com a identidade Singular (logo, Urbanist,
   paleta, tabelas com header preto, callouts cinza)
6. Você **sobe** o PDF na pasta Zel do Drive + **envia** o link via WhatsApp Zel3

## Arquivos da skill

```
~/.claude/skills/pdf/
├── SKILL.md              (este arquivo)
├── build.py              (gerador PDF — não editar sem testar)
├── example-content.json  (exemplo de JSON válido — referência de estrutura)
└── assets/
    ├── logo-singular.png     (logo oficial — embutida no topo de cada página)
    ├── logo-singular.svg     (versão vetorizada — referência)
    ├── isotipo-singular.png  (variação compacta, reserva)
    └── fonts/
        └── Urbanist-Regular.ttf  (fonte oficial Singular)
```

**Dependência única:** `reportlab` (`pip install reportlab`). Não precisa
de Word, LibreOffice ou pandoc — gera PDF nativamente.

**Configuração compartilhada:** os secrets de Drive/WhatsApp ficam em
`~/.claude/skills/documento/secrets.local.json` e são reaproveitados (não
duplicar).

## Fluxo de execução (7 passos — NÃO pule etapas)

### Passo 1 — Inferir o tipo e estrutura

A partir do texto livre, identifique:

| Inferência | Como detectar |
|------------|---------------|
| `tipo` | "relatório", "proposta", "dossiê", "briefing", "memo", "análise", "diagnóstico", "one-pager" |
| `titulo_curto` | Etiqueta no topo (ex.: "RELATÓRIO", "PROPOSTA", "DOSSIÊ") |
| `titulo` | Nome principal do documento |
| `subtitulo` | Linha secundária (opcional) |
| `autor` | Quem escreve (default: "Singular Group") |
| `destinatario` | Pra quem é (em PDF cliente-facing, quase sempre presente) |
| `data` | Data do doc — se omisso, data atual por extenso |
| `tldr` | Frase ou parágrafo curto resumindo tudo — vai como "RESUMO EXECUTIVO" no PDF |
| `secoes` | Blocos lógicos — discussão, dados, achados, recomendações |

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
  "titulo_curto": "RELATÓRIO",
  "titulo": "Relatório de Cliente Oculto",
  "subtitulo": "Diagnóstico de loja — cardápio, atendimento, operação",
  "empresa": "Singular",
  "autor": "Singular Group",
  "destinatario": "Equipe gestora da loja",
  "data": "15 de maio de 2026",
  "tldr": "Resumo executivo em 2-4 linhas. Aparece no topo do PDF em caixa cinza com borda preta.",
  "secoes": [
    {
      "titulo": "1. Seção",
      "paragrafos": ["Texto corrido."],
      "listas": [{"tipo": "bullet", "itens": ["item A", "item B"]}],
      "tabelas": [
        {
          "colunas": ["Frente", "Ação", "Prazo"],
          "linhas": [["Cardápio", "Redimensionar", "7 dias"]]
        }
      ],
      "destaque": "Frase de impacto — vira callout cinza com borda preta.",
      "subsecoes": [
        {"titulo": "1.1 Subsecção", "paragrafos": ["..."]}
      ]
    }
  ],
  "conclusao": "Parágrafo final.",
  "proximos_passos": ["Ação 1 — responsável — prazo"],
  "referencias": ["Fonte 1", "Fonte 2"],
  "autor_rodape": "Singular Group · Relatório · 15/05/2026"
}
```

**Tipos de lista:** `"bullet"` (default) ou `"numbered"`.

**Nomenclatura e estilo:**
- Títulos de seção: numere quando houver mais de 3 seções (`1.`, `2.`, `3.`)
- Parágrafos curtos (2-5 frases) — preferir quebrar a empilhar texto longo
- Use `destaque` para frases-chave (decisão, alerta, conclusão de seção)
- Use `tabelas` quando houver dados comparativos (frente × ação × prazo)
- `tldr` é a primeira coisa que aparece — não deixe vazio se conseguir extrair

### Passo 4 — Executar o gerador

No diretório de trabalho do usuário:

```bash
python ~/.claude/skills/pdf/build.py content.json pdf-<slug>.pdf
```

Onde `<slug>` é o título em kebab-case sem acentos.

**Alternativas de invocação:**
- Windows bash: `python /c/Users/teste/.claude/skills/pdf/build.py content.json pdf-X.pdf`
- PowerShell: `python "$env:USERPROFILE\.claude\skills\pdf\build.py" content.json pdf-X.pdf`

**Dependência:** `reportlab` (instalar uma vez com `pip install reportlab`).

### Passo 5 — Validar

- [ ] Arquivo `.pdf` criado com tamanho > 50 KB
- [ ] Nenhum erro na stdout (exceto "Gerado: ...")
- [ ] Sem campos "A definir" não-sinalizados
- [ ] Conferir nº de páginas razoável (rodar `pdftoppm` opcionalmente para preview)

### Passo 6 — Upload Drive na pasta Zel (com auto-share OBRIGATÓRIO)

O MCP `google-drive` está conectado na conta de serviço `techsingulargroup@gmail.com`,
não na conta pessoal do Pedro. Sem auto-share, o link retorna "acesso negado".

**Antes do upload:** ler `~/.claude/skills/documento/secrets.local.json` para
pegar `drive.zel_folder_id`, `drive.auto_share_email`, e a config de WhatsApp
do passo 7. Esse arquivo está fora do git e contém credenciais — não logue
o conteúdo. **Não duplicar este arquivo dentro da skill /pdf** — usar o
mesmo da `/documento`.

**Sequência fixa, sem exceção:**

1. **Upload** via `mcp__google-drive__uploadFile`:
   - `localPath`: path absoluto do `.pdf`
   - `parentFolderId`: valor de `drive.zel_folder_id` (pasta Zel — atual: `10ARKUMWyFzVkdaPEWLYC9OXWqm0ywS6e`)
   - `convertToGoogleFormat: false`
   - `name`: pode usar nome humano com data, ex.: "Relatório Cliente Oculto — Singular (2026-05-15).pdf"
   - Capturar o `fileId` e o `link` retornados
2. **Compartilhar** imediatamente via `mcp__google-drive__shareFile`:
   - `fileId`: id do passo 1
   - `emailAddress`: valor de `drive.auto_share_email`
   - `role: "writer"`
   - `sendNotificationEmail: false`

Não subir o `content.json` intermediário.

### Passo 7 — Enviar link via WhatsApp (Evolution API · instância Zel3)

Disparar mensagem com o link do Drive automaticamente após o upload.
Lê config de `~/.claude/skills/documento/secrets.local.json` → `whatsapp.*`.

**Comando (bash-friendly):**

```bash
CFG=~/.claude/skills/documento/secrets.local.json
EVOLUTION_API_URL=$(jq -r .whatsapp.evolution_api_url $CFG) \
EVOLUTION_INSTANCE=$(jq -r .whatsapp.evolution_instance $CFG) \
EVOLUTION_API_KEY=$(jq -r .whatsapp.evolution_api_key $CFG) \
node ~/.claude/scripts/whatsapp-send.js text \
  --number "$(jq -r .whatsapp.destination_number $CFG)" \
  --message "📄 <Título>\n<link Drive>\n\n(<tipo>, <N> seções)"
```

**Comando equivalente em PowerShell:**

```powershell
$cfg = Get-Content "$env:USERPROFILE\.claude\skills\documento\secrets.local.json" | ConvertFrom-Json
$env:EVOLUTION_API_URL = $cfg.whatsapp.evolution_api_url
$env:EVOLUTION_INSTANCE = $cfg.whatsapp.evolution_instance
$env:EVOLUTION_API_KEY  = $cfg.whatsapp.evolution_api_key
node "$env:USERPROFILE\.claude\scripts\whatsapp-send.js" text `
  --number $cfg.whatsapp.destination_number `
  --message "📄 <Título>`n<link>"
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
- Se o PDF tiver dados sensíveis (financeiro confidencial, dados pessoais),
  PERGUNTAR antes de mandar
- Se o número de destino for ambíguo, PERGUNTAR antes de enviar

### Passo 8 — Entregar ao usuário no chat

Resposta curta em 4 linhas:
1. Caminho absoluto do `.pdf` gerado
2. **Link Drive (pasta Zel)**
3. Confirmação do envio WhatsApp (✅ enviado para <número> via Zel3, ou ❌ falhou + motivo)
4. Resumo: tipo, título, nº de seções, campos "A definir" se houver

## Regras críticas

**Identidade visual (não negociável):**
- Logo Singular centralizada no topo de **cada página** (3.5 cm de largura)
- Paleta: corpo preto (`#1C1C1C`) sobre branco; callouts em cinza claro
  (`#F2F2F2`) com borda preta à esquerda; cabeçalho de tabela preto com
  texto branco; linhas alternadas em cinza claro
- Fonte: **Urbanist** em todo o corpo (registrada de `assets/fonts/`)
- Linha divisória fina acima da numeração de página, em cinza claro
- **NÃO substituir a logo nem editar paleta sem aprovação explícita**

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
| `/documento` | .docx | Doc editável genérico (estratégia, memo, briefing) |
| **`/pdf`** | **.pdf** | **Doc final pra apresentar (relatório, proposta, dossiê)** |
| `/ata` | .docx | Reunião com participantes, decisões, encaminhamentos |
| `/pop` | .docx | Processo Operacional Padrão com passo-a-passo executável |
| `/contrato` | .docx | Documento jurídico (NDA, MOU, prestação) |
| `/tese-investimento` | .docx | Tese de investimento estruturada |
| `/slide` | .html | Apresentação de slides interativa |

## Referência

- Exemplo completo: `example-content.json`
- Acentuação: `~/.claude/skills/pop/references/accents.md`
- Schema irmão (.docx): `~/.claude/skills/documento/SKILL.md`
- Brand guidelines: `C:\Users\teste\Desktop\dondon\pop\Brand Guidelines Singular (2).pdf`
