# Módulo database do LAB02

Este módulo cria a fundação privada de PostgreSQL em Amazon RDS e permite ingress TCP/5432 somente do security group da Lambda LAB02 fornecido como entrada. Não cria schema, tabelas, usuário de aplicação ou dados.

## Defaults

| Parâmetro | Default |
| --- | --- |
| Identificador | `lab02-postgres` |
| Database inicial | `lab02` |
| Master username | `lab02_admin` |
| Engine | PostgreSQL `16.15` |
| Classe | `db.t4g.micro` |
| AZ | Single-AZ |
| Armazenamento | 20 GiB gp3, criptografado |
| Backup automático | 1 dia |
| Deletion protection | habilitada |
| Acesso público | desabilitado |

Todos os parâmetros configuráveis ficam em `variables.tf`. A disponibilidade da combinação de classe/versão deve ser confirmada na região antes de aplicar.

## Rede e credenciais

O módulo descobre a VPC default e suas subnets por data sources; não fixa IDs. A criação do DB subnet group falha se as subnets não cobrem pelo menos duas Availability Zones. O SG do banco aceita somente TCP/5432 do SG da Lambda LAB02. A Lambda precisa estar na mesma AZ do RDS e seu SG egress limita-se a esse destino/porta.

`manage_master_user_password` deixa o RDS gerar e gerir a credencial em AWS Secrets Manager. O módulo expõe somente o ARN do secret, nunca sua senha. A chave padrão do Secrets Manager e a credencial gerenciada podem gerar custos adicionais. Acesso posterior exigirá uma mudança separada de rede e uma role de aplicação de privilégio mínimo.

## Outputs

O módulo publica identificador, ARN e resource ID do RDS, endpoint privado, porta, nome do database, ARN do secret, nome do subnet group, ID do security group e AZ da instância. O ARN do secret não fornece credenciais à Lambda.

## Ciclo de vida

Deletion protection e snapshot final são intencionais. Para teardown, altere explicitamente `deletion_protection` para `false`, escolha um `final_snapshot_identifier` ainda não utilizado, revise o plano e só então destrua pelo mesmo root/state. O snapshot permanece e pode continuar gerando custo; sua retenção ou exclusão é decisão separada. Reutilize um nome novo para cada ciclo de teardown.
