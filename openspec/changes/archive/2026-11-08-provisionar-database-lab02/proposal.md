## Why

O LAB02 já possui SQS e uma Lambda preparatória, mas ainda não dispõe do PostgreSQL que deverá persistir contas, eventos e transações do laboratório. Provisionar a base gerenciada cria essa fundação sem antecipar o schema financeiro nem a integração da Lambda.

## What Changes

- Implementar o módulo Terraform reservado `modules/database` para uma instância Amazon RDS for PostgreSQL de laboratório.
- Compor a instância no root `environments/lab`, preservando a conta/região aprovadas e o state existente de SQS e Lambda.
- Manter a instância sem acesso público, com armazenamento criptografado, backups automatizados e credencial master gerenciada pelo RDS em Secrets Manager.
- Expor endpoint, porta, nome do banco e ARN do secret sem expor valores de credencial.
- Documentar custo recorrente, conectividade ainda não habilitada e procedimento deliberado de snapshot/teardown.
- Não criar schema, usuário de aplicação, tabelas, dados, acesso de rede da Lambda, event source mapping ou processamento financeiro nesta mudança.

## Capabilities

### New Capabilities

- `lab02-database-foundation`: provisionamento privado e reproduzível de PostgreSQL em RDS para persistência futura do LAB02.

### Modified Capabilities

- `sqs-lab02-environment`: expandir o root Terraform existente para incluir o banco e seus outputs, mantendo os recursos SQS e Lambda já aprovados.

## Impact

- `labs/lab02/terraform/modules/database/` passa de README reservado para módulo Terraform executável.
- `labs/lab02/terraform/environments/lab/` passa a compor RDS no mesmo state local das filas e da Lambda.
- O usuário IAM `lab02-terraform` precisará de permissões RDS e Secrets Manager delimitadas para os recursos nomeados, sem alterar as permissões de workload da Lambda.
- A instância RDS gera custo enquanto provisionada; a estimativa regional e o teto mensal devem ser revistos antes de qualquer apply.
- O LAB02 permanece sem sessão pedagógica iniciada; esta mudança trata somente da infraestrutura do banco.
