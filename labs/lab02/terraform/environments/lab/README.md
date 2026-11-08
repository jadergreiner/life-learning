# Infraestrutura do LAB02

Este root Terraform gerencia no mesmo state local a fila principal e DLQ SQS, a função preparatória `lab02-processor` e uma instância PostgreSQL em Amazon RDS. A Lambda continua sem trigger/event source mapping, VPC, acesso ao RDS, secrets ou permissões SQS. O handler somente retorna `{"status":"ready"}`.

## Alvo e identidade

O alvo é a conta `325422573352`, região `us-east-1`. Use o perfil AWS CLI `lab02-terraform` para Terraform; não use `certificacao` para Terraform. A validação STS encerra o plano quando a conta não corresponde. O usuário `lab02-terraform` preserva as policies inline `Lab02TerraformSQS` e `Lab02TerraformLambda`. A policy managed adicional `Lab02TerraformRDS` está documentada em `iam-policy-lab02-terraform-rds.json`; ela limita alterações aos recursos nomeados do LAB02 e limita a descoberta de security groups e VPC. A policy foi validada com IAM Access Analyzer.

Terraform `>= 1.9.0` e AWS CLI devem estar disponíveis. O arquivo local `terraform.tfvars` define perfil, conta, região e parâmetros; não salve credenciais AWS nele. State, backups, planos e tfvars são ignorados pelo Git. Preserve state e seus backups para reconciliar ou remover os recursos pelo mesmo root.

## Recursos RDS

| Configuração | Valor padrão |
| --- | --- |
| Engine / versão | PostgreSQL `16.15` |
| Classe / disponibilidade | `db.t4g.micro`, Single-AZ |
| Armazenamento | 20 GiB gp3 criptografado |
| Backup automático | 1 dia |
| Deletion protection | habilitada |
| Acesso público | desabilitado |
| Ingress do security group | nenhum; egress padrão AWS para `0.0.0.0/0` |
| Master password | gerenciada pelo RDS no Secrets Manager |

O módulo descobre a VPC default e todas as subnets dinamicamente e exige cobertura em pelo menos duas AZs para o DB subnet group. Não cria VPC, NAT Gateway nem conectividade da aplicação. O security group não aceita tráfego de entrada; mantém egress IPv4 padrão da AWS. O endpoint é privado e ainda não pode ser alcançado pela Lambda. Outputs contêm endpoint, porta, database name e ARN do secret, nunca o valor da credencial. A credencial master não deve ser usada pela aplicação.

## Estimativa de custo recorrente

Estimativa de referência para `us-east-1`, 730 horas/mês, instância sempre ativa, 20 GiB e um secret:

| Item | Premissa | Estimativa mensal |
| --- | --- | ---: |
| RDS `db.t4g.micro` PostgreSQL Single-AZ | US$ 0,016/h × 730 h | US$ 11,68 |
| RDS gp3 | US$ 0,115/GiB-mês × 20 GiB | US$ 2,30 |
| Secrets Manager | 1 secret × US$ 0,40/mês | US$ 0,40 |
| Chamadas Secrets Manager | nenhuma ou poucas chamadas; US$ 0,05 por 10 mil | ~US$ 0,00 |
| **Subtotal de referência** | sem excedentes e sem impostos | **~US$ 14,38/mês** |

Os preços consultados na Price List API da AWS para `us-east-1` são US$ 0,016/h para `db.t4g.micro` PostgreSQL Single-AZ e US$ 0,115/GiB-mês para GP3 ([catálogo oficial de preços RDS da região](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonRDS/current/us-east-1/index.json)). A tarifa publicada do Secrets Manager é US$ 0,40 por secret/mês e US$ 0,05 por 10 mil chamadas ([preços oficiais Secrets Manager](https://aws.amazon.com/secrets-manager/pricing/)). Esta conta não inclui excedentes de armazenamento de backups/snapshot, créditos CPU T4g além da baseline, transferência de dados, outros serviços, impostos nem ajustes por Free Tier/créditos da conta. Backups automáticos dentro da franquia RDS podem não gerar custo adicional; snapshot final retido pode gerar cobrança se ultrapassar a franquia agregada. Verifique o valor atualizado no [AWS Pricing Calculator para RDS](https://calculator.aws/#/createCalculator/RDS) antes de aplicar. A estimativa não substitui a revisão do teto mensal aprovado pelo operador.

## Plan e apply

Execute nesta pasta (`labs/lab02/terraform/environments/lab`):

```powershell
aws sts get-caller-identity --profile lab02-terraform
terraform fmt -check -recursive
terraform init
terraform validate
terraform plan -out=lab02.tfplan
terraform show -no-color lab02.tfplan
```

Confirme conta, região, VPC/subnets e que o plano só adiciona recursos do banco, sem alterações ou destruições em SQS/Lambda. Revise a estimativa e o teto mensal. **Não execute apply até a revisão do plano e do custo e uma autorização operacional explícita para este banco.** Não use `-auto-approve`. Após autorização específica:

```powershell
terraform apply lab02.tfplan
terraform output
terraform state list
```

Verifique em AWS que a instância está `available`, privada, criptografada, Single-AZ, com backup e deletion protection; confirme que o security group não tem ingress e que o ARN do secret corresponde ao segredo gerenciado pelo RDS. Não revele nem copie a senha para outputs, logs ou arquivos versionados. Não envie mensagens SQS, invoque a Lambda ou teste conexão nesta mudança.

## Teardown deliberado

`terraform destroy` neste root remove também filas SQS, DLQ e Lambda, além do banco. Para manter os demais recursos e encerrar apenas o banco, use uma alteração explícita temporária nos inputs do módulo: desabilite deletion protection e escolha um identificador de snapshot final único; gere e revise o plano para garantir que somente o RDS seja alterado/removido e que o snapshot será criado. Aplique essa mudança somente após autorização operacional. Depois, revise um segundo plano de remoção do RDS e destrua pelo mesmo state. Não apague state para forçar remoção. Confirme o snapshot final e decida explicitamente sua retenção ou exclusão; snapshots retidos podem continuar gerando custo. Preserve evidência de custo e não exporte credenciais.

O identificador padrão de snapshot é datado; atualize para um nome novo em cada teardown/recriação para evitar colisão com snapshot existente.
