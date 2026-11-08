## MODIFIED Requirements

### Requirement: Instância RDS permanece privada
A instância SHALL usar um DB subnet group com subnets da VPC default em pelo menos duas Availability Zones, `publicly_accessible=false` e um security group dedicado que aceite somente ingress PostgreSQL originado do security group da Lambda LAB02.

#### Scenario: VPC e subnets não atendem ao requisito
- **WHEN** a VPC default não existe ou as subnets descobertas não cobrem ao menos duas Availability Zones
- **THEN** o plano falha antes de criar ou alterar recursos

#### Scenario: Nenhuma exposição pública ou ingress amplo
- **WHEN** o plano do módulo database é revisado
- **THEN** a instância não é publicamente acessível e o security group não permite ingress por CIDR, outros grupos, ou portas diferentes de PostgreSQL

#### Scenario: PostgreSQL acessível somente pela Lambda LAB02
- **WHEN** o security group da Lambda é fornecido ao módulo database
- **THEN** o SG do RDS permite TCP/5432 somente com esse SG como origem

### Requirement: Integração de aplicação fica para outra mudança
Esta capacidade SHALL provisionar somente a fundação do banco e da rede necessária ao RDS, sem schema financeiro, dados, usuário de aplicação ou tráfego SQS.

#### Scenario: Banco sem integração de runtime
- **WHEN** o plano é revisado
- **THEN** não há tabelas, schema, role de aplicação, event source mapping ou mensagens de teste, embora a Lambda possa ter configuração VPC e acesso de rede restrito ao PostgreSQL
