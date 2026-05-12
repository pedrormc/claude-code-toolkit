# Skill /contrato — Geração de Contratos Singular

Geração de contratos da Singular Venture com inteligência jurídica do Qdrant `Nexo_Adv`.

## Setup (uma vez)

```bash
cd C:/Users/teste/.claude/skills/contrato
python -m venv .venv
.venv/Scripts/activate          # Windows
pip install -r requirements.txt

cp .env.example .env
# editar .env com OPENAI_API_KEY e QDRANT_API_KEY
```

A `QDRANT_API_KEY` está no container Docker da VPS Lightsail:
```bash
ssh <vps> "sudo docker inspect qdrant | grep QDRANT__SERVICE__API_KEY"
```

## Estrutura

```
contrato/
├── SKILL.md                    # workflow obrigatório (passo 1 → 6)
├── partes/
│   ├── singular.yml            # identidade canônica (Cowmeia, CNPJ, etc.)
│   ├── _exemplo-cliente-pf.yml
│   └── _exemplo-cliente-pj.yml
├── templates/
│   ├── nda-pf.md               # NDA Pessoa Física (12 cláusulas)
│   ├── nda-pj.md               # NDA Pessoa Jurídica
│   ├── mou.md                  # Memorando de Entendimentos
│   ├── prestacao-servicos.md   # Prestação de Serviços (modelo Bossfit)
│   ├── representacao-comercial.md  # Repr. Comercial Autônoma
│   └── embaixador.md           # Embaixador/Embaixadora — Marketing PF (comissão + meta vesting + treinamento)
├── scripts/
│   ├── qdrant_search.py        # busca jurídica no Nexo_Adv
│   └── render_contrato.py      # template Jinja2 → .docx
├── .env.example
├── requirements.txt
└── README.md
```

## Uso manual (sem invocar a skill)

### 1. Pesquisar doutrina
```bash
python scripts/qdrant_search.py "obrigação de meio versus resultado" --area Civel --top 5
```

### 2. Renderizar contrato
```bash
# Editar partes/cliente.yml com dados da outra parte
python scripts/render_contrato.py --tipo nda-pf --vars partes/cliente.yml
# Output: C:\Users\teste\Desktop\contratos\nda-pf\<apelido>-<data>.docx
```

## Uso via skill (recomendado)

Digite no Claude Code:
```
/contrato
```
ou:
```
faz um NDA com a Maria Silva, CPF 123, ela é consultora autônoma...
```

A skill:
1. Pergunta o tipo (NDA/MOU/PS/RC)
2. Coleta variáveis em bloco
3. **Sempre** consulta o Nexo_Adv pra fundamentar e detectar ilegalidades
4. Renderiza o .docx em `Desktop/contratos/`
5. Faz upload pra pasta Zel no Google Drive
6. Reporta achados, riscos e link

## Áreas do Direito disponíveis no Nexo_Adv

Administrativo, Ambiental, Civel, Consumidor, Constitucional, Digital, Eleitoral, Empresarial, Familia, Penal, Previdenciario, Processual_civil, Trabalhista, Tributario.

Use `--area <nome>` no `qdrant_search.py` pra filtrar.

## Output

Todos os contratos vão pra:
```
C:\Users\teste\Desktop\contratos\<tipo>\<apelido>-<YYYY-MM-DD>.docx
```

E são automaticamente subidos pra pasta **Zel** no Google Drive.
