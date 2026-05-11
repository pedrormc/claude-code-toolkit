---
name: pop
description: Transforma texto extenso em Processo Operacional Padrão (POP) formatado como .docx espelhando o template oficial da Singular (fonte Urbanist, header/footer com logo, paleta preto/branco com acentos selecionados). Aplica norma culta do português (acentuação correta) e estrutura formal de procedimento. Use quando o usuário digitar /pop seguido de texto descritivo de processo, metodologia ou fluxo.
---

# /pop — Processo Operacional Padrão (Singular)

Converte texto livre extenso em um POP profissional em **.docx** (formato Word),
espelhando o template oficial da Singular e aplicando norma culta do português.

## Quando usar

Invoque quando o usuário:
- Digitar `/pop` seguido de texto (geralmente extenso) descrevendo processo, metodologia, fluxo ou procedimento
- Pedir para "transformar em POP", "criar processo operacional padrão", "documentar esse procedimento"
- Entregar transcrições, briefings, walkthroughs que precisem virar doc formal

## Como a skill funciona

1. Você **analisa** o texto do usuário e extrai estrutura
2. Você **escreve um arquivo JSON** (`content.json`) com a estrutura
3. Você **corrige acentuações** no JSON aplicando norma culta
4. Você **executa** `python build.py content.json saida.docx`
5. O script `build.py` abre `template.docx` (que já tem header/footer/fontes Urbanist da Singular),
   limpa o corpo, e reconstrói o documento com o conteúdo fornecido, preservando toda a
   identidade visual do template oficial

## Arquivos da skill

```
~/.claude/skills/pop/
├── SKILL.md              (este arquivo)
├── build.py              (gerador .docx — não editar sem testar)
├── template.docx         (template oficial Singular com fonts/header/footer)
├── example-content.json  (exemplo de JSON válido — referência de estrutura)
└── references/
    └── accents.md        (lista exaustiva de acentuações PT-BR)
```

## Fluxo de execução (7 passos — NÃO pule etapas)

### Passo 1 — Analisar o texto de entrada

Extraia do texto fornecido:

| Campo JSON | O que buscar no texto |
|------------|----------------------|
| `titulo` | Nome do processo (ex.: "Processo Operacional de Vendas Recorrentes") |
| `versao` | Número da versão — se omisso, usar "1.0" |
| `data` | Data de emissão — se omisso, usar data atual por extenso ("15 de abril de 2026") |
| `objetivo` | Uma frase que responde "por que esse processo existe?" |
| `perfil_secao` | Seção introdutória com bullets (perfil do cliente, pré-requisitos, contexto) |
| `fluxo_titulo` | Ex.: "Fluxo em 8 Passos", "Procedimento", "Etapas do Processo" |
| `passos` | Array com cada passo/etapa, contendo título, parágrafos, tabelas, listas, ação final |
| `checklist` | Seção de checklist com sub-seções (ex.: "Antes" / "Durante" / "Após") |
| `contato` | Tabela de contatos/canais (opcional) |

**Regra crítica:** campos não presentes no texto → omitir do JSON ou marcar "A definir". NUNCA invente conteúdo.

### Passo 2 — Aplicar norma culta do português

Antes de gravar o JSON, revise toda a redação corrigindo acentuação conforme `references/accents.md`.

**Palavras de alta frequência que SEMPRE conferir:**
você, vocês, não, é, até, já, só, também, após, três, gestão, organização, execução,
situação, ação, reunião, estratégia, método, prática, diagnóstico, negócio, salário,
mínimo, máximo, último, próprio, mês, férias, indústria, clínica, médico, serviço,
período, técnico, título, análise, síntese, responsável, executável, disponível, nível.

**Smart quotes:** use aspas tipográficas (`"` e `"`) nos textos em português, não aspas retas.
Use travessão (`—`) para inserções/pausas, não dois hifens (`--`).

### Passo 3 — Escrever o JSON

Escreva o arquivo `content.json` no diretório de trabalho do usuário. Siga EXATAMENTE
a estrutura abaixo (veja `example-content.json` para modelo completo):

```json
{
  "titulo_curto": "POP",
  "titulo": "Processo Operacional de [NOME]",
  "empresa": "Singular",
  "versao": "1.0",
  "data": "15 de abril de 2026",
  "objetivo": "Frase com verbo no infinitivo que define o resultado esperado.",
  "perfil_secao": {
    "titulo": "Perfil do Cliente",
    "bullets": ["item 1", "item 2"]
  },
  "fluxo_titulo": "Fluxo em N Passos",
  "passos": [
    {
      "titulo": "Passo 1 — Nome do Passo",
      "paragrafos": ["texto introdutório opcional"],
      "tabelas": [
        {
          "colunas": ["Coluna A", "Coluna B"],
          "linhas": [["a1", "b1"], ["a2", "b2"]]
        }
      ],
      "listas": [
        {"titulo": "Regras:", "itens": ["item", "item"]}
      ],
      "acao_final": "Frase final em destaque (opcional)"
    }
  ],
  "checklist": {
    "titulo": "Checklist",
    "secoes": [
      {"titulo": "Antes", "itens": ["item"]},
      {"titulo": "Depois", "itens": ["item"]}
    ]
  },
  "contato": {
    "titulo": "Contato",
    "linhas": [
      ["Canal", "Contato"],
      ["WhatsApp", "61 9 9126-1177"],
      ["Site", "osingular.com.br"]
    ]
  }
}
```

**Nomenclatura e estilo do conteúdo:**
- Títulos de passo seguem o padrão: `Passo N — Nome Curto` (com travessão `—`)
- Ações finais começam com verbo: "Nunca aceitar…", "Registrar…", "Confirmar…"
- Descrições em parágrafos curtos (1-3 frases)
- Tabelas: primeira coluna é o cenário/item, segunda é a ação/resposta
- Listas: itens curtos, imperativos ou substantivos
- Nada de jargão sem contexto

**Seções opcionais:** omita do JSON se não fizer sentido para o processo. Não force conteúdo vazio.

### Passo 4 — Executar o gerador

No diretório de trabalho do usuário:

```bash
python ~/.claude/skills/pop/build.py content.json pop-<slug>.docx
```

Onde `<slug>` é o nome do processo em kebab-case sem acentos
(ex.: "Vendas Recorrentes" → `pop-vendas-recorrentes.docx`).

**Alternativas de invocação:**
- Windows bash: `python /c/Users/teste/.claude/skills/pop/build.py content.json pop-X.docx`
- PowerShell: `python "$env:USERPROFILE\.claude\skills\pop\build.py" content.json pop-X.docx`

**Dependência:** `python-docx` (já instalado globalmente no ambiente).

### Passo 5 — Validar

Após gerar, confirme:

- [ ] Arquivo `.docx` foi criado com tamanho > 50KB (indicativo de conteúdo + fontes embutidas)
- [ ] Nenhum erro na stdout (exceto o print "Gerado: ...")
- [ ] JSON não tem campos "A definir" desnecessários — se houver, sinalize ao usuário

Validação opcional profunda (quando houver dúvida):

```bash
python -c "
import zipfile, re, sys
sys.stdout.reconfigure(encoding='utf-8')
with zipfile.ZipFile('saida.docx') as z:
    with z.open('word/document.xml') as f:
        doc = f.read().decode('utf-8')
    for t in re.findall(r'<w:t[^>]*>([^<]*)</w:t>', doc)[:40]:
        if t.strip(): print(t[:80])
"
```

### Passo 6 — Upload Drive (subpasta POPs)

Sempre subir o `.docx` final pra subpasta **POPs** da Zel via MCP `google-drive`:

- Tool: `mcp__google-drive__uploadFile`
- Args: `localPath` (path absoluto do .docx gerado), `parentFolderId: "1N65TYWzzICVV7QLRFvIdMysSG5kqSYue"` (subpasta POPs), `convertToGoogleFormat: false`
- Guardar o `link` retornado pra entregar ao usuário no passo 7.

Não subir o `content.json` intermediário — só o .docx final.

### Passo 7 — Entregar ao usuário

Resposta curta em 4 linhas:
1. Caminho absoluto do `.docx` gerado
2. **Link Drive (subpasta POPs)** — vem do response do `uploadFile`
3. Resumo: nome do processo, nº de passos, nº de tabelas, seções marcadas "A definir"
4. Sugestão de próximo passo (abrir no Word, converter para PDF, revisar seção X)

## Regras críticas

**Identidade visual (não negociável):**
- O template.docx já traz fonts Urbanist embutidas, header com logo, footer paginado
- **NÃO editar o template.docx diretamente** — mudanças permanentes quebram a skill
- O script `build.py` usa o template como base; preserva automaticamente header/footer
- Paleta: header de tabela preto (`#1C1C1C`) + texto branco, corpo preto/cinza sobre branco

**Conteúdo:**
- NUNCA inventar dados — se o texto do usuário não contém a informação, omitir seção ou marcar "A definir"
- Preservar a voz/tom do texto original — não reescrever em estilo corporativo genérico
- Corrigir APENAS ortografia/acentuação, não alterar sentido das frases
- Quando houver ambiguidade, marcar "[verificar com autor]" inline no JSON

**Limites:**
- Mínimo de seções: título + objetivo + pelo menos 1 passo
- Máximo recomendado: 10 passos (se for mais, dividir em 2 POPs)
- Tabelas com mais de 8 linhas quebram visualmente — dividir em múltiplas tabelas
- Texto por célula de tabela: máximo ~150 caracteres

## Referência

- Exemplo completo: `example-content.json` (conteúdo do POP de Vendas Recorrentes da Singular)
- Acentuação: `references/accents.md` (lista exaustiva)
- Template oficial: `template.docx` (imutável — use via `build.py`)
