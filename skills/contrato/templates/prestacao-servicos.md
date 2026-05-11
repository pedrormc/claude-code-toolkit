# CONTRATO DE PRESTAÇÃO DE SERVIÇOS

## {{ subtitulo | default("ESTRUTURAÇÃO E EXECUÇÃO DE PROJETO COMERCIAL") }} – {{ mes_ano | default(data_assinatura) }}

Pelo presente instrumento particular, de um lado, **{{ parte.nome }}**, pessoa jurídica de direito privado, inscrita no CNPJ sob nº {{ parte.documento }}, com sede em {{ parte.endereco }}, {{ parte.bairro }}, {{ parte.cidade_uf }}, CEP {{ parte.cep }}, neste ato representada por **{{ parte.representante }}**, CPF {{ parte.cpf_representante }}{% if parte.rg %}, RG {{ parte.rg }}{% endif %}{% if parte.endereco_representante %}, residente em {{ parte.endereco_representante }}{% endif %}{% if parte.email %}, e-mail {{ parte.email }}{% endif %}, doravante denominada **"CONTRATANTE"**;

e, de outro lado, **SINGULAR VENTURE LTDA**, pessoa jurídica de direito privado inscrita no CNPJ sob nº {{ singular.cnpj }}, com sede no {{ singular.endereco_completo }}, neste ato representada por seu administrador legal **{{ singular.representante_nome }}**, inscrito no CPF nº {{ singular.representante_cpf }}, doravante denominada **"CONTRATADA"** ou **"Singular"**;

têm entre si justo e contratado o seguinte.

---

## CLÁUSULA PRIMEIRA – DO OBJETO E DO PRAZO

**1.1.** O presente Contrato tem por objeto a prestação, pela CONTRATADA, de serviços de **{{ objeto }}**, nos termos do {{ anexo_cronograma | default("cronograma apresentado como Anexo I") }}.

**1.2.** {{ detalhamento_objeto | default("Os serviços serão prestados conforme metodologia própria da CONTRATADA, observando-se as melhores práticas do mercado.") }}

**1.3.** O projeto terá duração operacional de **{{ prazo_meses | default(12) }} ({{ prazo_meses_extenso | default("doze") }}) meses**, contados da assinatura deste Contrato, sem prejuízo das obrigações que, por sua natureza, devam subsistir após esse prazo, especialmente as de pagamento, confidencialidade, propriedade intelectual e solução de controvérsias.

{% if etapas %}
**1.4.** A execução do projeto seguirá o seguinte plano:

{% for etapa in etapas %}
**{{ etapa.titulo }}**
{% for item in etapa.itens %}
- {{ item }}
{% endfor %}

{% endfor %}
{% endif %}

---

## CLÁUSULA SEGUNDA – DOS SERVIÇOS E DAS OBRIGAÇÕES DA CONTRATADA

**2.1.** Compete à CONTRATADA:
{% for obrigacao in obrigacoes_contratada | default([
  "executar os serviços conforme escopo e cronograma acordados",
  "elaborar e ajustar materiais, processos e métricas operacionais",
  "acompanhar tecnicamente a execução e recomendar correções de rota",
  "manter comunicação ativa e transparente com a CONTRATANTE"
]) %}
- ({{ loop.index }}) {{ obrigacao }};
{% endfor %}

**2.2.** As Partes reconhecem que este Contrato reúne **obrigações de resultado** e **obrigações de meio**.

**2.3.** A CONTRATADA empregará técnica, diligência e metodologia própria para maximizar os resultados do projeto, sem garantir volume mínimo de vendas, faturamento, lucratividade ou resultado financeiro específico.

---

## CLÁUSULA TERCEIRA – DAS OBRIGAÇÕES DA CONTRATANTE

**3.1.** Compete à CONTRATANTE:
- (i) fornecer, em tempo hábil, as informações, materiais e acessos necessários à execução do projeto;
- (ii) participar das agendas estratégicas e rituais de governança;
- (iii) manter condições mínimas para a execução do projeto;
- (iv) efetuar os pagamentos devidos à CONTRATADA.

**3.2.** Qualquer atraso, omissão ou indisponibilidade imputável à CONTRATANTE que afete a execução do projeto autorizará o ajuste proporcional dos prazos, marcos e medições correspondentes mediante alinhamento prévio entre as PARTES.

---

## CLÁUSULA QUARTA – DA REMUNERAÇÃO

**4.1.** Pela execução dos serviços, a CONTRATANTE pagará à CONTRATADA:
{% if investimento_inicial %}
- (i) **investimento inicial de {{ investimento_inicial }}**;
{% endif %}
{% if bonus_condicionado %}
- (ii) **bônus condicionado de {{ bonus_condicionado }}**, se atendidas as metas previstas no item 4.4;
{% endif %}
{% if percentual_variavel %}
- (iii) **participação variável de {{ percentual_variavel }}** sobre {{ base_calculo | default("o faturamento bruto") }}, nos termos da Cláusula Quinta.
{% endif %}

Todos os pagamentos serão realizados pela CONTRATANTE mediante apresentação de Nota Fiscal pela CONTRATADA.

{% if forma_pagamento %}
**4.2.** {{ forma_pagamento }}
{% endif %}

{% if metas_bonus %}
**4.4.** O bônus condicionado será devido apenas se, ao final do período contratual, forem apuradas as seguintes metas acumuladas:
{% for meta in metas_bonus %}
- {{ meta }}
{% endfor %}

**4.5.** O bônus condicionado somente será devido se todas as metas descritas no item 4.4 forem integralmente atingidas. O não cumprimento de qualquer das metas desobriga a CONTRATANTE do pagamento do bônus.
{% endif %}

---

## CLÁUSULA QUINTA – DA NATUREZA DA RELAÇÃO E DA AUSÊNCIA DE VÍNCULO

**5.1.** A relação entre as Partes é exclusivamente empresarial, não gerando sociedade, mandato, representação, exclusividade geral, vínculo empregatício ou subordinação jurídica entre uma Parte e os empregados, sócios ou prepostos da outra.

---

## CLÁUSULA SEXTA – DA RESCISÃO

**6.1.** O presente Contrato poderá ser rescindido por justa causa por qualquer das Partes se a outra descumprir obrigação contratual relevante e não sanar a irregularidade no prazo de **10 (dez) dias corridos** contados do recebimento de notificação escrita, ressalvadas as hipóteses de gravidade que justifiquem suspensão imediata da execução para evitar prejuízo relevante.

**6.2.** O Contrato também poderá ser resilido imotivadamente por qualquer das Partes mediante aviso prévio escrito de **30 (trinta) dias**.

**6.3.** Na hipótese de resilição imotivada pela CONTRATANTE, permanecerão devidos à CONTRATADA: (i) os valores vencidos e não pagos; (ii) os valores proporcionais aos serviços efetivamente prestados até o término do aviso prévio; (iii) as despesas extraordinárias previamente aprovadas pela CONTRATANTE.

**6.4.** A rescisão ou resilição do presente Contrato não prejudicará as obrigações de confidencialidade, proteção de dados, propriedade intelectual, pagamento de valores já constituídos e solução de controvérsias.

---

## CLÁUSULA SÉTIMA – DA CONFIDENCIALIDADE, PROTEÇÃO DE DADOS E PROPRIEDADE INTELECTUAL

**7.1.** Cada Parte manterá sigilo sobre as informações comerciais, estratégicas, financeiras, operacionais, técnicas e cadastrais da outra Parte a que tiver acesso em razão deste Contrato, salvo autorização prévia e escrita ou exigência legal, regulatória ou judicial.

**7.2.** As Partes comprometem-se a tratar eventuais dados pessoais em conformidade com a legislação aplicável, inclusive a **LGPD (Lei nº 13.709/2018)**, exclusivamente para execução da relação contratual.

**7.3.** A obrigação de confidencialidade permanecerá vigente por **{{ prazo_confidencialidade | default("2 (dois) anos") }}** após o término deste Contrato.

**7.4.** Os materiais e entregáveis desenvolvidos especificamente para a operação da CONTRATANTE poderão ser utilizados internamente por ela, desde que todos os valores devidos à CONTRATADA estejam integralmente pagos.

**7.5.** Permanecem de titularidade da CONTRATADA seus métodos, modelos, templates, estruturas, know-how, conceitos e materiais preexistentes ou reaproveitáveis, ainda que utilizados na execução deste Contrato.

**7.6.** A CONTRATANTE não poderá comercializar, sublicenciar, ceder ou disponibilizar a terceiros os materiais e métodos da CONTRATADA sem autorização prévia e escrita.

---

## CLÁUSULA OITAVA – DAS RESPONSABILIDADES E DISPOSIÇÕES GERAIS

**8.1.** A CONTRATADA responde pelos serviços prestados dentro dos limites deste Contrato, não respondendo por decisões comerciais, trabalhistas, financeiras, tributárias, regulatórias ou de gestão interna tomadas exclusivamente pela CONTRATANTE.

**8.2.** A responsabilidade da CONTRATADA por perdas diretas comprovadamente causadas por culpa exclusiva sua fica limitada {{ limite_responsabilidade | default("ao valor total efetivamente pago a título de investimento inicial") }}, exceto em caso de dolo.

**8.3.** Nenhuma tolerância ou omissão será interpretada como renúncia de direito. Qualquer alteração deste Contrato somente terá validade se feita por escrito e assinada por ambas as Partes. Este Contrato substitui entendimentos anteriores sobre o mesmo objeto.

---

## CLÁUSULA NONA – DO FORO

**9.1.** Fica eleito o {{ singular.foro_descricao }}, com renúncia a qualquer outro, por mais privilegiado que seja, para dirimir quaisquer controvérsias oriundas deste Contrato.

E, por estarem justas e contratadas, as Partes assinam o presente instrumento em 2 (duas) vias de igual teor e forma, juntamente com 2 (duas) testemunhas.

---

{{ cidade_assinatura | default(singular.foro_cidade) }}/{{ singular.foro_uf }}, {{ data_assinatura }}.

---

___________________________________
**CONTRATANTE**
{{ parte.nome }}
Representante: {{ parte.representante }}
CPF: {{ parte.cpf_representante }}

___________________________________
**CONTRATADA**
{{ singular.razao_social }}
Representante: {{ singular.representante_nome }}
CPF: {{ singular.representante_cpf }}

---

**Testemunha 1**
Nome: ___________________________________
CPF: ___________________________________

**Testemunha 2**
Nome: ___________________________________
CPF: ___________________________________
