## Context

O LAB02 já possui fila/DLQ SQS e a função preparatória `lab02-processor` no root Terraform `labs/lab02/terraform/environments/lab`, conta `325422573352`, região `us-east-1`, state local. O diretório `modules/database` ainda é somente documentação. O contrato ED-05 escolhe PostgreSQL em RDS para persistir contas, eventos e transações, mas não fixa schema nem conectividade.

Uma consulta somente leitura à conta encontrou uma VPC default e subnets default em seis Availability Zones na região. A implementação deve redescobrir esses recursos pelo provider e falhar claramente se a VPC ou a cobertura de subnets não existir; não deve gravar IDs atuais no código.

## Goals / Non-Goals

**Goals:**

- Provisionar uma instância Amazon RDS for PostgreSQL pequena para o laboratório e compor seus recursos no root/state atual.
- Manter o endpoint sem acesso público, sem ingress de rede nesta etapa, com armazenamento criptografado e backup automatizado.
- Fazer o RDS gerar e gerir a senha master no AWS Secrets Manager; expor somente o ARN do secret.
- Preservar SQS e Lambda, estimar o custo recorrente e documentar proteção, snapshot e teardown.

**Non-Goals:**

- Configurar VPC própria, NAT Gateway, VPC endpoints, conexão de rede da Lambda ou regra de ingress PostgreSQL.
- Criar schema, tabelas, dados de exemplo, role de aplicação ou migrations.
- Implementar consultas, processamento financeiro, SQS event source mapping, monitoramento avançado ou failover Multi-AZ.
- Aplicar recursos AWS durante a criação da proposta; o apply continua condicionado à revisão de plano/custo e autorização operacional específica.

## Decisions

1. **RDS for PostgreSQL, não Aurora.** ED-05 define PostgreSQL relacional e depende de transações/constraints do próprio PostgreSQL. Usar a instância RDS padrão reduz escopo e preserva portabilidade. Começar com classe `db.t4g.micro`, PostgreSQL `16.15`, Single-AZ e 20 GiB gp3; confirmar classe/versão, cotas e preço no plano antes de aplicar. A combinação estava orderable em `us-east-1` quando esta proposta foi escrita.

2. **Usar VPC default existente, com descoberta dinâmica.** Criar um DB subnet group usando subnets da VPC default distribuídas por pelo menos duas AZs, conforme o requisito do RDS. Isso evita introduzir NAT e uma segunda topologia antes da integração. `publicly_accessible=false` e um security group dedicado sem regras ingress mantêm o banco fechado; aceitar conexão de Lambda em 5432 fica para uma mudança que também associe a Lambda à VPC. A AWS requer subnets em pelo menos duas AZs para o subnet group e recomenda manter o banco privado ([criação de DB instance](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_CreateDBInstance.html), [subnet group em VPC](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.WorkingWithRDSInstanceinaVPC.html)).

3. **Credencial master gerenciada pelo RDS.** Configurar `manage_master_user_password=true` e usar a chave gerenciada padrão do Secrets Manager. Não colocar senha em tfvars, outputs ou código. O módulo expõe o ARN do secret, sem seu valor. O custo de Secrets Manager deve entrar na estimativa; integração posterior da Lambda precisará de permissão de leitura restrita ao secret ([RDS e Secrets Manager](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-secrets-manager.html)).

4. **Persistência protegida e recuperação explícita.** Habilitar criptografia, backup automático por 1 dia e deletion protection. Destruição requer desabilitar proteção em uma etapa explícita, obter snapshot final com identificador único e confirmar se o snapshot deve ser mantido ou removido. Como o root/state também contém filas e Lambda, documentar que `terraform destroy` afeta todos os recursos desse ambiente.

5. **Permissões do deployer separadas das permissões da aplicação.** Preservar `Lab02TerraformSQS` e `Lab02TerraformLambda`; acrescentar uma policy de provisionamento RDS com ações e ARNs mínimos derivados do plano. Incluir apenas as leituras de descoberta necessárias e as permissões exigidas pela integração de master password gerenciada. A execution role da Lambda não recebe acesso RDS, Secrets Manager ou VPC nesta mudança.

6. **Custo e autorização antes de apply.** A instância gera cobrança enquanto provisionada, além de armazenamento, backups/snapshot final e secret. Registrar estimativa mensal para `us-east-1`, revisar teto, conta e plano sem alterações em SQS/Lambda e só aplicar após autorização operacional explícita. Referências de preço: [RDS PostgreSQL](https://aws.amazon.com/rds/postgresql/pricing/) e [Secrets Manager](https://aws.amazon.com/secrets-manager/pricing/).

## Risks / Trade-offs

- [A VPC default pode ser removida ou não cobrir duas AZs] → descobrir VPC/subnets dinamicamente e falhar antes do apply quando a pré-condição não for atendida.
- [O endpoint privado não será conectável pela Lambda ainda] → declarar essa limitação e adiar ingress, VPC config e credencial de aplicação para uma mudança de integração.
- [RDS mantém custo enquanto ativo, mesmo sem tráfego] → estimar custo antes do apply, habilitar proteção contra exclusão acidental e documentar parada/teardown e custo do snapshot.
- [O root Terraform reúne recursos com ciclos de vida distintos] → manter o state reconciliável e exigir revisão do plano; nunca apagar state para remover apenas o banco.
- [A senha master não é apropriada para consultas da aplicação] → não criar usuário de aplicação nesta mudança; a futura integração deve provisionar uma role PostgreSQL de privilégio mínimo.
- [Classe ou versão pode deixar de estar disponível] → confirmar disponibilidade regional e ajustar a estimativa na fase de plan.

## Migration Plan

1. Implementar o módulo RDS e as variáveis/outputs, além da composição no root sem alterar SQS/Lambda.
2. Descobrir a VPC default e verificar pelo menos duas AZs; validar policy IAM do deployer e `terraform fmt/init/validate`.
3. Gerar e revisar plano com `lab02-terraform`; confirmar somente recursos RDS, subnet group/security group e outputs novos.
4. Atualizar estimativa mensal e teto para RDS, armazenamento, backups/snapshot e Secrets Manager. Aplicar somente depois de autorização operacional explícita.
5. Verificar configuração, status `available`, ausência de acesso público/ingress, encryption, backup, secret ARN e state. Não testar conexão nem criar schema nesta mudança.
6. Para rollback/teardown, desabilitar deletion protection em plano revisado, criar snapshot final nomeado, destruir pelo mesmo root/state e decidir explicitamente a retenção/exclusão do snapshot.

## Open Questions

- Nenhuma decisão bloqueia a proposta. `db.t4g.micro`, PostgreSQL 16.15, 20 GiB gp3 e backup de 1 dia são baseline de laboratório, sujeitos a disponibilidade e estimativa atualizadas antes do apply.
