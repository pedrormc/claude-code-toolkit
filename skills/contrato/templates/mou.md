# MEMORANDO DE ENTENDIMENTOS (MOU)

## {{ subtitulo | default("Parceria Técnica e Estratégica") }}

---

## 1. IDENTIFICAÇÃO DAS PARTES

De um lado:

**SINGULAR VENTURE LTDA**, pessoa jurídica de direito privado inscrita no CNPJ sob nº {{ singular.cnpj }}, com sede no {{ singular.endereco_completo }}, neste ato representado pelo administrador legal, **{{ singular.representante_nome }}**, {{ singular.representante_estado_civil }}, {{ singular.representante_profissao }}, inscrito no CPF sob nº {{ singular.representante_cpf }}, doravante denominada **{{ apelido_singular | default("SINGULAR") }}**.

E, de outro lado:

**{{ parte.nome }}**{% if parte.nome_fantasia %} ({{ parte.nome_fantasia }}){% endif %}, pessoa jurídica de direito privado, inscrita no CNPJ sob o nº {{ parte.documento }}, na pessoa de seu representante legal **{{ parte.representante }}**, {{ parte.descricao_profissional | default(parte.cargo) }}, doravante denominada **{{ parte.apelido }}**.

As Partes resolvem firmar o presente Memorando de Entendimentos (MOU), com o objetivo de alinhar princípios, escopo, responsabilidades e diretrizes da parceria a ser desenvolvida no âmbito do **{{ projeto | default(subtitulo) }}**, sem constituição de vínculo societário, empregatício ou exclusividade, nos termos abaixo.

---

## 2. NATUREZA DO DOCUMENTO

O presente MOU tem caráter **não societário** e **não empregatício**, servindo como instrumento de alinhamento estratégico preliminar entre as Partes, estabelecendo:

- o papel da {{ parte.apelido }} no ecossistema da {{ apelido_singular | default("SINGULAR") }};
- as diretrizes iniciais de atuação;
- os critérios de remuneração vinculados à geração de valor de ambas as partes;
- os marcos de avaliação e revisão da parceria ao final dos {{ prazo_meses | default(6) }} ({{ prazo_meses_extenso | default("seis") }}) meses.

Este documento **não constitui contrato definitivo**, nem cria vínculo trabalhista, societário ou de exclusividade entre as Partes, podendo ser revisado, ajustado ou substituído por instrumentos contratuais específicos mediante comum acordo.

---

## 3. OBJETIVO DA PARCERIA

{{ objetivo | default("As Partes reconhecem que esta parceria se baseia na confiança, no respeito mútuo e na convergência de valores profissionais, tendo como premissa a construção gradual de impacto, sem atalhos ou promessas artificiais.") }}

{% if objetivos_especificos %}
O objetivo desta parceria contempla:
{% for obj in objetivos_especificos %}
- {{ obj }};
{% endfor %}
{% endif %}

---

## 4. ESCOPO DE ATUAÇÃO

{{ escopo | default("O escopo será detalhado em cronograma de trabalho construído conjuntamente pelas Partes após a assinatura deste MOU.") }}

{% if limites_atuacao %}
**Limites de Atuação:**
{% for limite in limites_atuacao %}
- {{ limite }};
{% endfor %}
{% endif %}

Qualquer ampliação de escopo, atribuições adicionais ou assunção de responsabilidades operacionais deverá ser previamente discutida e formalizada por meio de aditivo a este MOU.

---

## 5. ESTRUTURA DE REMUNERAÇÃO

{{ remuneracao | default("A remuneração estará vinculada exclusivamente à geração de valor associada às ofertas em que a atuação técnica e intelectual contribua para a sustentação de preço.") }}

**Princípios Gerais:**
- A remuneração não constitui salário, pró-labore ou remuneração fixa;
- Está vinculada a valores brutos efetivamente vendidos;
- Não há garantia mínima de remuneração;
- Não há obrigação de volume mínimo de vendas;
- As Partes reconhecem o compromisso mútuo de boa-fé.

{% if linhas_receita %}
{% for linha in linhas_receita %}
**5.{{ loop.index + 1 }} {{ linha.titulo }}**
{{ linha.descricao }}
{% endfor %}
{% endif %}

---

## 6. METAS, PRAZO E MARCOS DE AVALIAÇÃO

**6.1 Prazo Inicial.** O presente MOU estabelece um prazo inicial de **{{ prazo_meses | default(6) }} ({{ prazo_meses_extenso | default("seis") }}) meses** de vigência, contados a partir do início efetivo da parceria em **{{ data_inicio | default(data_assinatura) }}**.

Este período tem caráter **experimental e avaliativo**, destinado a validar:
- aderência da parceria;
- sustentabilidade do modelo financeiro;
- efetividade do escopo definido;
- alinhamento estratégico entre as Partes.

{% if meta_referencia %}
**6.2 Meta Inicial.** Durante o prazo inicial deste MOU, as Partes adotam como meta de referência: **{{ meta_referencia }}**.

Esta meta:
- não configura garantia de resultado;
- não gera penalidades automáticas;
- serve como marco objetivo para reavaliação da parceria.
{% endif %}

**6.3 Marcos de Avaliação.** Ao término do prazo inicial, as Partes comprometem-se a realizar uma avaliação conjunta, contemplando, no mínimo:
- desempenho da estrutura de remuneração vigente;
- adequação do escopo;
- viabilidade de ampliação ou ajuste da parceria;
- definição de novas metas e prazos.

Nenhuma alteração será considerada automática, devendo qualquer ajuste ser formalizado por escrito em instrumento próprio.

---

## 7. DISPOSIÇÕES GERAIS, LIMITES E ENCERRAMENTO

**7.1 Ausência de Exclusividade e Vínculo.** Fica expressamente acordado que:
- a presente parceria não estabelece exclusividade entre as Partes;
- não há vínculo empregatício, societário ou de representação comercial;
- cada Parte permanece livre para desenvolver outras atividades, projetos ou parcerias, desde que não haja conflito direto com o objeto deste MOU.

**7.2 Autonomia das Partes.** Cada Parte será responsável por:
- seus próprios custos, tributos, obrigações fiscais e previdenciárias;
- a gestão de suas respectivas agendas, equipes e entregas;
- a observância das normas legais e éticas aplicáveis às suas atividades.

Nenhuma das Partes poderá assumir obrigações ou compromissos em nome da outra sem autorização expressa e por escrito.

**7.3 Confidencialidade.** As Partes comprometem-se a manter confidenciais todas as informações estratégicas, comerciais, técnicas ou operacionais às quais tenham acesso em razão desta parceria, não podendo divulgá-las a terceiros sem autorização prévia, salvo quando exigido por lei. A obrigação de confidencialidade permanecerá válida mesmo após o encerramento deste MOU.

**7.4 Vigência e Encerramento.** Este MOU entra em vigor na data de sua assinatura, permanecendo válido pelo prazo definido no item 6.1. O MOU poderá ser encerrado por qualquer das Partes, mediante comunicação prévia por escrito, sem necessidade de justificativa, respeitando-se as obrigações já assumidas e os valores eventualmente devidos até a data do encerramento.

**7.5 Foro.** Para dirimir quaisquer controvérsias oriundas deste MOU, as Partes elegem o {{ singular.foro_descricao }}, com renúncia expressa a qualquer outro, por mais privilegiado que seja.

---

## 8. ENCERRAMENTO

As Partes declaram que leram, compreenderam e concordam com os termos deste Memorando de Entendimentos, firmando-o como expressão fiel de suas intenções atuais, podendo ser revisado, ajustado ou formalizado em instrumentos contratuais específicos, conforme a evolução da parceria.

---

{{ cidade_assinatura | default(singular.foro_cidade) }}-{{ singular.foro_uf }}, {{ data_assinatura }}.

---

**SINGULAR VENTURE**
CNPJ nº {{ singular.cnpj }}

---

**{{ parte.nome }}**
CNPJ nº {{ parte.documento }}
