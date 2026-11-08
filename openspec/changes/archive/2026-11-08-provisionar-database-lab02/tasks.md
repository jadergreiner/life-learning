## 1. Implementar o módulo PostgreSQL em RDS

- [x] 1.1 Definir inputs e validações do módulo database para identificador, database name, PostgreSQL version/class, storage, backup retention e deletion protection; usar os defaults descritos na spec.
- [x] 1.2 Descobrir a VPC default e suas subnets dinamicamente; validar cobertura mínima em duas Availability Zones sem fixar IDs no código.
- [x] 1.3 Criar DB subnet group e security group dedicado sem regras ingress.
- [x] 1.4 Criar a instância RDS PostgreSQL Single-AZ com gp3 criptografado, backup de 1 dia, deletion protection, acesso não público e senha master gerenciada pelo RDS em Secrets Manager.
- [x] 1.5 Expor endpoint, porta, database name, ARN do secret e metadados sem retornar credencial.
- [x] 1.6 Documentar escopo, parâmetros, limitações de conectividade e ciclo de vida em `modules/database/README.md`.

## 2. Integrar ao ambiente LAB02

- [x] 2.1 Instanciar o módulo database no root `environments/lab` mantendo a validação de conta e os recursos atuais de SQS e Lambda.
- [x] 2.2 Adicionar outputs do banco sem expor a senha.
- [x] 2.3 Criar e validar policy IAM de provisionamento RDS/Secrets Manager com ações e recursos mínimos, preservando `Lab02TerraformSQS` e `Lab02TerraformLambda`.
- [x] 2.4 Atualizar o README do ambiente com pré-requisitos, privacidade, credenciais, custo recorrente e procedimento explícito para snapshot/teardown.

## 3. Validar o plano, custo e provisionamento

- [x] 3.1 Executar `terraform fmt -check`, `terraform init` e `terraform validate`; validar o módulo e os documentos IAM.
- [x] 3.2 Confirmar identidade `lab02-terraform`, conta `325422573352`, região `us-east-1`, VPC default e cobertura de subnets em pelo menos duas AZs.
- [x] 3.3 Gerar e revisar o plano; exigir somente recursos RDS/subnet group/security group/outputs novos, sem alterações ou destruições em SQS/Lambda.
- [x] 3.4 Registrar estimativa mensal atualizada para instância, gp3, backups/snapshot e Secrets Manager, confrontar com o pedido de menor custo possível e aplicar somente após autorização operacional explícita.
- [x] 3.5 Após apply autorizado, verificar status, classe/engine/storage, encryption, backup, deletion protection, endpoint privado, ausência de ingress, secret ARN, outputs e state.
- [x] 3.6 Documentar o procedimento seguro para desligar proteção, criar snapshot final e encerrar os recursos no mesmo state sem apagar evidência de custos ou credenciais.

