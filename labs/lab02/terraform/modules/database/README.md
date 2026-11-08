# Módulo database do LAB02

Este módulo cria somente a fundação privada de PostgreSQL em Amazon RDS. Não cria schema, tabelas, usuário de aplicação, dados, conectividade de Lambda ou regras de entrada.

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

O módulo descobre a VPC default e suas subnets por data sources; não fixa IDs. A criação do DB subnet group falha se as subnets não cobrem pelo menos duas Availability Zones. O security group dedicado não declara ingress e preserva a regra egress padrão da AWS (`0.0.0.0/0`). A Lambda do LAB02 não está associada à VPC e não consegue conectar-se ao endpoint nesta etapa.

`manage_master_user_password` deixa o RDS gerar e gerir a credencial em AWS Secrets Manager. O módulo expõe somente o ARN do secret, nunca sua senha. A chave padrão do Secrets Manager e a credencial gerenciada podem gerar custos adicionais. Acesso posterior exigirá uma mudança separada de rede e uma role de aplicação de privilégio mínimo.

## Outputs

O módulo publica identificador, ARN e resource ID do RDS, endpoint privado, porta, nome do database, ARN do secret, nome do subnet group e ID do security group. O endpoint não implica conectividade autorizada.

## Ciclo de vida

Deletion protection e snapshot final são intencionais. Para teardown, altere explicitamente `deletion_protection` para `false`, escolha um `final_snapshot_identifier` ainda não utilizado, revise o plano e só então destrua pelo mesmo root/state. O snapshot permanece e pode continuar gerando custo; sua retenção ou exclusão é decisão separada. Reutilize um nome novo para cada ciclo de teardown.
