# Lab 002 — Terraform e Amazon S3

Laboratório individual e temporário para criar um bucket S3 vazio, verificar
seus controles com AWS CLI e removê-lo com Terraform. Execute todos os comandos
no PowerShell, a partir da raiz do repositório, salvo indicação em contrário.

## Pré-requisitos

- Terraform CLI 1.9.0 ou superior e AWS CLI v2 instalados.
- Credenciais AWS já configuradas para uma identidade IAM nomeada e de
  privilégio mínimo. Não use credenciais root.
- A identidade deve poder consultar a própria conta/região, criar, configurar,
  consultar e excluir o bucket deste exercício. Para validar que está vazio,
  precisa de `s3:ListBucket` limitado ao bucket. Não é necessário
  `s3:ListAllMyBuckets`; este laboratório não cria IAM.
- Use a região `us-east-1`, conforme os critérios de aceitação do SDD.

Confirme a identidade e a região antes de começar. O ARN retornado deve
identificar a identidade IAM esperada e não um usuário root:

```powershell
aws sts get-caller-identity
aws configure get region
```

Se a região padrão estiver diferente, configure o perfil já autorizado ou
ajuste a região do perfil antes de continuar. Terraform usa `us-east-1` por
padrão.

## Configuração e revisão

```powershell
Set-Location labs/lab002-terraform
terraform init
terraform fmt -check
terraform validate
terraform plan -var="bucket_prefix=seu-prefixo-curto"
```

Escolha um prefixo próprio, em minúsculas, com letras, números e hífens, sem
hífen no início ou no fim. Terraform deriva o nome com o prefixo, o ID da conta,
a região e o sufixo `-an`, e usa o namespace S3 `account-regional`. O prefixo
deve deixar o nome resultante dentro do limite de 63 caracteres. Se o plano
indicar uma colisão ou qualquer recurso fora deste laboratório, pare, ajuste o
prefixo se necessário e revise novamente.

O plano deve conter somente um bucket S3 e seus controles de acesso público,
ownership, criptografia e política HTTPS. Nenhum recurso é criado por `init`,
`validate` ou `plan`.

## Aprovar e criar

Revise o plano antes de aplicar. O comando seguinte cria recursos reais na conta
AWS configurada:

```powershell
terraform apply -var="bucket_prefix=seu-prefixo-curto"
```

Confirme a operação no prompt do Terraform. Se o comando falhar, pare e leia a
mensagem; não declare sucesso. Preserve o state local até terminar o `destroy`.

## Validar com AWS CLI

Use o nome exibido pelo output do Terraform:

```powershell
$bucket = terraform output -raw bucket_name
$region = "us-east-1"
aws s3api head-bucket --bucket $bucket --region $region
aws s3api get-public-access-block --bucket $bucket --region $region
aws s3api get-bucket-ownership-controls --bucket $bucket --region $region
aws s3api get-bucket-encryption --bucket $bucket --region $region
aws s3api get-bucket-policy-status --bucket $bucket --region $region
aws s3api get-bucket-policy --bucket $bucket --region $region
```

Resultados esperados: `head-bucket` termina com sucesso; as quatro opções de
Block Public Access são `true`; ownership é `BucketOwnerEnforced`; a regra de
criptografia usa `AES256`; `IsPublic` é `false`; e a política contém `Deny` para
`aws:SecureTransport=false` nos recursos do bucket e dos objetos. Uma resposta
403 é falha de permissão, não uma validação bem-sucedida. Não é necessário
enviar requisições HTTP para testar a política.

Confirme que o bucket está vazio antes da remoção:

```powershell
aws s3api list-objects-v2 --bucket $bucket --region $region
```

Não envie dados a este bucket. Se houver objetos, remova-os antes do `destroy`.

## Limpar

```powershell
terraform destroy -var="bucket_prefix=seu-prefixo-curto"
terraform state list
```

Confirme o `destroy` no prompt. O bucket precisa estar vazio; se a remoção
falhar por conteúdo, remova os objetos e repita. O state deve permanecer local
até o comando terminar. `terraform state list` sem recursos confirma que o
state deste exercício está vazio; isso, sozinho, não substitui a confirmação
da remoção na AWS.

## Arquivos locais

O state, diretório `.terraform/`, variáveis locais e planos salvos são ignorados
pelo Git. O arquivo `.terraform.lock.hcl` deve ser mantido versionado para
registrar a seleção do AWS Provider. Não compartilhe nem publique o state.
