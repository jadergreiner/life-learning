## Why

O módulo `modules/queue` do LAB02 está vazio, embora SQS Standard seja a origem do fluxo de eventos descrito no contrato do laboratório. Implementá-lo agora cria a infraestrutura reproduzível da fila e da DLQ, mantendo os parâmetros operacionais explícitos para posterior integração com Lambda e validação do desenho pedagógico.

## What Changes

- Implementar módulo Terraform para fila principal SQS Standard e sua dead-letter queue (DLQ), incluindo política de redrive.
- Expor nomes e ARNs necessários para integração posterior, sem configurar consumidor Lambda, banco ou permissões IAM nesta mudança.
- Documentar parâmetros, comportamento, uso local e teardown do módulo.
- Manter execução em modo de planejamento somente; não provisionar recursos AWS.

## Capabilities

### New Capabilities
- `sqs-lab02`: contrato do módulo Terraform para fila Standard, DLQ e redrive no LAB02.

### Modified Capabilities
- Nenhuma.

## Impact

- `labs/lab02/terraform/modules/queue`: README e configuração Terraform do módulo.
- Dependência do AWS Terraform Provider já usada pelo projeto; parâmetros de retenção, visibilidade e tentativas serão configuráveis, sem presumir dimensionamento final.
- Nenhuma alteração na cadência pedagógica, nos critérios AWS-01–AWS-07 ou em `labs/lab002-terraform`; sem chamadas de criação/alteração na AWS.
