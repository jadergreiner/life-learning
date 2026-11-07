# PRD — SDD-0001 lab002-terraform

Status: Aguardando aprovação do usuário
Data: 2026-11-07

## 1. Objetivo e valor

Como aluno da especialização em Engenharia de Dados, demonstrar conhecimento de infraestrutura como código criando um bucket S3 temporário com Terraform, validando sua configuração com AWS CLI e removendo-o ao final.

## 2. Escopo

### Incluído
- Um bucket S3 vazio e temporário na região `us-east-1`.
- Nome do bucket informado como variável e escolhido pelo aluno para ser globalmente único.
- Provisionamento e configuração de segurança por Terraform.
- Validação da existência e das configurações via AWS CLI.
- Remoção dos recursos gerenciados pelo Terraform após a validação.
- Uso de credenciais e permissões AWS já configuradas pelo aluno.

### Fora do escopo
- Conteúdo de `labs\lab02`.
- Armazenar ou processar dados reais.
- Criar IAM, credenciais ou outros serviços AWS além do bucket e suas proteções.
- Uso contínuo, operação de produção ou metas próprias de SLA, latência e concorrência.
- CloudTrail S3 data events, logs de acesso e métricas de requisição adicionais.
- Teste separado de requisições HTTP; a política HTTPS será verificada pela configuração declarada.

## 3. Requisitos funcionais

| ID | Requisito | Origem |
|---|---|---|
| RF-001 | O aluno informa o nome do bucket por variável; o nome precisa ser globalmente único. | PM, PO, BA |
| RF-002 | Terraform permite inicializar, revisar o plano e aplicar a configuração para criar exatamente um bucket S3 em `us-east-1`, acompanhado somente das configurações de segurança requeridas. | Usuário, PO |
| RF-003 | O bucket permanece privado, com as quatro opções de S3 Block Public Access ativadas e ACLs desativadas (`BucketOwnerEnforced`). | Usuário, BA |
| RF-004 | O bucket usa criptografia em repouso SSE-S3, sem configuração de chave KMS. | Usuário |
| RF-005 | A política do bucket nega requisições sem transporte seguro (`aws:SecureTransport` igual a `false`). | Usuário, BA |
| RF-006 | AWS CLI verifica a existência do bucket e permite conferir seus controles de acesso, ownership, criptografia, status público e política HTTPS. | Usuário, PO, BA |
| RF-007 | O exercício não envia objetos ao bucket; ele permanece vazio para permitir sua remoção ao fim do teste. | Usuário, BA |
| RF-008 | `terraform destroy` remove os recursos gerenciados pelo exercício; após a remoção, `terraform state list` não apresenta recursos. | Usuário, PM, PO |
| RF-009 | Em qualquer falha, o fluxo interrompe, mostra o comando e a mensagem de erro e não informa sucesso. Após correção, o aluno pode repetir o passo; recursos criados parcialmente são removidos pelo Terraform com o state disponível. | Usuário, PM, BA |
| RF-010 | Se `destroy` falhar porque o bucket deixou de estar vazio, o fluxo informa que o conteúdo precisa ser removido antes de repetir a destruição. | PM, BA |

## 4. Requisitos não funcionais

| ID | Requisito | Origem |
|---|---|---|
| RNF-001 | Manter baixo o custo: um único bucket vazio e temporário; sem chave KMS, logging adicional, data events ou métricas de requisição. | Usuário |
| RNF-002 | Não armazenar dados reais ou sensíveis. | Usuário |
| RNF-003 | Não há SLA próprio nem metas de latência, concorrência ou disponibilidade além do comportamento padrão do S3. | Usuário |
| RNF-004 | A execução pressupõe Terraform, AWS CLI e credenciais existentes na região `us-east-1`, com permissões suficientes para criar, consultar e excluir o bucket e suas configurações. A identidade deve ter `s3:ListBucket` limitado ao nome configurado para a validação do bucket antes do destroy; não se exige `s3:ListAllMyBuckets`. Provisionamento de IAM ou credenciais não pertence ao escopo. | PM, PO, BA |

## 5. Regras de negócio

- **RN-001:** Apenas um bucket S3 de teste é provisionado por execução.
- **RN-002:** O nome é fornecido pelo aluno e deve ser globalmente único; colisão deve ser exibida como erro acionável, sem declarar o provisionamento concluído.
- **RN-003:** O bucket não recebe objetos nem dados; o fluxo termina com sua destruição.
- **RN-004:** O bucket não pode permitir acesso público, deve manter ACLs desativadas e exigir HTTPS conforme os controles definidos nos RF-003 e RF-005.
- **RN-005:** Os recursos AWS usados na validação devem ser removidos antes de encerrar o exercício.

## 6. Fluxos

### FL-001 — Principal
1. O aluno define um nome globalmente único para o bucket.
2. Executa `terraform init` e revisa `terraform plan`.
3. Executa `terraform apply` e confirma a criação.
4. Usa AWS CLI para validar existência e configurações de segurança.
5. Executa `terraform destroy`.
6. Executa `terraform state list` e confirma que não restam recursos gerenciados pelo exercício.

### FL-002 — Alternativos
Nenhum fluxo alternativo é necessário para esta entrega.

### FL-003 — Erros
- Falha em `init`, `plan`, `apply`, validação ou `destroy`: interromper, mostrar o comando e a mensagem retornada, sem declarar sucesso.
- Colisão de nome ou permissão insuficiente: informar a causa retornada; corrigir o nome ou permissões e repetir.
- Falha parcial no `apply`: manter o state e usar Terraform para limpar os recursos antes de concluir.
- Falha no `destroy` por bucket não vazio: remover o conteúdo e repetir `terraform destroy`. Resposta 403 durante validação AWS CLI indica problema de permissão e não é tratada como sucesso.

## 7. Critérios de aceite

| ID | Critério verificável | Requisitos |
|---|---|---|
| CA-001 | `terraform init`, `terraform plan` e `terraform apply` terminam sem erro; o plano contém somente o bucket e suas configurações de segurança, sem serviços ou recursos não relacionados. | RF-001, RF-002 |
| CA-002 | Após `apply`, `aws s3api head-bucket --bucket <BUCKET_NAME> --region us-east-1` termina com sucesso. | RF-002, RF-006 |
| CA-003 | `aws s3api get-public-access-block --bucket <BUCKET_NAME> --region us-east-1` mostra `BlockPublicAcls`, `IgnorePublicAcls`, `BlockPublicPolicy` e `RestrictPublicBuckets` como `true`. | RF-003, RF-006 |
| CA-004 | `aws s3api get-bucket-ownership-controls --bucket <BUCKET_NAME> --region us-east-1` retorna `BucketOwnerEnforced`; `aws s3api get-bucket-encryption --bucket <BUCKET_NAME> --region us-east-1` retorna `AES256` (SSE-S3). | RF-003, RF-004, RF-006 |
| CA-005 | `aws s3api get-bucket-policy-status --bucket <BUCKET_NAME> --region us-east-1` retorna `IsPublic=false`; `aws s3api get-bucket-policy --bucket <BUCKET_NAME> --region us-east-1` mostra uma declaração `Deny` para `aws:SecureTransport=false`, cobrindo o bucket e seus objetos. Não é exigido teste de requisição HTTP. | RF-005, RF-006 |
| CA-006 | O exercício não envia objetos, não cria logging, CloudTrail data events nem métricas de requisição adicionais. | RF-007, RNF-001, RNF-002 |
| CA-007 | `terraform destroy` termina sem erro e `terraform state list` não retorna endereços de recursos do exercício. | RF-008 |
| CA-008 | Nos erros previstos em RF-009 e RF-010, o fluxo para, mostra o erro sem declarar sucesso e permite correção e nova tentativa ou limpeza pelo state. | RF-009, RF-010 |

## 8. Dependências e riscos

- O aluno precisa ter Terraform e AWS CLI disponíveis e uma identidade AWS com permissões suficientes para criar, consultar e excluir o bucket e suas configurações.
- O nome de bucket precisa estar disponível; colisões interrompem o `apply` e exigem outro nome.
- O destroy depende de o bucket estar vazio. Nenhum dado será enviado pelo exercício.
- SSE-S3 é a escolha de criptografia para manter o exercício simples; o AWS S3 aplica SSE-S3 por padrão a novos objetos e não cobra tarifa adicional pela criptografia em si.
- Logs de acesso entregues a outro bucket S3 não têm tarifa de entrega, mas a armazenagem é cobrada; CloudTrail data events e métricas de requisição têm cobranças adicionais. Esses componentes foram excluídos por decisão do usuário para limitar esforço e custo.

## 9. Deliberações e aprovações

| Revisão | Resultado | Deliberação registrada |
|---|---|---|
| PM | Aprovado pelo usuário | Credenciais/permissões existentes são pré-requisito; nome configurável e único; tratar falha de destroy em bucket não vazio. |
| PO | Aprovado pelo usuário | Critérios incluem comandos AWS CLI e resultados esperados; IAM não é provisionado pelo SDD. |
| BA | Aprovado pelo usuário | Bucket vazio; validar a política HTTPS pela configuração declarada, sem teste HTTP adicional. |
| Usuário | Aguardando | Gate final do PRD. |

**Questões em aberto:** nenhuma.

## 10. Referências AWS

- [Práticas de segurança do Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)
- [API HeadBucket e códigos de resposta](https://docs.aws.amazon.com/AmazonS3/latest/API/API_HeadBucket.html)
- [Criptografia SSE-S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingServerSideEncryption.html)
- [Opções de logging do S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/logging-with-S3.html)
- [CloudTrail S3 data events e cobrança](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-s3-data-events-governance.html)
- [Métricas S3 no CloudWatch e cobrança](https://docs.aws.amazon.com/AmazonS3/latest/userguide/cloudwatch-monitoring.html)
- [Preços do Amazon S3](https://aws.amazon.com/s3/pricing/)
