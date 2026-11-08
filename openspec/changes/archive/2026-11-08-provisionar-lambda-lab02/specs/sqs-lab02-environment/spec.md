## RENAMED Requirements

- FROM: Ambiente LAB02 compõe somente a fila SQS aprovada
- TO: Ambiente LAB02 compõe a fila SQS e a função Lambda preparatória aprovadas

## MODIFIED Requirements

### Requirement: Ambiente LAB02 compõe a fila SQS e a função Lambda preparatória aprovadas
O root module `labs/lab02/terraform/environments/lab` SHALL configurar o provider AWS, instanciar o módulo de fila SQS e uma única função Lambda preparatória, e expor saídas para verificar esses recursos.

#### Scenario: Plano contém somente os recursos aprovados
- **WHEN** o root module é inicializado e planejado com os parâmetros aprovados
- **THEN** o plano preserva a fila principal Standard, a DLQ Standard, SSE-SQS e políticas redrive/redrive-allow, e adiciona uma função Lambda, sua execution role e log group; não adiciona event source mapping, produtor, RDS, VPC, IAM de aplicação ou outros serviços

#### Scenario: Identidade AWS não corresponde
- **WHEN** o account ID obtido por STS difere do account ID aprovado no arquivo de variáveis local
- **THEN** Terraform encerra o plano antes de permitir alterações em qualquer módulo

#### Scenario: State e variáveis locais
- **WHEN** a configuração local é usada
- **THEN** state, backups, planos, ZIP gerado e valores de `terraform.tfvars` permanecem ignorados pelo Git, enquanto os lockfiles dos providers podem ser versionados

#### Scenario: Filas e função sem invocação automática
- **WHEN** o ambiente é aplicado sob o escopo desta mudança
- **THEN** as filas permanecem vazias e sem tráfego, e a função não consome SQS nem é invocada automaticamente

#### Scenario: Teardown no mesmo root/state
- **WHEN** o usuário encerra o laboratório e executa destroy no mesmo root/state
- **THEN** as filas, políticas associadas, função Lambda, execution role e log group são removidos, e o state confirma ausência de recursos gerenciados
