## Why

O módulo SQS do LAB02 está implementado e validado, mas ainda não há root module no ambiente `environments/lab` para compô-lo, planejar e manter seu state. Criar essa composição torna possível provisionar somente a fila principal e a DLQ autorizadas, com parâmetros revisáveis e ciclo de limpeza explícito.

## What Changes

- Criar root module do ambiente LAB02 que configura o AWS Provider e instancia `modules/queue`.
- Definir state local ignorado pelo Git, entradas explícitas para região, prefixo e parâmetros da fila, e outputs para inspeção.
- Documentar pré-requisitos, revisão do plano, aplicação autorizada e teardown.
- Provisionar somente as duas filas SQS após plano e custo serem revisados; não compor Lambda, RDS, IAM, rede ou CloudWatch.

## Capabilities

### New Capabilities
- `sqs-lab02-environment`: composição e ciclo de vida do ambiente Terraform que instancia apenas o módulo de fila SQS do LAB02.

### Modified Capabilities
- Nenhuma.

## Impact

- `labs/lab02/terraform/environments/lab`: root module, documentação e regras locais de state/variáveis.
- `modules/queue`: consumido pelo root module existente; sem alterar seu contrato nesta mudança.
- AWS SQS na conta e região aprovadas, limitado à fila principal e DLQ; estimativa baseada em filas vazias sem tráfego de aplicação.
