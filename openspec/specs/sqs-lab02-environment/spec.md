# sqs-lab02-environment Specification

## Purpose
Define o ambiente Terraform do LAB02 que compõe SQS, Lambda preparatória e PostgreSQL em RDS, com validação da conta-alvo, state local e procedimento de teardown.

## Requirements
### Requirement: Ambiente LAB02 compõe SQS, Lambda preparatória e PostgreSQL em RDS aprovados
O root module `labs/lab02/terraform/environments/lab` SHALL configurar o provider AWS, instanciar o módulo de fila SQS, uma função Lambda preparatória e uma instância PostgreSQL em RDS, e expor saídas para verificar os recursos e localizar a credencial gerenciada sem retornar seu valor.

#### Scenario: Plano contém somente os recursos aprovados
- **WHEN** o root module é inicializado e planejado com os parâmetros aprovados
- **THEN** o plano preserva a fila principal Standard, a DLQ Standard, SSE-SQS, políticas redrive/redrive-allow e a Lambda preparatória, e adiciona a instância RDS, DB subnet group e security group sem ingress; não adiciona event source mapping, produtor, schema, ingress de aplicação, NAT Gateway, RDS Multi-AZ, IAM de workload ou serviços não aprovados

#### Scenario: Identidade AWS não corresponde
- **WHEN** o account ID obtido por STS difere do account ID aprovado no arquivo de variáveis local
- **THEN** Terraform encerra o plano antes de permitir alterações em qualquer módulo

#### Scenario: State e variáveis locais
- **WHEN** a configuração local é usada
- **THEN** state, backups, planos e valores de `terraform.tfvars` permanecem ignorados pelo Git, enquanto os lockfiles dos providers podem ser versionados; nenhum valor da senha master é persistido em texto claro em arquivos versionáveis

#### Scenario: Recursos sem tráfego de aplicação
- **WHEN** o ambiente é aplicado sob autorização específica desta mudança
- **THEN** as filas permanecem vazias, a Lambda permanece sem trigger e sem VPC configuration, e o banco permanece sem ingress ou conexão de aplicação

#### Scenario: Outputs e secret
- **WHEN** o ambiente é aplicado e os outputs são consultados
- **THEN** os outputs identificam fila, Lambda e endpoint/porta/database name do RDS e o ARN do secret master, sem revelar a senha

#### Scenario: Teardown no mesmo root/state
- **WHEN** o usuário encerra o laboratório e executa destroy no mesmo root/state após desabilitar deletion protection em plano explícito
- **THEN** os recursos gerenciados de SQS, Lambda e RDS são removidos, o RDS cria o snapshot final nomeado e o state confirma ausência dos recursos gerenciados; retenção ou remoção do snapshot é uma decisão explícita de custo
