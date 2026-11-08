## Context

O LAB02 hoje é composto por fila SQS Standard e DLQ, uma Lambda `lab02-processor` cujo handler apenas responde `{"status":"ready"}`, e PostgreSQL em RDS. O root Terraform gerencia os três componentes, mas a Lambda não tem event source mapping, configuração VPC, permissões SQS ou acesso ao secret/banco; o security group do RDS não tem ingress e o banco ainda não tem schema ou usuário de aplicação. O RDS usa endpoint privado e senha master gerenciada pelo RDS em Secrets Manager.

O contrato de ED-05 preserva o desafio I0: o aluno deve defender as garantias de SQS, Lambda e PostgreSQL diante de duplicatas, concorrência, falha após commit e lote parcialmente inválido. Os ensaios AWS-01–AWS-07 são gates de avaliação existentes. `labs/lab02/README.md`, `labs/lab02/terraform/README.md` e `docs/ed05-u2-aws.md` ainda contêm declarações de inventário anteriores ao provisionamento de Lambda/RDS/Terraform executável.

## Goals / Non-Goals

**Goals:**

- Registrar um inventário coerente dos componentes implementados e das integrações ainda ausentes.
- Criar um plano faseado, com pré-requisitos, decisões em aberto, critérios de saída e evidências para integrar SQS, Lambda e PostgreSQL.
- Organizar as preocupações de contrato de mensagem, rede/segredos, permissões, falhas/reentrega, persistência, observabilidade, custos e teardown.
- Manter o desafio I0 e os critérios AWS-01–AWS-07 como definidos no contrato pedagógico.
- Atualizar as descrições de estado nos documentos de inventário sem declarar iniciada a sessão U2.1 ou o processamento.

**Non-Goals:**

- Alterar Terraform, código Lambda, IAM, rede, schema, banco, filas ou recursos AWS.
- Escolher pelo aluno um algoritmo de idempotência, estratégia transacional final, sizing de concorrência/lote ou desenho definitivo de endpoints de rede.
- Abrir ou registrar a sessão U2.1 no Notion, mudar a cadência pedagógica ou aprovar competências.
- Executar testes AWS-01–AWS-07, enviar mensagens, invocar Lambda, conectar ao banco ou alterar custos.

## Decisions

1. **Publicar um documento único em `labs/lab02/integration-plan.md`.** Ele será a referência técnica do plano entre os módulos e separará fatos observados, gaps, decisões a defender, sequência sugerida e gates. Alternativa considerada: distribuir a sequência pelos READMEs dos módulos; rejeitada porque fragmentaria dependências transversais e critérios de saída.

2. **Organizar as integrações em etapas com gates, sem prescrever a solução do I0.** A sequência cobre (a) reconciliação do baseline e defesa independente da arquitetura; (b) contrato do evento e modelo de persistência; (c) rede privada, identidade da aplicação e acesso ao secret; (d) associação SQS–Lambda, retry, lote e DLQ; (e) observabilidade; (f) ensaios AWS-01–AWS-07 e evidências; (g) custo, autorização e teardown. Cada etapa listará pré-requisitos, decisões e critério verificável de conclusão. Não fixará parâmetros numéricos que o contrato exige justificar.

3. **Tratar semânticas de falha como decisões e critérios, não como receita.** O documento explicará que SQS Standard pode duplicar entregas, que o retorno da Lambda afeta retry/lotes e que a persistência deve sustentar o invariante de negócio. O aluno continua responsável por defender como obter o resultado; alternativas de mecanismo podem ser registradas como perguntas de comparação, sem código ou resposta de referência.

4. **Registrar limites de rede e credenciais sem antecipar alterações.** O plano identifica a necessidade futura de Lambda em VPC para alcançar o endpoint privado, regra mínima Lambda-SG → RDS-SG na porta PostgreSQL, acesso ao secret restrito, e escolha justificada de caminho de saída/endpoints. Não assume NAT, VPC endpoint, regra ingress, role de aplicação ou modo de conexão como decidido; a etapa futura deverá comparar custo, escopo e superfície de rede antes de qualquer provisionamento.

5. **Reconciliar apenas afirmações factuais em documentos existentes.** Atualizar os inventários de LAB02/Terraform e o estado descritivo do contrato ED-05 para indicar recursos presentes, ausência de fluxo integrado e sessão U2.1 não iniciada. Preservar invariantes, critérios AWS-01–AWS-07, fonte Notion e gates de autorização. Alternativa considerada: alterar só o plano novo; rejeitada porque deixaria instruções operacionais antigas contraditórias.

6. **Nenhuma execução operacional nesta mudança.** A entrega é documentação revisável. Infraestrutura, plano de deploy, sessão pedagógica e eventual liberação de custo exigem mudança e autorização próprias.

## Risks / Trade-offs

- [Um plano técnico pode entregar a resposta do desafio I0] → apresentar responsabilidades, falhas e perguntas de decisão sem escolher o desenho de idempotência ou fornecer implementação de referência.
- [Documentos de inventário podem voltar a divergir] → nomear o documento de integração como referência de sequência e alinhar os três resumos existentes no mesmo conjunto de tarefas.
- [A etapa de rede pode criar custo ou exposição indevida] → deixar opções de endpoint/saída em aberto, exigir regra mínima e estimativa antes de uma mudança operacional separada.
- [Critérios de ensaio podem ser confundidos com critérios novos] → reutilizar AWS-01–AWS-07 sem adicionar gates ou alterar o contrato de aprovação.
- [Sizings podem envelhecer ou depender de escolhas do aluno] → registrar como decisões a validar, não como defaults imutáveis.

## Migration Plan

1. Revisar os módulos, outputs, specs e contrato ED-05 para compor o inventário factual e identificar afirmações obsoletas.
2. Criar `labs/lab02/integration-plan.md` com estado atual, gaps, fases, dependências, decisões, critérios e evidências.
3. Atualizar `labs/lab02/README.md`, `labs/lab02/terraform/README.md` e `docs/ed05-u2-aws.md` para distinguir componentes provisionados de processamento e sessão ainda não iniciados.
4. Validar referências, escopo e consistência documental; revisar que não houve alteração em Terraform ou código/runtime.
5. Para rollback documental, reverter apenas as alterações desses documentos; nenhum recurso AWS é alterado por esta mudança.

## Open Questions

- Qual padrão de migração e qual modelo mínimo de dados o aluno defenderá para satisfazer AWS-01–AWS-05?
- Qual opção de conectividade para Lambda privada e Secrets Manager será justificada considerando o custo e as rotas existentes?
- Quais parâmetros de event source mapping, visibility timeout, concorrência e resposta parcial serão escolhidos depois da defesa I0?
- Qual teto de gasto e janela operacional serão aprovados antes das fases que criem ou alterem recursos?
