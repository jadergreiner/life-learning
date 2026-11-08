# lab02-database-foundation Specification

## Purpose
Define o provisionamento privado e reproduzível de PostgreSQL em RDS como fundação de persistência futura do LAB02, sem criar schema ou integração de aplicação.

## Requirements
### Requirement: Módulo database provisiona PostgreSQL no RDS
O módulo Terraform `labs/lab02/terraform/modules/database` SHALL provisionar uma instância Amazon RDS for PostgreSQL para persistência futura do LAB02, usando como baseline a classe `db.t4g.micro`, versão PostgreSQL `16.15`, Single-AZ e armazenamento gp3 de 20 GiB; esses valores devem permanecer configuráveis.

#### Scenario: Configuração baseline
- **WHEN** o root module planeja o módulo database com seus valores padrão
- **THEN** o plano contém uma instância RDS for PostgreSQL Single-AZ com os parâmetros baseline e sem read replica ou recursos de alta disponibilidade avançada

#### Scenario: Disponibilidade regional
- **WHEN** a classe ou versão configurada não está disponível em `us-east-1`
- **THEN** o plano falha claramente antes do apply, sem substituir silenciosamente a classe ou versão solicitada

### Requirement: Instância RDS permanece privada
A instância SHALL usar um DB subnet group com subnets da VPC default em pelo menos duas Availability Zones, `publicly_accessible=false` e um security group dedicado sem regra de entrada nesta mudança.

#### Scenario: VPC e subnets não atendem ao requisito
- **WHEN** a VPC default não existe ou as subnets descobertas não cobrem ao menos duas Availability Zones
- **THEN** o plano falha antes de criar ou alterar recursos

#### Scenario: Nenhuma exposição pública ou ingress
- **WHEN** o plano do módulo database é revisado
- **THEN** a instância não é publicamente acessível e o security group não permite entrada PostgreSQL ou outro tráfego

### Requirement: Dados e credencial master são protegidos
A instância SHALL criptografar o armazenamento, manter backup automático por 1 dia como default, habilitar deletion protection e deixar o RDS gerar/gerenciar a senha master em AWS Secrets Manager.

#### Scenario: Plano contém controles de proteção
- **WHEN** o plano é criado com os valores padrão
- **THEN** armazenamento criptografado, backup automático, deletion protection e gestão de senha master pelo RDS estão habilitados

#### Scenario: Segredo não é exposto
- **WHEN** outputs, logs, arquivos Terraform versionáveis e documentação são inspecionados
- **THEN** nenhum valor de senha é emitido ou armazenado em texto claro, e apenas o ARN do secret pode ser exposto

#### Scenario: Destruição deliberada
- **WHEN** o operador executa o procedimento de teardown autorizado
- **THEN** deletion protection deve ser removida por mudança explícita e o banco deve gerar um snapshot final com identificador único antes da exclusão

### Requirement: Módulo expõe metadados sem credenciais
O módulo SHALL expor endpoint, porta, nome da instância, nome do banco, ARN do secret master e ARN/ID dos recursos necessários à integração futura, sem expor o valor do secret.

#### Scenario: Inspeção do resultado
- **WHEN** a instância é provisionada
- **THEN** outputs permitem localizar o endpoint e o secret ARN sem retornar senha

### Requirement: Integração de aplicação fica para outra mudança
Esta capacidade SHALL provisionar somente a fundação do banco e da rede necessária ao RDS, sem schema financeiro, dados, usuário de aplicação, conexão Lambda ou tráfego SQS.

#### Scenario: Banco sem integração de runtime
- **WHEN** o plano é revisado
- **THEN** não há tabelas, schema, role de aplicação, ingress da Lambda, VPC configuration da Lambda, event source mapping ou mensagens de teste

### Requirement: Apply depende de custo e autorização
O provisionamento SHALL exigir revisão do plano, estimativa mensal para RDS/armazenamento/backups/snapshot/Secrets Manager e autorização operacional explícita antes de qualquer apply.

#### Scenario: Plano sem autorização operacional
- **WHEN** os artefatos, custo ou plano ainda não foram aprovados operacionalmente
- **THEN** nenhum recurso RDS ou Secrets Manager é aplicado
