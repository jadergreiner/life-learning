## ADDED Requirements

### Requirement: O estado dos componentes LAB02 é documentado sem contradições
O documento de integração SHALL identificar SQS/DLQ, Lambda preparatória e PostgreSQL em RDS, as responsabilidades atuais de cada peça e as integrações ainda ausentes, distinguindo fatos provisionados de comportamento não iniciado.

#### Scenario: Leitor avalia o baseline
- **WHEN** o leitor consulta o inventário do plano
- **THEN** encontra o estado atual de cada componente, seus limites conhecidos e a ausência de fluxo SQS-Lambda-PostgreSQL ativo

#### Scenario: Resumos de status são consultados
- **WHEN** o leitor consulta os resumos do LAB02, Terraform e contrato ED-05
- **THEN** eles não afirmam que Lambda, RDS ou configuração Terraform executável estão ausentes e não afirmam que o processamento ou a sessão U2.1 começou

### Requirement: O plano de integração é faseado e verificável
O documento SHALL apresentar uma sequência de integração SQS → Lambda → PostgreSQL com pré-requisitos, decisões, riscos, critério de saída e evidência esperada em cada etapa, cobrindo contrato da mensagem, modelo/migração de dados, conectividade privada, identidade/segredos, entrega/retry/DLQ, observabilidade, validação AWS-01–AWS-07, custos e teardown.

#### Scenario: Etapas são avaliadas antes de implementação
- **WHEN** uma etapa do plano é revisada
- **THEN** estão explícitos seus pré-requisitos, o que precisa ser decidido ou implementado, como verificar o resultado e qual etapa depende dela

#### Scenario: Critérios existentes são preservados
- **WHEN** o plano descreve validação de integração
- **THEN** referencia AWS-01–AWS-07 sem alterar ou acrescentar gates de aprovação do contrato ED-05

### Requirement: A autonomia pedagógica I0 é preservada
O plano SHALL descrever responsabilidades e perguntas sobre duplicatas, concorrência, transações, falhas após commit e falha parcial sem escolher pelo aluno a solução de idempotência ou apresentar implementação de referência.

#### Scenario: Desafio independente continua aberto
- **WHEN** o aluno usa o documento para preparar a integração
- **THEN** encontra questões e critérios para defender o próprio desenho, sem receber uma resposta pronta para o desafio I0

### Requirement: O plano não executa mudanças operacionais
Esta mudança SHALL limitar-se a documentação: não altera código ou configuração de runtime/infraestrutura, não provisiona nem modifica recursos AWS, não executa ensaios de integração e não inicia a sessão U2.1.

#### Scenario: Proposta documental concluída
- **WHEN** os artefatos desta mudança são concluídos
- **THEN** Terraform, Lambda, IAM, rede, banco e filas permanecem sem alterações por esta mudança, e nenhum teste AWS-01–AWS-07 é executado
