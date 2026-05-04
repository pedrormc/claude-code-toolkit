# /documento — Documento Formal Singular (genérico)

Skill do Claude Code que transforma texto livre (notas, brain-dump, conversa de WhatsApp, draft de e-mail) em um **documento formal `.docx`** com a identidade visual da Singular Group — fonte Urbanist, logo no topo, paleta preto/branco — e (opcionalmente) faz upload pra pasta no Google Drive e dispara o link via WhatsApp pelo Evolution API.

Diferente de `/ata` (reunião) e `/pop` (processo operacional), o `/documento` é o **schema genérico**: serve pra estratégia, briefing, memo, plano, análise, RFC, one-pager, decisão, ou qualquer outro doc que precise sair limpo e com a marca.

## O que essa skill faz

1. **Analisa** texto livre e infere a estrutura (tipo, seções, tópicos, listas, tabelas, callouts).
2. **Aplica norma culta do português** (acentuação, smart quotes, travessões).
3. **Gera `.docx`** em Urbanist com a logo Singular no topo, via `python-docx`.
4. **(Opcional) Sobe no Google Drive** numa pasta configurada e auto-compartilha com seu e-mail pessoal.
5. **(Opcional) Manda o link via WhatsApp** usando uma instância Evolution.

## Estrutura

```
skills/documento/
├── README.md                    (este arquivo — para humanos)
├── SKILL.md                     (instruções para o Claude Code — fluxo de 8 passos)
├── build.py                     (gerador .docx — Python + python-docx)
├── example-content.json         (exemplo válido do schema)
├── secrets.local.json.example   (template de config local — NÃO commitar a versão preenchida)
├── .gitignore                   (exclui secrets.local.json e artefatos)
├── assets/
│   ├── logo-singular.png        (logo oficial — embutida no topo do .docx)
│   ├── logo-singular.svg        (versão vetorizada — referência)
│   └── isotipo-singular.png     (variação compacta)
└── references/
    └── accents.md               (ponteiro para o accents.md compartilhado)
```

## Dependências

- **Python 3.10+** com `python-docx` (`pip install python-docx`).
- **Skill `/pop`** instalada no mesmo diretório irmão — o `build.py` reutiliza o `template.docx` oficial em `~/.claude/skills/pop/template.docx` (mesma seção, margens e fonte Urbanist da Singular).
- **MCP `google-drive`** configurado no Claude Code (opcional, para o passo de upload).
- **Node.js** + script `~/.claude/scripts/whatsapp-send.js` (já incluso no toolkit) para o passo de WhatsApp.
- **Instância Evolution API** acessível (opcional, só se quiser disparar mensagem automática).

## Setup (passo a passo)

### 1. Instalar a skill

Copie o diretório `skills/documento/` para `~/.claude/skills/documento/`. Se você usa o `install.sh` deste toolkit, ele já cuida disso.

### 2. Garantir o template Singular

A skill depende de `~/.claude/skills/pop/template.docx`. Se você ainda não tem a skill `/pop`, instale-a também (também faz parte deste toolkit em `skills/pop/`).

### 3. Configurar credenciais locais (opcional — só se quiser auto-upload e WhatsApp)

```bash
cp ~/.claude/skills/documento/secrets.local.json.example ~/.claude/skills/documento/secrets.local.json
```

Edite `secrets.local.json` e preencha:

- `drive.zel_folder_id` — ID da pasta Drive de destino. Pra achar: abra a pasta no Drive, copie o trecho final da URL (`drive.google.com/drive/folders/<este_id>`).
- `drive.auto_share_email` — seu e-mail Gmail pessoal (o MCP google-drive geralmente roda numa conta de serviço diferente; sem auto-share você não consegue abrir o link).
- `whatsapp.evolution_api_url` — URL base da sua instância Evolution.
- `whatsapp.evolution_instance` — nome da instância (ex.: `Zel3`).
- `whatsapp.evolution_api_key` — API key da instância.
- `whatsapp.destination_number` — número padrão (formato `55DDDNNNNNNNNN`).
- `whatsapp.contacts` — dicionário com outros contatos pra resolver "manda pro fulano".

**Nunca** commite o `secrets.local.json`. O `.gitignore` da skill já bloqueia.

### 4. Pronto

No Claude Code:

```
/documento

<cola aqui o texto bagunçado / brain-dump / draft que você quer transformar em doc>
```

A skill:
- Analisa, estrutura, gera `.docx`
- Sobe no Drive na pasta configurada (se config presente)
- Auto-compartilha com seu e-mail
- Manda o link no seu WhatsApp (se config presente)
- Devolve no chat o caminho local + link Drive

Sem `secrets.local.json`, a skill ainda funciona: gera o `.docx` localmente e pula os passos de Drive e WhatsApp.

## Identidade visual aplicada

- **Template `.docx`** compartilhado com `/pop` e `/ata` — header/footer/margens consistentes em todos os docs Singular
- **Fonte Urbanist** em todo o corpo (ascii/hAnsi/cs/eastAsia)
- **Logo Singular vetorizada** centralizada no topo (1.8")
- **Paleta:**
  - Texto: preto `#1C1C1C` sobre branco
  - Cinza médio `#555555` para metadados
  - Cinza fundo `#F2F2F2` para callouts e TL;DR
  - Cabeçalho de tabela: preto `#1C1C1C` com texto branco
- **Linha horizontal cinza fina** separando o cabeçalho do corpo

> ⚠️ Não edite o `template.docx` nem substitua a logo. Mudanças quebram a identidade compartilhada das três skills (`/pop`, `/ata`, `/documento`).

## Schema do `content.json` (resumo)

Campos obrigatórios: `titulo`, `secoes` (com pelo menos 1 seção e 1 parágrafo).

Cada seção pode conter qualquer combinação de:

- `paragrafos` — lista de strings
- `listas` — bullets ou numbered
- `tabelas` — colunas + linhas
- `destaque` — callout em caixa cinza
- `subsecoes` — recursivo, até 3 níveis de heading

Campos opcionais no topo: `titulo_curto`, `subtitulo`, `empresa`, `autor`, `destinatario`, `data`, `tldr`, `conclusao`, `proximos_passos`, `referencias`, `autor_rodape`.

Veja `example-content.json` para um JSON completo e funcional.

> ❗ NÃO existe campo `assinaturas` com linha de assinatura — bloco de assinatura formal não faz sentido em docs internos (estratégia, memo, briefing). Se você precisa de assinaturas, use `/ata` ou `/contrato`.

## Diferença das skills irmãs

| Skill | Quando usar |
|-------|-------------|
| `/ata` | Reunião com participantes, decisões e encaminhamentos |
| `/pop` | Processo Operacional Padrão com passo-a-passo executável |
| `/contrato` | Documento jurídico (NDA, MOU, prestação de serviços) |
| `/tese-investimento` | Tese de investimento estruturada |
| **`/documento`** | **Tudo o resto** — estratégia, memo, briefing, plano, análise, RFC, one-pager |

## Segurança

- `secrets.local.json` nunca vai pro git (`.gitignore` da skill bloqueia).
- API keys nunca aparecem em logs ou no chat — passadas só por env var pro `whatsapp-send.js`.
- Antes de mandar conteúdo sensível por WhatsApp, a skill confirma com você.
- O Claude (rodando a skill) não tem permissão de editar `secrets.local.json` — só lê.

## Licença

Mesma do toolkit (ver `LICENSE` na raiz).

## Autoria

Singular Group — Pedro Roberto Miranda (CTO)
