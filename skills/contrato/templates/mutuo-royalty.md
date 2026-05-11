# INSTRUMENTO PARTICULAR DE MÚTUO COM AMORTIZAÇÃO VARIÁVEL ATRELADA À PERFORMANCE DE VENDAS

---

## 1. IDENTIFICAÇÃO DAS PARTES

De um lado, na qualidade de **MUTUANTE**:

**SINGULAR VENTURE LTDA**, pessoa jurídica de direito privado, inscrita no CNPJ/MF sob o nº {{ singular.cnpj }}, com sede no {{ singular.endereco_completo }}, neste ato representada, na forma de seu contrato social, pelo seu administrador legal **{{ singular.representante_nome }}**, {{ singular.representante_estado_civil }}, {{ singular.representante_profissao }}, inscrito no CPF/MF sob o nº {{ singular.representante_cpf }}, doravante denominada **{{ apelido_singular | default("SINGULAR") }}** ou simplesmente **MUTUANTE**.

E, de outro lado, na qualidade de **MUTUÁRIA**:

**{{ parte.nome }}**{% if parte.nome_fantasia %} (nome fantasia: {{ parte.nome_fantasia }}){% endif %}, pessoa jurídica de direito privado, inscrita no CNPJ/MF sob o nº {{ parte.documento }}, com sede em {{ parte.endereco }}, {{ parte.bairro }}, {{ parte.cidade_uf }}, CEP {{ parte.cep }}, neste ato representada, na forma de seu contrato/estatuto social, por seu(sua) representante legal **{{ parte.representante }}**, {% if parte.cpf_representante %}inscrito(a) no CPF/MF sob o nº {{ parte.cpf_representante }}, {% endif %}{% if parte.cargo %}na qualidade de {{ parte.cargo }}, {% endif %}doravante denominada **{{ parte.apelido }}** ou simplesmente **MUTUÁRIA**.

A MUTUANTE e a MUTUÁRIA, doravante denominadas em conjunto **PARTES** e individualmente **PARTE**, têm entre si, justa e contratada, a celebração do presente **Instrumento Particular de Mútuo com Amortização Variável Atrelada à Performance de Vendas** (doravante "Contrato"), com fundamento nos artigos 586 a 592 do Código Civil Brasileiro, mediante as cláusulas e condições a seguir.

---

## 2. CONSIDERAÇÕES PRELIMINARES

**CONSIDERANDO** que a MUTUÁRIA é sociedade empresária dedicada à fabricação, distribuição e comercialização do produto comercialmente conhecido como **{{ produto_nome | default("Power Coffee") }}** (doravante "Produto"), em todos os seus canais de venda (revenda, varejo direto, marketplaces, eventos, assinaturas e demais);

**CONSIDERANDO** que a MUTUÁRIA necessita de aporte de capital de giro para financiar a expansão de sua operação logística, comercial e de penetração de mercado do Produto;

**CONSIDERANDO** que a MUTUANTE detém recursos financeiros disponíveis e tem interesse em conceder mútuo em dinheiro à MUTUÁRIA, mediante restituição vinculada à performance de vendas do Produto, sem assumir, em hipótese alguma, qualquer participação societária, gestionária, deliberativa ou nos lucros da MUTUÁRIA;

**CONSIDERANDO** que as PARTES reconhecem expressamente que esta operação configura **mútuo civil** nos termos dos artigos 586 e seguintes do Código Civil, **NÃO constituindo** sociedade em conta de participação (artigos 991 a 996 do Código Civil), sociedade comum, consórcio, joint venture, vínculo associativo, participação nos lucros, nem qualquer outra forma de constituição societária ou parassocietária entre as PARTES;

**CONSIDERANDO** que o vínculo entre o valor restituído e a performance de vendas do Produto opera **exclusivamente como índice de cálculo do prazo e do ritmo de quitação** do valor mutuado, sem que a MUTUANTE assuma o risco do negócio, o resultado operacional ou qualquer responsabilidade pela gestão da MUTUÁRIA;

RESOLVEM as PARTES, em comum acordo e na melhor forma de direito, firmar o presente Contrato, que se regerá pelas seguintes cláusulas e condições.

---

## 3. OBJETO E VALOR DO MÚTUO

**3.1.** O presente instrumento tem por objeto o mútuo, em moeda corrente nacional, no valor de **R$ {{ valor_mutuo_numero | default("30.000,00") }} ({{ valor_mutuo_extenso | default("trinta mil reais") }})** (doravante "Valor Mutuado"), que a MUTUANTE entrega à MUTUÁRIA, neste ato ou na forma estabelecida na cláusula 3.2, mediante transferência bancária para conta de titularidade da MUTUÁRIA.

**3.2.** A liberação do Valor Mutuado dar-se-á da seguinte forma:

{% if liberacao_modo == "parcelada" %}{{ liberacao_descricao }}{% else %}**(a)** integralmente, em parcela única, no prazo de até 5 (cinco) dias úteis contados da assinatura deste Contrato, mediante transferência bancária para conta de titularidade da MUTUÁRIA cujos dados serão informados por escrito pela MUTUÁRIA à MUTUANTE.{% endif %}

**3.3.** A MUTUÁRIA destinará o Valor Mutuado integralmente a finalidades operacionais relacionadas à expansão da comercialização do Produto, observando-se princípios de boa gestão, prudência financeira e diligência empresarial.

**3.4.** As PARTES acordam que **não incidirão juros remuneratórios** sobre o Valor Mutuado, em razão de a contrapartida do mútuo estar contemplada na sistemática de amortização variável estabelecida na cláusula 4 deste Contrato. Por força da exceção expressamente pactuada, fica afastada a presunção do artigo 591 do Código Civil neste particular, sem prejuízo dos juros moratórios devidos em caso de inadimplemento (cláusula 7).

---

## 4. FORMA DE RESTITUIÇÃO — AMORTIZAÇÃO VARIÁVEL ATRELADA A VENDAS

**4.1.** A MUTUÁRIA obriga-se a restituir à MUTUANTE o Valor Mutuado mediante pagamentos mensais calculados pela fórmula:

> **Pagamento mensal = R$ {{ royalty_unitario_numero | default("3,00") }} ({{ royalty_unitario_extenso | default("três reais") }}) × Unidades do Produto vendidas no mês de referência**

considerando-se "Unidades vendidas" o total de unidades do Produto efetivamente comercializadas pela MUTUÁRIA, em todos os seus canais de distribuição, no mês civil imediatamente anterior ao do pagamento, líquido de cancelamentos, devoluções confirmadas e estornos formalmente registrados.

**4.2. Teto Total de Restituição (Cap).** A obrigação de restituição da MUTUÁRIA limita-se ao montante cumulativo de **R$ {{ cap_numero | default("90.000,00") }} ({{ cap_extenso | default("noventa mil reais") }})** (doravante "Teto"), englobando o Valor Mutuado e todo e qualquer acréscimo decorrente da sistemática de amortização aqui pactuada. Atingido o Teto, a MUTUÁRIA estará automaticamente desonerada de qualquer pagamento adicional, com plena e geral quitação ao término dos pagamentos.

**4.3. Periodicidade e prazo de pagamento.** Os pagamentos mensais serão efetuados pela MUTUÁRIA até o **{{ dia_pagamento | default("10º (décimo)") }} dia útil de cada mês**, mediante transferência bancária para conta de titularidade da MUTUANTE, tendo por base as Unidades vendidas no mês civil imediatamente anterior.

**4.4. Início dos pagamentos.** O primeiro pagamento será devido no mês subsequente ao da liberação integral do Valor Mutuado, tendo por base de cálculo as Unidades vendidas no mês de liberação.

**4.5. Mês sem vendas.** Caso, em determinado mês de referência, não haja Unidades vendidas, o pagamento mensal correspondente será de R$ 0,00 (zero), sem que isto configure mora ou inadimplemento, observado o disposto na cláusula 6 quanto à prestação de contas e na cláusula 7 quanto às hipóteses de vencimento antecipado.

**4.6. Prazo máximo do mútuo.** Independentemente da sistemática de amortização, o prazo máximo de vigência da obrigação de pagamento é de **{{ prazo_maximo_meses | default("60 (sessenta)") }} meses** contados da liberação integral do Valor Mutuado. Ao final desse prazo, caso o Teto não tenha sido atingido, o saldo remanescente entre o Valor Mutuado e o total efetivamente pago tornar-se-á imediatamente exigível, vencido e cobrável pela MUTUANTE, com os acréscimos da cláusula 7.

**4.7. Quitação antecipada.** É facultado à MUTUÁRIA antecipar pagamentos a qualquer tempo, total ou parcialmente, sem incidência de qualquer multa ou penalidade, com correspondente abatimento sobre o Teto.

---

## 5. NATUREZA DA RELAÇÃO E LIMITES EXPRESSOS

**5.1. Mútuo civil puro.** As PARTES declaram expressamente, para todos os fins de direito, que o presente Contrato configura **mútuo civil**, regido pelos artigos 586 a 592 do Código Civil, e **não** constitui:

- **(a)** sociedade em conta de participação (artigos 991 a 996 do Código Civil) nem qualquer outra forma de sociedade, formal ou informal;
- **(b)** consórcio empresarial, joint venture, parceria empresarial nem aliança estratégica;
- **(c)** vínculo empregatício, prestação de serviços, representação comercial ou qualquer relação contratual diversa do mútuo;
- **(d)** participação da MUTUANTE nos lucros, prejuízos, resultados ou patrimônio da MUTUÁRIA;
- **(e)** direito da MUTUANTE de interferir, opinar, deliberar ou fiscalizar a gestão administrativa, operacional, comercial ou financeira da MUTUÁRIA;
- **(f)** assunção pela MUTUANTE de qualquer risco do negócio da MUTUÁRIA, de obrigações trabalhistas, fiscais, previdenciárias, ambientais ou de qualquer outra natureza assumidas pela MUTUÁRIA perante terceiros.

**5.2. Indexador como métrica de prazo.** O vínculo entre o ritmo dos pagamentos e as Unidades vendidas tem natureza exclusivamente de **índice de cálculo do prazo e do ritmo de quitação** do Valor Mutuado. As PARTES reconhecem que a sistemática descrita na cláusula 4 é equivalente, na sua essência, a um cronograma variável de amortização, em que a velocidade de pagamento varia conforme uma métrica objetiva, mas o conteúdo da obrigação permanece sendo o de restituir até o Teto.

**5.3. Inexistência de affectio societatis.** As PARTES declaram a inexistência de affectio societatis entre si, não havendo intenção de partilhar resultados ou riscos do negócio da MUTUÁRIA.

**5.4. Independência operacional.** A MUTUÁRIA mantém total autonomia e responsabilidade exclusiva por sua gestão, decisões comerciais, definição de preços, escolha de canais, estratégia de marketing, seleção de fornecedores, contratação de empregados e prestadores de serviço e quaisquer outras decisões empresariais, não havendo qualquer ingerência ou direito de veto da MUTUANTE.

---

## 6. PRESTAÇÃO DE CONTAS E TRANSPARÊNCIA

**6.1. Relatório mensal de vendas.** A MUTUÁRIA enviará à MUTUANTE, até o **{{ dia_relatorio | default("5º (quinto)") }} dia útil de cada mês**, relatório eletrônico contendo, no mínimo:

- **(a)** quantidade total de Unidades do Produto vendidas no mês civil imediatamente anterior, segregadas por canal de distribuição (revenda, site, eventos, assinaturas e demais);
- **(b)** quantidade de cancelamentos, devoluções e estornos do mesmo período;
- **(c)** memória de cálculo do pagamento mensal devido;
- **(d)** saldo cumulativo restituído à MUTUANTE em relação ao Teto.

**6.2. Direito de auditoria limitada.** A MUTUANTE poderá, mediante aviso prévio de 15 (quinze) dias, requerer auditoria limitada e proporcional dos registros de venda do Produto, em horário comercial e sem prejuízo das atividades da MUTUÁRIA, exclusivamente para conferência das informações reportadas no relatório mensal. A auditoria não autoriza acesso a informações sobre fornecedores, custos, margens, estratégia, recursos humanos ou demais aspectos da gestão da MUTUÁRIA, em respeito aos limites da cláusula 5.

**6.3. Confidencialidade dos dados.** A MUTUANTE compromete-se a manter sob estrita confidencialidade os dados de vendas e demais informações empresariais a que tenha acesso em razão deste Contrato, não podendo divulgá-los a terceiros, salvo por exigência legal ou ordem judicial. Esta obrigação subsiste por 5 (cinco) anos após o término deste Contrato.

**6.4. Boa-fé objetiva.** As PARTES comprometem-se a agir, ao longo da execução deste Contrato, com observância dos princípios da probidade e da boa-fé objetiva (artigo 422 do Código Civil), inclusive em seus deveres anexos de informação, lealdade, cooperação e proteção mútua.

---

## 7. INADIMPLEMENTO, MORA E VENCIMENTO ANTECIPADO

**7.1. Mora.** Caracteriza-se mora da MUTUÁRIA o atraso superior a 10 (dez) dias corridos no pagamento de qualquer parcela mensal devida nos termos da cláusula 4, ou no envio do relatório mensal previsto na cláusula 6.1.

**7.2. Encargos moratórios.** Sobre os valores em atraso incidirão, cumulativamente:

- **(a)** correção monetária pelo IPCA/IBGE, ou índice que vier a substituí-lo;
- **(b)** **juros de mora** equivalentes à taxa SELIC (artigo 406 do Código Civil), pro rata die, contados da data do vencimento até o efetivo pagamento;
- **(c)** **multa moratória** de **2% (dois por cento)** sobre o valor inadimplido, observado o limite do artigo 412 do Código Civil.

**7.3. Vencimento antecipado.** Tornar-se-ão automaticamente vencidas, exigíveis e cobráveis a totalidade do saldo do Valor Mutuado ainda não restituído, acrescido dos encargos da cláusula 7.2, nas seguintes hipóteses:

- **(a)** inadimplemento, pela MUTUÁRIA, de qualquer obrigação pecuniária deste Contrato por prazo superior a 60 (sessenta) dias corridos, após notificação extrajudicial;
- **(b)** descumprimento reiterado da obrigação de prestação de contas (cláusula 6.1) por 2 (dois) meses consecutivos ou 3 (três) alternados em período de 12 (doze) meses, após notificação extrajudicial e prazo de 15 (quinze) dias para regularização;
- **(c)** decretação de falência, deferimento de recuperação judicial ou extrajudicial, dissolução, liquidação ou estado de insolvência reconhecido judicialmente da MUTUÁRIA;
- **(d)** alienação, transferência ou cessão, em ato único ou em série de atos correlacionados, de mais de 50% (cinquenta por cento) do controle societário da MUTUÁRIA, sem anuência prévia da MUTUANTE;
- **(e)** descontinuidade definitiva da fabricação e comercialização do Produto pela MUTUÁRIA por prazo superior a 6 (seis) meses consecutivos, sem solução de substituição ou continuidade acordada por escrito entre as PARTES;
- **(f)** demais hipóteses do artigo 333 do Código Civil.

**7.4. Saldo exigível em vencimento antecipado.** Em qualquer das hipóteses da cláusula 7.3, considerar-se-á imediatamente exigível **a diferença positiva entre o Valor Mutuado e os valores efetivamente restituídos até a data do evento**, em moeda corrente nacional, acrescida dos encargos moratórios da cláusula 7.2 e demais cominações legais. A MUTUANTE não fará jus, em caso de vencimento antecipado, ao Teto integral, mas tão-somente ao Valor Mutuado, descontados os pagamentos já efetuados, salvo prova de que o vencimento antecipado decorreu de simulação ou fraude da MUTUÁRIA, hipótese em que será devida indenização suplementar nos termos do artigo 416, parágrafo único, do Código Civil.

**7.5. Cláusula penal.** As multas previstas neste Contrato observam o limite do artigo 412 do Código Civil e poderão ser equitativamente reduzidas pelo juízo, na forma do artigo 413 do Código Civil, em hipóteses de cumprimento parcial ou de manifesto excesso, sendo esta disposição irrenunciável pelas PARTES, conforme Enunciado 355 do CJF.

---

## 8. GARANTIAS E SITUAÇÃO ECONÔMICA DA MUTUÁRIA

**8.1.** O presente mútuo é celebrado **sem garantias reais ou fidejussórias**, em razão da relação de confiança entre as PARTES.

**8.2.** Nos termos do artigo 590 do Código Civil, a MUTUANTE poderá exigir garantia da restituição caso, antes do final do prazo de pagamento, a MUTUÁRIA sofra notória mudança em sua situação econômica que comprometa a expectativa de adimplemento, ficando facultado à MUTUÁRIA prestar garantia adequada (real, pessoal ou societária) no prazo de 30 (trinta) dias contados da notificação extrajudicial pela MUTUANTE.

**8.3.** A recusa injustificada em prestar garantia, nos termos da cláusula 8.2, autoriza a MUTUANTE a invocar o vencimento antecipado do mútuo, na forma da cláusula 7.3.

---

## 9. CESSÃO E SUCESSÃO

**9.1.** Nenhuma das PARTES poderá ceder ou transferir, total ou parcialmente, os direitos e obrigações decorrentes deste Contrato, salvo mediante prévia e expressa anuência por escrito da outra PARTE.

**9.2.** Excetua-se da vedação da cláusula 9.1 a cessão pela MUTUANTE de seus direitos creditórios decorrentes deste Contrato, hipótese em que bastará a comunicação prévia por escrito à MUTUÁRIA.

**9.3.** Os direitos e obrigações deste Contrato vinculam as PARTES, seus sucessores e cessionários autorizados, a qualquer título.

---

## 10. DISPOSIÇÕES GERAIS

**10.1. Tributação.** Cada PARTE será responsável, exclusivamente, pelos tributos incidentes sobre seus respectivos resultados decorrentes deste Contrato, nos termos da legislação aplicável.

**10.2. Comunicações.** Toda e qualquer comunicação entre as PARTES decorrente deste Contrato será feita por escrito, considerando-se válida quando enviada por carta registrada, e-mail com confirmação de recebimento ou aplicativo de mensageria, para os endereços indicados na qualificação das PARTES, ou outros que vierem a ser informados por notificação prévia.

**10.3. Tolerância.** A eventual tolerância de qualquer das PARTES quanto ao descumprimento de cláusulas deste Contrato pela outra não constituirá novação, renúncia ou alteração tácita de seus termos, nem impedirá a exigência de seu integral cumprimento.

**10.4. Validade parcial.** A invalidade ou ineficácia de qualquer cláusula deste Contrato não afetará a validade das demais, comprometendo-se as PARTES a, em boa-fé, substituir a cláusula viciada por outra que produza efeitos econômicos equivalentes.

**10.5. Alterações.** Qualquer alteração, modificação ou aditamento deste Contrato somente terá validade se formalizado por escrito e assinado por ambas as PARTES.

**10.6. Lei aplicável.** Este Contrato rege-se pelas leis da República Federativa do Brasil, em especial pelos artigos 586 a 592 e demais dispositivos aplicáveis do Código Civil.

**10.7. Foro.** Para dirimir quaisquer questões oriundas deste Contrato, as PARTES elegem o {{ singular.foro_descricao }}, com renúncia expressa a qualquer outro, por mais privilegiado que seja.

---

## 11. ENCERRAMENTO

E, por estarem assim justas e contratadas, as PARTES firmam o presente Contrato em 2 (duas) vias de igual teor e forma, na presença das testemunhas abaixo, para que produza seus regulares efeitos jurídicos.

---

{{ cidade_assinatura | default(singular.foro_cidade) }}/{{ singular.foro_uf }}, {{ data_assinatura }}.

---

**MUTUANTE:**

_________________________________________
**SINGULAR VENTURE LTDA**
CNPJ nº {{ singular.cnpj }}
Por: {{ singular.representante_nome }}
CPF nº {{ singular.representante_cpf }}

---

**MUTUÁRIA:**

_________________________________________
**{{ parte.nome }}**
CNPJ nº {{ parte.documento }}
Por: {{ parte.representante }}{% if parte.cpf_representante %}
CPF nº {{ parte.cpf_representante }}{% endif %}

---

**TESTEMUNHAS:**

1. _________________________________________
   Nome:
   CPF:

2. _________________________________________
   Nome:
   CPF:
