## Context

O RDS PostgreSQL privado e a Lambda preparatória já existem em uma VPC default. A função ainda retorna apenas `ready`; portanto, o objetivo imediato é preparar a rede sem iniciar consumo SQS nem conceder credenciais. O banco é Single-AZ e usa um security group dedicado.

## Goals / Non-Goals

**Goals:** habilitar caminho privado da Lambda ao PostgreSQL, com subnet na AZ do RDS e regras SG restritas; documentar IAM necessário para Terraform e para a execution role.

**Non-Goals:** implementar handler de negócio, trigger/event source mapping, credenciais ou usuário de aplicação, schema, NAT Gateway, VPC endpoint, alta disponibilidade ou iniciar a sessão didática U2.1.

## Decisions

- Exportar do módulo database a AZ atual da instância e seu SG. No root, descobrir subnet default pelo VPC ID e AZ exportada, evitando IDs fixos. Falhar se não houver subnet nessa AZ.
- Criar SG dedicado da Lambda no root, sem ingress e com egress TCP/5432 somente para o SG do banco. No módulo database, aceitar o SG da Lambda e criar uma regra ingress PostgreSQL cuja origem seja apenas esse SG.
- Passar subnet e SG ao módulo processor e configurar `vpc_config`. Associar `AWSLambdaVPCAccessExecutionRole` à role de execução, além da política de logs, para gerenciamento de ENIs.
- Atualizar políticas locais do deployer com as ações específicas para regras SG, descoberta de subnets, VPC config Lambda e attachment da política gerenciada VPC. Nenhuma permissão de aplicação é adicionada.
- Não adicionar NAT nem endpoints: Lambda e RDS permanecem na mesma VPC/AZ, e a função não precisa de acesso de saída a serviços AWS neste estágio.

## Risks / Trade-offs

- [A função `ready` não processa eventos] → manter event source mapping ausente; a conectividade de rede não autoriza tráfego de aplicação.
- [A instância é Single-AZ] → selecionar subnet somente na AZ atual; mudança futura da AZ requer novo plan e revisão.
- [Permissões do principal de deploy podem divergir dos JSON locais] → revisar plan e parar diante de AccessDenied; os JSON documentam a política a conceder por administrador.
- [Tráfego de rede pode ter custo variável] → não criar recursos com tarifa horária; avaliar custo antes de evoluir para endpoints ou tráfego de dados.

## Migration Plan

1. Atualizar módulos e documentos IAM locais.
2. Gerar e revisar Terraform plan, confirmando somente alteração de configuração Lambda e regras SG restritas, sem substituição do RDS.
3. Aplicar apenas se o plano respeitar o escopo; rollback removendo VPC config/regra SG em mudança Terraform posterior.

## Open Questions

Nenhuma para esta etapa de conectividade. A autenticação e o processamento permanecem pendentes da defesa I0 e de uma mudança futura.
