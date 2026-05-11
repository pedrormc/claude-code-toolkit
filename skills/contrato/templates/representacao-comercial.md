# CONTRATO DE PRESTAÇÃO DE SERVIÇOS DE REPRESENTAÇÃO COMERCIAL AUTÔNOMA

## CONTRATANTE

**SINGULAR VENTURE LTDA**, pessoa jurídica de direito privado inscrita no CNPJ nº {{ singular.cnpj }}, com sede no {{ singular.endereco_completo }}, neste ato representada por seu administrador legal **{{ singular.representante_nome }}**, CPF nº {{ singular.representante_cpf }}.

## CONTRATADA

**{{ parte.nome }}**, pessoa física inscrita no CPF nº {{ parte.documento }}{% if parte.rg %}, portador do RG nº {{ parte.rg }}{% endif %}, com endereço à {{ parte.endereco }}, {{ parte.bairro }}, {{ parte.cidade_uf }}, CEP {{ parte.cep }}, doravante denominado(a) **CONTRATADA**.

As partes resolvem celebrar o presente **CONTRATO DE PRESTAÇÃO DE SERVIÇOS AUTÔNOMOS DE REPRESENTAÇÃO COMERCIAL**, que se regerá pelas cláusulas e condições seguintes.

---

## CLÁUSULA PRIMEIRA – DO OBJETO

**1.1.** O presente contrato tem por objeto a contratação da CONTRATADA, na qualidade de **profissional autônomo**, para atuação na frente de **{{ frente_atuacao | default("prospecção ativa de clientes e gestão de funil comercial") }}**, pelo período inicial de **{{ prazo_meses | default(6) }} ({{ prazo_meses_extenso | default("seis") }}) meses**.

**1.2.** A atuação compreenderá:
{% for atividade in atividades | default([
  "prospecção ativa de novos clientes",
  "qualificação de leads",
  "agendamento de reuniões de venda",
  "aplicação de metodologia de gerenciamento de funil",
  "acompanhamento de contratos originados por sua atuação",
  "utilização dos sistemas, CRM e infraestrutura tecnológica da CONTRATANTE"
]) %}
- {{ loop.index | string }}) {{ atividade }};
{% endfor %}

**1.3.** A presente contratação possui natureza **estritamente civil e comercial**, não configurando vínculo empregatício, societário ou associativo, inexistindo:
- subordinação hierárquica;
- controle de jornada;
- pessoalidade obrigatória;
- exclusividade;
- habitualidade nos moldes da CLT.

**1.4.** A CONTRATADA possui plena liberdade quanto à metodologia, organização de agenda, estratégia comercial e forma de execução, responsabilizando-se integralmente por seus encargos fiscais e tributários.

---

## CLÁUSULA SEGUNDA – DOS RITOS DE ALINHAMENTO

**2.1.** Para fins de coordenação estratégica, as partes acordam a realização de:
- a) Dailys breves de alinhamento comercial;
- b) Reunião semanal de revisão de resultados e iniciativas;
- c) Reunião mensal de avaliação estratégica.

**2.2.** Tais encontros não caracterizam subordinação ou controle de jornada, constituindo mera coordenação estratégica entre partes independentes.

---

## CLÁUSULA TERCEIRA – DA REMUNERAÇÃO

**3.1.** A remuneração da CONTRATADA será **exclusivamente variável**, correspondente a **{{ percentual_comissao | default("10% (dez por cento)") }}** sobre os valores efetivamente recebidos pela CONTRATANTE:

- I – provenientes de vendas geradas por sua atuação direta;
- II – enquanto os contratos permanecerem ativos e adimplentes;
- III – enquanto vigente o presente contrato.

**3.2.** A comissão incidirá sobre a receita recorrente mensal efetivamente recebida.

{% if ajuda_custo %}
**3.3.** Ao atingir a meta de vendas correspondente a {{ meta_ajuda_custo | default("R$ receita recorrente mensal ativa") }}, a CONTRATADA fará jus a **ajuda de custo adicional no valor de {{ ajuda_custo }}**, cumulativa às comissões.
{% endif %}

**3.{{ "4" if ajuda_custo else "3" }}.** O pagamento será efetuado todo dia **{{ dia_pagamento | default("20 (vinte)") }}** de cada mês, mediante transferência bancária.

**3.{{ "5" if ajuda_custo else "4" }}.** Não haverá garantia mínima mensal.

---

## CLÁUSULA QUARTA – DA VIGÊNCIA E RENOVAÇÃO

**4.1.** A partir da assinatura do presente instrumento em **{{ data_inicio }}**, o contrato passará a vigorar até **{{ data_fim }}**.

**4.2.** Após esse período, renovar-se-á automaticamente por períodos sucessivos de **{{ prazo_meses | default(6) }} ({{ prazo_meses_extenso | default("seis") }}) meses**, salvo manifestação expressa em contrário com antecedência mínima de 30 dias.

---

## CLÁUSULA QUINTA – DAS INFORMAÇÕES CONFIDENCIAIS

**5.1.** Considera-se INFORMAÇÃO CONFIDENCIAL toda informação escrita, verbal, digital ou de qualquer natureza revelada pela CONTRATANTE, incluindo, mas não se limitando a:

- a) planos de negócio, estratégias comerciais e financeiras;
- b) frameworks, metodologias, POPs, playbooks;
- c) dados técnicos e operacionais;
- d) informações de clientes e parceiros;
- e) quaisquer dados acessados em razão da relação contratual.

**5.2.** A obrigação de confidencialidade perdurará por prazo indeterminado, mesmo após o término contratual.

---

## CLÁUSULA SEXTA – DA PROPRIEDADE INTELECTUAL

**6.1.** Todos os direitos de propriedade intelectual decorrentes das atividades realizadas pertencem exclusivamente à CONTRATANTE.

**6.2.** A utilização indevida de materiais, sistemas ou metodologias será considerada infração grave.

---

## CLÁUSULA SÉTIMA – DAS PENALIDADES

**7.1.** A divulgação não autorizada de informação confidencial sujeitará a CONTRATADA:

- a) à rescisão imediata do contrato;
- b) ao pagamento de multa de **{{ multa_confidencialidade | default("10 (dez) salários mínimos") }}**;
- c) à indenização integral por perdas e danos.

---

## CLÁUSULA OITAVA – DA NÃO CONFIGURAÇÃO DE VÍNCULO EMPREGATÍCIO

**8.1.** As partes reconhecem expressamente que o presente instrumento não gera vínculo empregatício.

**8.2.** A eventual habitualidade na atuação decorre da natureza da atividade comercial e não caracteriza subordinação jurídica.

---

## CLÁUSULA NONA – DA RESCISÃO

**9.1.** O contrato poderá ser rescindido por qualquer das partes mediante aviso prévio de 30 dias.

**9.2.** Em caso de infração contratual, a rescisão poderá ocorrer imediatamente.

---

## CLÁUSULA DÉCIMA – ASSINATURA DIGITAL

As PARTES reconhecem a validade da assinatura digital, nos termos da MP 2.200-2/2001.

---

## CLÁUSULA DÉCIMA PRIMEIRA – DO FORO

Fica eleito o {{ singular.foro_descricao }}, com renúncia a qualquer outro.

---

{{ cidade_assinatura | default(singular.foro_cidade) }}, {{ data_assinatura }}.

---

________________________
**SINGULAR VENTURE LTDA**
{{ singular.representante_nome }}
CNPJ {{ singular.cnpj }}

________________________
**{{ parte.nome }}**
CPF: {{ parte.documento }}
