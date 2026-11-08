## ADDED Requirements

### Requirement: Ambiente LAB02 compõe somente a fila SQS aprovada
O root module `labs/lab02/terraform/environments/lab` SHALL configurar o provider AWS, instanciar somente o módulo de fila do LAB02 e expor as saídas necessárias para verificar a fila principal e a DLQ.

#### Scenario: Plano contém somente recursos de fila
- **WHEN** o root module é inicializado e planejado com os parâmetros aprovados
- **THEN** o plano inclui apenas a fila principal Standard, a DLQ Standard, criptografia SSE-SQS e suas políticas redrive/redrive-allow, sem Lambda, RDS, IAM, rede ou outros serviços

#### Scenario: Identidade AWS não corresponde
- **WHEN** o account ID obtido por STS difere do account ID aprovado no arquivo de variáveis local
- **THEN** Terraform encerra o plano antes de permitir que o módulo de filas seja aplicado

#### Scenario: State e variáveis locais
- **WHEN** a configuração local é usada
- **THEN** state, backups, plano e valores de `terraform.tfvars` permanecem ignorados pelo Git, enquanto o lockfile do provider pode ser versionado

#### Scenario: Uso e custo aprovados
- **WHEN** o módulo é aplicado sob o escopo desta mudança
- **THEN** as duas filas permanecem vazias e sem tráfego da aplicação, e nenhum serviço adicional ou chave KMS é criado

#### Scenario: Teardown
- **WHEN** o usuário encerra o laboratório e executa destroy no mesmo root/state
- **THEN** a fila principal, DLQ e políticas associadas são removidas e o state confirma ausência de recursos gerenciados
