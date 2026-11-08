## Why

A Lambda preparatória e um RDS privado já existem, mas não há caminho de rede entre eles. Esta mudança libera somente conectividade privada e restrita da Lambda ao PostgreSQL, como pré-requisito de uma integração futura que ainda depende da defesa independente I0.

## What Changes

- Associar a Lambda a uma subnet default da mesma Availability Zone do RDS, descoberta dinamicamente.
- Criar um security group da Lambda sem ingress e com egress somente para a porta PostgreSQL do security group do RDS; permitir a origem Lambda no security group do banco.
- Conceder à execution role as permissões de gerenciamento de ENI exigidas pela Lambda e autorizar o deployer a atualizar a configuração VPC e regras de security group de LAB02.
- Manter a Lambda sem event source mapping, acesso ao secret master, código de processamento e usuário/schema de aplicação.
- Provisionar apenas o caminho de rede: sem NAT Gateway, VPC endpoint ou serviço adicional com tarifa horária.

## Capabilities

### New Capabilities
- Nenhuma.

### Modified Capabilities
- `lab02-database-foundation`: permitir ingress PostgreSQL exclusivamente do security group da Lambda do LAB02, mantendo o RDS privado.
- `lab02-lambda-foundation`: associar a função à VPC para conectividade ao RDS, mantendo-a sem trigger e sem credenciais de aplicação.
- `sqs-lab02-environment`: atualizar o cenário de recursos sem tráfego para registrar a configuração de rede Lambda sem ativar processamento.

## Impact

- Alterações em `modules/database`, `modules/processor`, root `environments/lab`, policies JSON de provisionamento e nas três delta specs.
- Mudança de configuração na função Lambda e regra ingress restrita no security group do RDS.
- Nenhum event source mapping, schema, usuário de aplicação, leitura de secret, envio de mensagem ou alteração da cadência U2.1.
- Sem recurso AWS de custo horário novo; custos de tráfego, se houver, seguem as tarifas de transferência da região. O desenho Single-AZ acompanha o RDS existente para evitar cross-AZ nesta etapa.
