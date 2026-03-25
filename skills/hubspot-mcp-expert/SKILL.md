---
name: hubspot-mcp-expert
description: Expert guide for using HubSpot MCP tools effectively. Use when managing HubSpot CRM data — contacts, companies, deals, leads, engagements (calls, emails, meetings, notes, tasks), associations, and communications. Provides tool selection, parameter formats, common patterns, and integration with n8n workflows.
---

# HubSpot MCP Expert

Guia completo para usar as ferramentas do HubSpot MCP (`@shinzolabs/hubspot-mcp`) no Claude Code.

---

## Visão Geral

O HubSpot MCP fornece **90+ ferramentas** para gerenciar o CRM HubSpot diretamente via Claude Code. Suporta CRUD completo, batch operations, search avançado e engagements.

**Autenticação:** Private App Access Token (`pat-na1-...`)
**Pacote:** `@shinzolabs/hubspot-mcp`

---

## Categorias de Ferramentas

### 1. CRM Core — [CRM_OPERATIONS.md](CRM_OPERATIONS.md)
Operações genéricas que funcionam com qualquer objeto CRM.

### 2. Contacts — [CONTACTS_GUIDE.md](CONTACTS_GUIDE.md)
Gerenciamento completo de contatos: criar, buscar, atualizar, deletar, batch.

### 3. Companies — [COMPANIES_GUIDE.md](COMPANIES_GUIDE.md)
Gerenciamento de empresas com search e batch operations.

### 4. Deals — [DEALS_GUIDE.md](DEALS_GUIDE.md)
Pipeline de vendas: criar deals, mover stages, batch, search.

### 5. Engagements — [ENGAGEMENTS_GUIDE.md](ENGAGEMENTS_GUIDE.md)
Calls, emails, meetings, notes e tasks.

### 6. Associations & Communications — [ASSOCIATIONS_GUIDE.md](ASSOCIATIONS_GUIDE.md)
Vincular objetos entre si e gerenciar preferências de comunicação.

---

## Quick Reference — Ferramentas Mais Usadas

| Ferramenta | Quando Usar |
|------------|-------------|
| `crm_search_contacts` | Buscar contatos por email, nome, propriedade |
| `crm_create_contact` | Criar novo contato |
| `crm_update_contact` | Atualizar propriedades de contato |
| `crm_search_companies` | Buscar empresas |
| `crm_create_company` | Criar nova empresa |
| `crm_list_objects` | Listar qualquer objeto CRM com filtros |
| `crm_create_association` | Vincular contato ↔ empresa, deal, etc. |
| `crm_get_associations` | Ver vínculos de um objeto |
| `notes_create` | Adicionar nota a contato/empresa/deal |
| `tasks_create` | Criar tarefa vinculada a registro CRM |
| `deals_create` | Criar deal no pipeline |
| `emails_list` | Listar emails de engagements |

---

## Guia de Seleção de Ferramentas

### "Preciso encontrar um contato"
```
crm_search_contacts → busca por email, nome, telefone
crm_list_objects(objectType: "contacts") → listar com filtros
```

### "Preciso criar registros em massa"
```
crm_batch_create_contacts → até 100 contatos por vez
crm_batch_update_contacts → atualizar em lote
crm_batch_create_companies → empresas em lote
```

### "Preciso vincular contato a empresa"
```
crm_create_association → criar vínculo
crm_get_associations → verificar vínculos existentes
```

### "Preciso registrar uma interação"
```
notes_create → adicionar nota
calls_create → registrar ligação
emails_create → registrar email
meetings_create → registrar reunião
tasks_create → criar tarefa de follow-up
```

### "Preciso gerenciar pipeline de vendas"
```
deals_create → novo deal
deals_update → mover stage, atualizar valor
deals_search → buscar deals por stage, owner, valor
```

---

## Padrões Comuns

### Padrão 1: Busca + Enriquecimento

```
1. crm_search_contacts({query: "email@example.com"})
2. crm_get_associations({objectId: "123", objectType: "contacts", toObjectType: "companies"})
3. crm_get_object({objectType: "companies", objectId: "456"})
```
**Resultado:** Contato + empresa associada com todos os dados

### Padrão 2: Criação Completa (Contato + Empresa + Deal)

```
1. crm_create_company({properties: {name: "Acme Corp", domain: "acme.com"}})
2. crm_create_contact({properties: {email: "john@acme.com", firstname: "John"}})
3. crm_create_association({fromObjectId: contactId, fromObjectType: "contacts", toObjectId: companyId, toObjectType: "companies"})
4. deals_create({properties: {dealname: "Acme Deal", pipeline: "default", dealstage: "appointmentscheduled"}})
5. crm_create_association({fromObjectId: dealId, fromObjectType: "deals", toObjectId: contactId, toObjectType: "contacts"})
```

### Padrão 3: Atualização em Lote

```
1. crm_search_contacts({filters: [{propertyName: "lifecyclestage", operator: "EQ", value: "lead"}]})
2. crm_batch_update_contacts({inputs: [{id: "1", properties: {lifecyclestage: "marketingqualifiedlead"}}, ...]})
```

### Padrão 4: Registro de Atividade Comercial

```
1. calls_create({properties: {hs_call_title: "Discovery Call", hs_call_body: "Discussed needs...", hs_call_duration: "1800000"}})
2. notes_create({properties: {hs_note_body: "Follow-up: send proposal by Friday"}})
3. tasks_create({properties: {hs_task_subject: "Send proposal", hs_task_due_date: "2026-03-15"}})
```

---

## Integração com n8n

### Quando usar HubSpot MCP vs nó HubSpot do n8n

| Cenário | Usar | Razão |
|---------|------|-------|
| Consulta rápida / ad-hoc | **HubSpot MCP** | Direto no Claude, sem workflow |
| Automação recorrente | **Nó HubSpot n8n** | Scheduled/trigger-based |
| Análise e exploração de dados | **HubSpot MCP** | Interativo, conversacional |
| Webhook de HubSpot → ação | **n8n workflow** | Event-driven |
| Migração / import em massa | **HubSpot MCP** (batch) | Batch operations nativas |
| Relatório periódico | **n8n workflow** | Agendamento automático |

### Padrão: Pesquisa no MCP → Workflow no n8n

```
1. Usar HubSpot MCP para explorar dados e entender estrutura
2. Identificar IDs de pipelines, stages, properties
3. Criar workflow n8n usando os IDs corretos
4. Validar e ativar o workflow
```

---

## Properties Importantes do HubSpot

### Contacts
| Property | Descrição |
|----------|-----------|
| `email` | Email (identificador único) |
| `firstname`, `lastname` | Nome |
| `phone` | Telefone |
| `lifecyclestage` | subscriber → lead → mql → sql → opportunity → customer |
| `hs_lead_status` | Status do lead |
| `hubspot_owner_id` | Owner (responsável) |

### Companies
| Property | Descrição |
|----------|-----------|
| `name` | Nome da empresa |
| `domain` | Domínio web |
| `industry` | Setor |
| `numberofemployees` | Porte |
| `annualrevenue` | Receita anual |
| `hubspot_owner_id` | Owner |

### Deals
| Property | Descrição |
|----------|-----------|
| `dealname` | Nome do deal |
| `pipeline` | ID do pipeline |
| `dealstage` | Stage atual |
| `amount` | Valor |
| `closedate` | Data prevista de fechamento |
| `hubspot_owner_id` | Owner |

---

## Filtros de Busca (Search)

### Operadores Disponíveis

| Operador | Descrição | Exemplo |
|----------|-----------|---------|
| `EQ` | Igual | `{propertyName: "email", operator: "EQ", value: "john@acme.com"}` |
| `NEQ` | Diferente | Excluir valores específicos |
| `GT` / `GTE` | Maior / Maior ou igual | Filtrar por valor, data |
| `LT` / `LTE` | Menor / Menor ou igual | Filtrar por valor, data |
| `CONTAINS_TOKEN` | Contém | Busca parcial em texto |
| `NOT_CONTAINS_TOKEN` | Não contém | Excluir por texto |
| `HAS_PROPERTY` | Tem valor | Filtrar preenchidos |
| `NOT_HAS_PROPERTY` | Não tem valor | Filtrar vazios |
| `IN` | Em lista | Múltiplos valores |
| `NOT_IN` | Fora da lista | Excluir múltiplos valores |
| `BETWEEN` | Entre valores | Range de datas/valores |

### Exemplo de Search com Filtros

```javascript
crm_search_contacts({
  filterGroups: [{
    filters: [
      {propertyName: "lifecyclestage", operator: "EQ", value: "lead"},
      {propertyName: "createdate", operator: "GTE", value: "2026-01-01"}
    ]
  }],
  sorts: [{propertyName: "createdate", direction: "DESCENDING"}],
  limit: 50,
  properties: ["email", "firstname", "lastname", "lifecyclestage", "createdate"]
})
```

---

## Erros Comuns e Soluções

### Erro: 401 Unauthorized
**Causa:** Token expirado ou escopos insuficientes
**Solução:** Recriar Private App com escopos necessários

### Erro: 409 Conflict (duplicata)
**Causa:** Contato/empresa já existe com mesmo email/domain
**Solução:** Buscar primeiro com `crm_search_contacts`, depois `crm_update_contact`

### Erro: Property não reconhecida
**Causa:** Nome da property errado ou custom property não criada
**Solução:** Verificar nome exato no HubSpot (Settings > Properties)

### Erro: Association type inválido
**Causa:** Tipo de associação não suportado ou formato errado
**Solução:** Usar formato correto: `{fromObjectType}_{toObjectType}` (ex: `contact_to_company`)

### Erro: Rate limit (429)
**Causa:** Muitas requisições por segundo
**Solução:** HubSpot permite 100 req/10s (Private Apps). Usar batch operations para volumes grandes.

---

## Boas Práticas

### Fazer
- Usar `crm_search_*` antes de criar para evitar duplicatas
- Usar batch operations para 10+ registros
- Sempre vincular registros com associations após criação
- Registrar atividades (notes, calls, tasks) para histórico
- Usar properties específicas no search (não trazer tudo)

### Não Fazer
- Criar contatos sem verificar duplicatas
- Usar operações individuais quando batch está disponível
- Ignorar associations (dados ficam órfãos no CRM)
- Hardcodar IDs de pipeline/stage (podem mudar)
- Fazer mais de 100 req/10s (rate limit)

---

## Escopos Necessários (Private App)

Para funcionalidade completa, a Private App precisa:

| Escopo | Para |
|--------|------|
| `crm.objects.contacts.read` | Ler contatos |
| `crm.objects.contacts.write` | Criar/editar contatos |
| `crm.objects.companies.read` | Ler empresas |
| `crm.objects.companies.write` | Criar/editar empresas |
| `crm.objects.deals.read` | Ler deals |
| `crm.objects.deals.write` | Criar/editar deals |
| `crm.objects.owners.read` | Ler owners |
| `sales-email-read` | Ler emails de engagements |
| `crm.objects.custom.read` | Objetos customizados (se usar) |
| `crm.objects.custom.write` | Editar objetos customizados |

---

## Related Skills

- **n8n-mcp-tools-expert** — Para criar workflows n8n que integram com HubSpot
- **n8n-workflow-patterns** — Padrões de webhook/API para automações HubSpot
- **n8n-node-configuration** — Configurar nó HubSpot nativo do n8n
