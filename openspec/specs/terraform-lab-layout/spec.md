## ADDED Requirements

### Requirement: Layout Terraform preparado e documentado
O repositório SHALL fornecer em `labs/lab02/terraform` uma estrutura versionável, autoexplicativa e sem configuração executável para organizar a futura infraestrutura do LAB02, mantendo o laboratório S3 em `labs/lab002-terraform` separado.

#### Scenario: Estrutura inicial existe
- **WHEN** uma pessoa inspeciona `labs/lab02/terraform`
- **THEN** encontra uma raiz documentada, um diretório `environments/lab` para o futuro root module e diretórios documentados `modules/queue`, `modules/processor` e `modules/database`

#### Scenario: Estrutura não provisiona recursos
- **WHEN** a mudança estrutural é concluída
- **THEN** os novos diretórios não contêm configuração Terraform executável nem alteram ou provisionam recursos AWS

#### Scenario: Laboratórios permanecem separados
- **WHEN** o layout Terraform do LAB02 é adicionado
- **THEN** os arquivos existentes de `labs/lab02` e `labs/lab002-terraform` permanecem preservados e o README declara que são exercícios distintos
