# CRM Core Operations

Operações genéricas que funcionam com **qualquer objeto** CRM do HubSpot.

---

## Listar Objetos

```javascript
crm_list_objects({
  objectType: "contacts",  // contacts, companies, deals, tickets, products, etc.
  limit: 50,               // max 100
  after: "cursor_string",  // paginação
  properties: ["email", "firstname", "lastname"]  // só o que precisa
})
```

**Tipos de objeto suportados:**
- `contacts`, `companies`, `deals`, `tickets`
- `products`, `line_items`, `quotes`
- `invoices`, `subscriptions`, `orders`, `carts`
- Objetos customizados: usar o `objectType` definido no HubSpot

---

## Criar Objeto

```javascript
crm_create_object({
  objectType: "contacts",
  properties: {
    email: "john@example.com",
    firstname: "John",
    lastname: "Doe",
    phone: "+5511999999999"
  }
})
```

**Retorno:** `{ id: "12345", properties: {...}, createdAt: "..." }`

---

## Ler Objeto

```javascript
crm_get_object({
  objectType: "contacts",
  objectId: "12345",
  properties: ["email", "firstname", "lifecyclestage"]
})
```

---

## Atualizar Objeto

```javascript
crm_update_object({
  objectType: "contacts",
  objectId: "12345",
  properties: {
    lifecyclestage: "customer",
    hs_lead_status: "CONNECTED"
  }
})
```

**Importante:** Atualização é merge — só as properties enviadas são alteradas, o resto permanece.

---

## Deletar (Archive) Objeto

```javascript
crm_archive_object({
  objectType: "contacts",
  objectId: "12345"
})
```

**Nota:** Archive no HubSpot é soft delete — o registro pode ser restaurado em até 90 dias.

---

## Search Genérico

```javascript
crm_search_objects({
  objectType: "contacts",
  filterGroups: [{
    filters: [
      {
        propertyName: "lifecyclestage",
        operator: "EQ",
        value: "lead"
      }
    ]
  }],
  sorts: [{
    propertyName: "createdate",
    direction: "DESCENDING"
  }],
  limit: 20,
  properties: ["email", "firstname", "lastname", "lifecyclestage"]
})
```

### FilterGroups Logic

- **Filters dentro do mesmo grupo:** AND (todas devem ser verdadeiras)
- **FilterGroups entre si:** OR (qualquer grupo pode ser verdadeiro)

```javascript
// Exemplo: (lifecyclestage = lead AND city = SP) OR (lifecyclestage = mql)
filterGroups: [
  {
    filters: [
      {propertyName: "lifecyclestage", operator: "EQ", value: "lead"},
      {propertyName: "city", operator: "EQ", value: "São Paulo"}
    ]
  },
  {
    filters: [
      {propertyName: "lifecyclestage", operator: "EQ", value: "marketingqualifiedlead"}
    ]
  }
]
```

---

## Batch Operations

### Batch Create
```javascript
crm_batch_create({
  objectType: "contacts",
  inputs: [
    {properties: {email: "a@example.com", firstname: "Alice"}},
    {properties: {email: "b@example.com", firstname: "Bob"}},
    // ... até 100 itens
  ]
})
```

### Batch Update
```javascript
crm_batch_update({
  objectType: "contacts",
  inputs: [
    {id: "123", properties: {lifecyclestage: "customer"}},
    {id: "456", properties: {lifecyclestage: "customer"}},
  ]
})
```

### Batch Read
```javascript
crm_batch_read({
  objectType: "contacts",
  inputs: [{id: "123"}, {id: "456"}, {id: "789"}],
  properties: ["email", "firstname"]
})
```

---

## Paginação

Todas as operações de listagem retornam `paging.next.after` quando há mais resultados:

```javascript
// Página 1
const page1 = crm_list_objects({objectType: "contacts", limit: 100})
// page1.paging.next.after = "eyJsaW1pdCI6M..."

// Página 2
const page2 = crm_list_objects({objectType: "contacts", limit: 100, after: page1.paging.next.after})
```

**Limite:** max 100 itens por página. Para mais, iterar com `after`.
