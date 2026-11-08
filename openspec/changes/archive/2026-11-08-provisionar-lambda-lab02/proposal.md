## Why

O LAB02 já tem fila SQS e DLQ provisionadas, mas o módulo `modules/processor` continua sendo apenas um placeholder. Uma função Lambda mínima, executável e preparada para extensão cria uma base implantável sem antecipar a integração SQS, a conexão com banco ou o comportamento pedagógico do processador.

## What Changes

- Criar uma capacidade Terraform para uma única função Lambda preparatória, com pacote executável mínimo, execution role de privilégio mínimo e logging básico.
- Compor essa função no root module Terraform do LAB02, preservando a validação da conta-alvo e o state local existente.
- Deixar event source mapping SQS, integração com RDS/VPC, produção de mensagens, processamento financeiro, concorrência, retries e tratamento de lote para mudanças posteriores.
- Atualizar o contrato do ambiente LAB02, que atualmente limita o root module aos recursos SQS.

## Capabilities

### New Capabilities
- `lab02-lambda-foundation`: uma função Lambda inicial, executável e observável, com role e permissões básicas de logging.

### Modified Capabilities
- `sqs-lab02-environment`: expandir a composição aprovada do root module para incluir a função Lambda preparatória além da fila e da DLQ, sem incluir integrações futuras.

## Impact

- `labs/lab02/terraform/modules/processor/` deixa de ser somente placeholder e passa a fornecer a função e seu pacote mínimo.
- `labs/lab02/terraform/environments/lab/` passa a compor a função existente no ambiente SQS.
- O usuário IAM Terraform `lab02-terraform` precisará de permissões delimitadas para administrar os recursos Lambda e a execution role específica; a função precisa somente de acesso a logs nesta etapa.
- A alteração do ambiente AWS cria custo de invocação e logging sujeito a uso; não cria mapping SQS, rede ou banco.
