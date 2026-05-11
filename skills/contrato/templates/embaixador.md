# CONTRATO DE PRESTAÇÃO DE SERVIÇO DE MARKETING

## Das Partes

**CONTRATANTE:** {{ singular.razao_social }}, pessoa jurídica de direito privado inscrita no CNPJ sob nº {{ singular.cnpj }}, com sede no {{ singular.endereco_completo }}, neste ato representada por seu administrador legal, **{{ singular.representante_nome }}**, {{ singular.representante_estado_civil }}, {{ singular.representante_profissao }}, inscrito no CPF sob nº {{ singular.representante_cpf }}, doravante denominado **CONTRATANTE**.

**CONTRATADA:** **{{ parte.nome }}**, pessoa física de direito privado inscrita no CPF sob nº {{ parte.documento }}{% if parte.rg %}, portador(a) do RG nº {{ parte.rg }}{% endif %}, com endereço {{ parte.endereco }}{% if parte.bairro %}, {{ parte.bairro }}{% endif %}, {{ parte.cidade_uf }}, CEP {{ parte.cep }}{% if parte.profissao %}, {{ parte.profissao }}{% endif %}, doravante denominada **CONTRATADA**.

---

{% set ns = namespace(n=0) %}
## Do objeto

{% set ns.n = ns.n + 1 %}**{{ ns.n }}.** O presente instrumento tem como objeto a prestação de serviços, pela CONTRATADA, de **{{ objeto | default("liderança em projetos e serviços fornecidos pela CONTRATANTE, quais sejam: prestação de serviços de modelagem de processos e aplicação de captação ativa enquanto executiva comercial") }}**.

{% set ns.n = ns.n + 1 %}**{{ ns.n }}.** A CONTRATADA obriga-se a {{ obrigacao_cadastro | default("cadastrar novas empresas parceiras/clientes na plataforma digital da CONTRATANTE, conforme treinamento prévio oferecido") }}.

{% set ns.n = ns.n + 1 %}**{{ ns.n }}.** A CONTRATANTE fornecerá à CONTRATADA o suporte tecnológico necessário à prestação do serviço como acesso à sistemas, software e banco de dados da CONTRATANTE.

{% set ns.n = ns.n + 1 %}**{{ ns.n }}.** A zona de atuação de vendas da CONTRATADA é livre, de modo que as despesas, se necessárias, com locomoção, hospedagem, alimentação, comunicações, contratação de pessoal, correm por conta única e exclusiva da CONTRATADA.

{% set ns.n = ns.n + 1 %}**{{ ns.n }}.** CONTRATANTE e CONTRATADA se comprometem a realizar reuniões remotas periódicas, a fim de sanar dúvidas, dar suporte recíproco sobre o objeto do presente contrato, bem como fazer ajustes e trocar informações que entendam necessárias.

---

## Do treinamento

{% set ns.n = ns.n + 1 %}**{{ ns.n }}.** A CONTRATADA receberá da CONTRATANTE treinamento e capacitação, na modalidade *curso livre*, o qual terá carga horária total de **{{ treinamento_horas | default(40) }} horas**{% if treinamento_valor %}, valorado em **{{ treinamento_valor }}**{% endif %}, caracterizado como investimento da CONTRATANTE na parceria objeto deste contrato. Este treinamento visa o aperfeiçoamento da produtividade e otimização de tempo e recursos para as melhores práticas de Organização e Métodos.

---

## Do pagamento

{% set ns.n = ns.n + 1 %}**{{ ns.n }}.** O presente contrato tem como principal característica a autonomia da CONTRATADA cuja remuneração se dará na modalidade de comissão, devida de acordo com os projetos envolvidos, sendo devido a comissão por êxito em **{{ percentual_comissao | default("20% (vinte por cento)") }}** {{ base_comissao | default("sobre as vendas do Powercoffee") }}.

{% set ns.n = ns.n + 1 %}**{{ ns.n }}.** {{ meta_ajuste | default("Ao atingirmos 80 (oitenta) vendas de embalagens de 270g do Powercoffee, o contrato de comissionamento será ajustado para a nova margem.") }}

{% set ns.n = ns.n + 1 %}**{{ ns.n }}.** O pagamento por êxito devido pela CONTRATANTE à CONTRATADA será efetuado todo **{{ dia_pagamento | default("5º (quinto) dia útil") }}** do mês subsequente à assinatura do contrato, e se dará por meio de depósito/transferência bancária em sua conta corrente, a saber.

{% if bonificacao_renovacao %}{% set ns.n = ns.n + 1 %}**{{ ns.n }}.** A CONTRATADA receberá bonificação de **{{ bonificacao_renovacao }}** quando a empresa parceira/cliente por ela gerenciada atingir **{{ prazo_bonificacao | default("3 (três) meses") }}** de contrato com a CONTRATANTE e garantir sua renovação.

{% endif %}{% set ns.n = ns.n + 1 %}**{{ ns.n }}.** Este contrato **não é de caráter exclusivo**, podendo a CONTRATADA estipular idêntico contrato com outra empresa, distribuidor, representante ou prestadora de serviços, observadas as cláusulas de confidencialidade e propriedade intelectual deste contrato. Assim como a CONTRATANTE firmar contratos da mesma natureza com outras empresas e/ou prestadores de serviços.

---

## Da propriedade intelectual

{% set ns.n = ns.n + 1 %}**{{ ns.n }}.** Todos e quaisquer direitos de propriedade intelectual ou industrial decorrentes e/ou relativos aos serviços descritos neste contrato, incluindo, mas não se limitando, aos direitos autorais patrimoniais, pertencem única e exclusivamente à CONTRATANTE. Em nenhuma hipótese o contrato implica transferência, no todo ou em parte, de qualquer direito de propriedade intelectual ou industrial pela CONTRATANTE à CONTRATADA. A CONTRATADA expressamente reconhece e concorda que as regras aqui estabelecidas se estendem a todo e qualquer software cujo uso venha a ser autorizado pela CONTRATANTE no âmbito da prestação dos serviços descritos neste contrato.

**{{ ns.n }}.1.** A divulgação de qualquer **INFORMAÇÃO CONFIDENCIAL**, devidamente comprovada, sem autorização expressa da CONTRATANTE, possibilitará a imediata extinção de qualquer contrato firmado entre as **PARTES**, sem qualquer ônus para a CONTRATANTE.

**{{ ns.n }}.2.** No caso de violação do presente acordo, a CONTRATADA estará obrigada ao pagamento de multa contratual no valor de **{{ multa_violacao | default("R$ 100.000,00 (cem mil reais)") }}** com prazo de **{{ prazo_multa | default("3 (três) anos") }}**, independente de recomposição de todas as perdas e danos apurados sofridos pela CONTRATANTE, inclusive as de ordem moral ou concorrencial, bem como as de responsabilidades civil e criminal respectivas, as quais serão apuradas em regular processo judicial ou administrativo.

---

## Da confidencialidade

{% set ns.n = ns.n + 1 %}**{{ ns.n }}.** A CONTRATADA se compromete a não utilizar em benefício próprio, nem compartilhar com terceiros, os dados cadastrais das empresas parceiras e/ou clientes da CONTRATANTE.

{% set ns.n = ns.n + 1 %}**{{ ns.n }}.** A CONTRATADA, ao acessar programas e plataformas virtuais da CONTRATANTE, fica vedada a utilização para quaisquer fins que não aqueles determinados no objeto do presente contrato.

{% set ns.n = ns.n + 1 %}**{{ ns.n }}.** As Partes se obrigam a manter total confidencialidade das informações obtidas em razão deste contrato, sejam elas classificadas como confidenciais ou não, abrangendo, mas não se limitando, àquelas relacionadas às atividades da empresa, estratégias de negócios, produtos em desenvolvimento, dados financeiros e estatísticos, negociações em andamento, informações sobre softwares, informações cadastrais de empresas parceiras, clientes, fornecedores e parceiros comerciais, senhas, entre outras, que sejam de propriedade exclusiva da CONTRATANTE ou de terceiros entregues à guarda da CONTRATADA.

{% set ns.n = ns.n + 1 %}**{{ ns.n }}.** As vedações relativas à propriedade intelectual e à confidencialidade deste contrato permanecerão em vigor por **prazo indeterminado**, sobrevivendo ao término, rescisão ou resilição deste contrato por qualquer motivo. Comprometendo-se a CONTRATADA a cumprir com os termos da **Lei nº 13.709/2018 (Lei Geral de Proteção de Dados — LGPD)**, bem como outras legislações aplicáveis à proteção de dados pessoais e à garantia da privacidade dos usuários cadastrados.

---

## Do prazo

{% set ns.n = ns.n + 1 %}**{{ ns.n }}.** O presente contrato terá vigência por **{{ vigencia | default("tempo indeterminado") }}**, podendo ser rescindido por qualquer das partes, a qualquer tempo, desde que noticiando a parte contrária com antecedência mínima de **{{ aviso_rescisao | default("30 (trinta) dias") }}**, observada a cláusula de pagamento deste contrato.

{% set ns.n = ns.n + 1 %}**{{ ns.n }}.** Em qualquer hipótese de rescisão contratual, a CONTRATADA procederá a devolução de todo o material fornecido pela CONTRATANTE, que estiver em seu poder, a saber: fichas, formulários, guias, material publicitário, e outros afins, além de obrigar-se a deixar de fazer uso de qualquer senha, sinal ou marca de propaganda que se relacione à CONTRATANTE.

{% set ns.n = ns.n + 1 %}**{{ ns.n }}.** A CONTRATADA, no caso de extinção do presente contrato, por qualquer motivo, fica proibida de se utilizar, repassar ou divulgar, sob qualquer forma, informações sigilosas, produtos, serviços, senhas ou outras informações que tiver acesso em razão deste contrato, da CONTRATANTE ou das empresas parceiras/clientes, sob pena de multa pecuniária de **{{ multa_pos_extincao | default("10 (dez) salários-mínimos vigentes à época") }}**, bem como ser responsabilizada cível e criminalmente nos termos da lei.

{% set ns.n = ns.n + 1 %}**{{ ns.n }}.** As partes elegem o {{ singular.foro_descricao }} para dirimir eventuais litígios decorrentes deste contrato.

---

{{ cidade_assinatura | default(singular.foro_cidade) }}, {{ data_assinatura }}.

---

________________________
**CONTRATADA:** {{ parte.nome }}
CPF nº {{ parte.documento }}

________________________
**CONTRATANTE:** {{ singular.razao_social }}
CNPJ nº: {{ singular.cnpj }}
Representante: {{ singular.representante_nome }}
