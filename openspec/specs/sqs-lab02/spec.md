# sqs-lab02 Specification

## Purpose
Define o módulo Terraform reutilizável que compõe a fila SQS Standard do LAB02, sua DLQ e os contratos operacionais necessários para integração futura.
## Requirements
### Requirement: Módulo SQS Standard com DLQ
O módulo Terraform de fila do LAB02 SHALL criar uma fila principal SQS Standard e uma DLQ SQS Standard associada por redrive policy, com parâmetros operacionais explícitos e outputs suficientes para integração posterior.

#### Scenario: Fila e DLQ configuradas
- **WHEN** um root module válido instancia o módulo com entradas obrigatórias
- **THEN** o plano contém uma fila principal Standard, uma DLQ Standard, uma política de redrive da principal para a DLQ e uma política de redrive allow limitada à fila principal

#### Scenario: Limite de recebimentos atingido
- **WHEN** uma mensagem da fila principal alcança o limite configurado de recebimentos sem sucesso
- **THEN** a política de redrive direciona a mensagem à DLQ associada

#### Scenario: Entradas fora dos limites
- **WHEN** retention, visibility timeout, long polling ou maxReceiveCount recebe valor inválido
- **THEN** a validação Terraform rejeita a configuração antes de qualquer provisionamento

#### Scenario: Integração futura
- **WHEN** outro módulo precisa configurar um consumidor ou permissões de menor privilégio
- **THEN** o módulo expõe URL, ARN e nome da fila principal e da DLQ

#### Scenario: Sem promessa de processamento exactly-once
- **WHEN** uma mensagem é entregue ou processada mais de uma vez
- **THEN** a documentação declara que SQS Standard permite duplicatas e que idempotência do efeito financeiro não é fornecida pelo módulo de fila

#### Scenario: Sem provisionamento nesta mudança
- **WHEN** os artefatos desta mudança são concluídos
- **THEN** nenhum `terraform apply` ou recurso AWS é executado/criado

