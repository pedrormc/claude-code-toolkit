---
name: contrato
description: Gera contratos da Singular Venture (NDA-PF, NDA-PJ, MOU, Prestação de Serviços, Representação Comercial, Embaixador) em .docx, salvos em C:\Users\teste\Desktop\contratos\ e com upload automático pra pasta Zel no Google Drive. SEMPRE consulta o Qdrant Nexo_Adv (25k+ chunks de doutrina jurídica brasileira) pra fundamentar cláusulas, detectar ilegalidades e enriquecer o texto. Use quando o usuário pedir "fazer contrato", "gerar NDA", "redigir contrato", "criar MOU", "contrato embaixador", "novo contrato Singular" etc.
---

# Skill: /contrato

Geração de contratos com inteligência jurídica do Nexo_Adv. Output sempre em `.docx`, padrão Singular Venture.

## Identidade da CONTRATANTE (canônico)

```yaml
razao_social: SINGULAR VENTURE LTDA
cnpj: 62.618.804/0001-06
endereco: Cowmeia Coworking, Edifício Easy, R. das Pitangueiras, 5/6
complemento: Residencial Easy - Portaria B
bairro: Águas Claras
cidade: Brasília
uf: DF
cep: 71908-720
representante: Pedro da Silva Rocha
cpf_representante: 000.000.000-00
cargo_representante: Administrador Legal
foro: Brasília/DF
```

Fonte canônica versionada em `partes/singular.yml`. **NUNCA** use endereços antigos (SIA Guará, SCRN Asa Norte) — eles aparecem em contratos legados, mas o vigente é o Cowmeia.

## Workflow obrigatório

### Passo 1 — Identificar tipo
Pergunte qual modelo (a menos que o usuário já tenha dito):

```
[CONTRATO] Qual tipo?
[ ] nda-pf       — NDA com pessoa física
[ ] nda-pj       — NDA com pessoa jurídica
[ ] mou          — Memorando de Entendimentos (parceria estratégica)
[ ] prestacao    — Prestação de Serviços (modelo Bossfit)
[ ] repcomercial — Representação Comercial Autônoma
[ ] embaixador   — Embaixador/Embaixadora — Prestação de Serviço de Marketing (PF, comissão por êxito + meta de vesting + treinamento)
```

### Passo 2 — Coletar variáveis da CONTRATADA / outra parte
Use o template correspondente em `templates/<tipo>.md` como guia. Pergunte em bloco, nunca campo por campo:

```
[CONTRATO] Me passa os dados da outra parte:
- Nome/Razão social:
- CPF/CNPJ:
- RG (se PF) / Representante legal (se PJ):
- Endereço completo (rua, número, bairro, cidade/UF, CEP):
- Apelido curto (como será referenciada no contrato):
- E demais campos específicos do tipo (objeto, prazo, valor, percentual, etc.)
```

### Passo 3 — CONSULTA OBRIGATÓRIA AO NEXO_ADV
**Antes de gerar o contrato, sempre consulte o Qdrant Nexo_Adv** pra:

1. **Fundamentar as cláusulas críticas** com doutrina/jurisprudência. Queries-base por tipo:
   - **NDA:** "obrigação de confidencialidade prazo razoável", "multa por quebra de NDA proporcionalidade"
   - **MOU:** "memorando entendimentos vínculo societário pre-contrato", "boa-fé objetiva tratativas preliminares"
   - **Prestação Serviços:** "obrigação de meio versus obrigação de resultado", "rescisão imotivada aviso prévio prestação serviços"
   - **Representação Comercial:** "Lei 4.886/65 representação comercial", "indenização representante comercial rescisão", "vínculo empregatício representação comercial autônoma"
   - **Embaixador:** "comissão por êxito autonomia profissional", "vínculo empregatício prestação serviço marketing", "comissão sobre vendas produto pessoa física", "multa contratual desproporcional CC art. 412", "treinamento como investimento contrapartida prestação serviço", "ajuste de margem comissão por meta atingida"

2. **Detectar ilegalidades** — sempre rodar busca pra cada cláusula sensível:
   - Cláusulas penais excessivas (CC art. 412 — limite ao valor da obrigação principal)
   - Não-concorrência com prazo abusivo (>5 anos costuma ser questionado)
   - Foro de eleição (CPC art. 63)
   - LGPD em contratos com tratamento de dados pessoais
   - Renúncia abusiva de direitos (CDC se aplicável)
   - **Em contrato Embaixador especificamente:** alertar SEMPRE sobre (a) multa contratual default de R$ 100.000,00 — checar proporcionalidade ao art. 412 do CC contra a obrigação principal/valor estimado de comissão; (b) comissão sobre vendas de produto específico (default: 20% sobre vendas do Powercoffee) — se a CONTRATADA é pessoa física e exerce captação/venda habitual com treinamento prévio, pode caracterizar vínculo empregatício ou representação comercial regulada pela Lei 4.886/65; (c) cláusula de ajuste de margem após meta atingida (ex: 80 vendas de embalagens 270g) — verificar se está clara o suficiente pra evitar disputa sobre a "nova margem".

3. **Filtrar por área do direito relevante** usando `law_area` no payload:
   - Trabalhista (vínculo, CLT)
   - Empresarial (sociedade, contratos comerciais)
   - Civel (obrigações, responsabilidade)
   - Constitucional (princípios)
   - Consumidor (se aplicável)
   - Digital (LGPD, marco civil)

Use `scripts/qdrant_search.py` (CLI) com flag `--area <law_area>` quando souber o filtro.

### Passo 4 — Gerar o .docx
Rodar `python scripts/render_contrato.py --tipo <tipo> --vars <yaml-com-variaveis>` que:
- Carrega `templates/<tipo>.md` (Jinja2)
- Funde com `partes/singular.yml` + variáveis da outra parte
- Renderiza em `.docx` formatado (python-docx)
- Salva em `C:\Users\teste\Desktop\contratos\<tipo>\<nome-curto>-<YYYY-MM-DD>.docx`

### Passo 5 — Upload Drive (sempre)
Após gerar o .docx, fazer upload pra pasta **Zel** no Google Drive via MCP `google-drive` (@piotr-agier/google-drive-mcp v2.2.0):
1. Buscar a pasta Zel (se ainda não souber o ID): `mcp__claude_ai_Google_Drive__search_files` com query `name contains 'Zel'` — esse MCP continua útil pra busca.
   - ID conhecido da pasta Zel: `10ARKUMWyFzVkdaPEWLYC9OXWqm0ywS6e`.
2. Subir o .docx: `mcp__google-drive__uploadFile` passando `localPath` (path absoluto do arquivo, NÃO base64) e `parentFolderId` da Zel. Sem limite prático de tamanho (não trafega base64).
3. Reportar pro usuário o link do Drive (vem no response do uploadFile).

### Passo 6 — Resumo final
Reportar ao usuário:
- Caminho local do .docx
- Link Drive
- **Achados do Nexo_Adv** (citações de doutrina/jurisprudência usadas)
- **Riscos detectados** se houver (cláusula com potencial questionamento)
- Próximos passos sugeridos (revisão jurídica humana, assinatura digital, etc.)

## Variáveis universais dos templates

Todos os templates aceitam essas variáveis (Jinja2):

| Variável | Descrição | Exemplo |
|---|---|---|
| `parte.nome` | Razão social ou nome completo | "Maria Silva Santos" |
| `parte.tipo` | "PF" ou "PJ" | "PF" |
| `parte.documento` | CPF ou CNPJ formatado | "123.456.789-00" |
| `parte.rg` | RG (só PF) | "1234567 SSP/DF" |
| `parte.representante` | Nome do representante (só PJ) | "João Souza" |
| `parte.cargo` | Cargo do representante (só PJ) | "Sócio-Diretor" |
| `parte.cpf_representante` | CPF do representante (só PJ) | "111.222.333-44" |
| `parte.endereco` | Endereço completo | "Rua X, 100, Sala 5" |
| `parte.bairro` | Bairro | "Asa Sul" |
| `parte.cidade_uf` | Cidade/UF | "Brasília/DF" |
| `parte.cep` | CEP | "70000-000" |
| `parte.apelido` | Como será referenciada no texto | "MARIA" |
| `parte.email` | E-mail (opcional) | "x@y.com" |
| `objeto` | Descrição do objeto contratual | "consultoria estratégica..." |
| `prazo_meses` | Prazo em meses | 12 |
| `valor` | Valor total ou referência | "R$ 10.000,00" |
| `percentual` | Percentual aplicável | "10%" |
| `data_assinatura` | Data por extenso | "25 de fevereiro de 2026" |
| `cidade_assinatura` | Cidade da assinatura | "Brasília" |

## Regras invioláveis

- **NUNCA** gerar contrato sem antes consultar o Nexo_Adv (passo 3 obrigatório).
- **NUNCA** salvar fora de `C:\Users\teste\Desktop\contratos\` ou pular o upload Drive.
- **SEMPRE** alertar sobre riscos jurídicos detectados — não é só "geração", é também triagem.
- **SEMPRE** usar o endereço Cowmeia. Se um contrato modelo legado mostrar SIA Guará ou SCRN Asa Norte, é dado obsoleto.
- Se o usuário pedir uma cláusula específica que conflite com doutrina/lei encontrada no Nexo_Adv, reporte o conflito antes de aceitar a alteração.

## Dependências (requirements.txt)

```
python-docx>=1.1
qdrant-client>=1.9
openai>=1.30
jinja2>=3.1
python-dotenv>=1.0
pyyaml>=6.0
```

`.env` necessário (criar a partir de `.env.example`):
```
OPENAI_API_KEY=sk-...
QDRANT_URL=https://seu-qdrant.exemplo.com
QDRANT_API_KEY=<key do Lightsail>
QDRANT_COLLECTION=Nexo_Adv
EMBED_MODEL=text-embedding-3-large
```

## Sinalização de origem

Todo contrato gerado leva ao final do arquivo (não imprimível, em propriedade do docx):
`Gerado por: Claude Master Desktop / Skill /contrato / [data]`
