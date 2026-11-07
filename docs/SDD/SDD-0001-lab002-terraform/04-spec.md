# SPEC — SDD-0001 lab002-terraform

Status: Aprovado pelo usuário
Data: 2026-11-07

## 1. Visão arquitetural

Laboratório local, individual e temporário, separado de `labs/lab02`. O aluno executa Terraform com credenciais AWS já configuradas e valida os recursos com AWS CLI. O Terraform cria um bucket vazio e as configurações de segurança; ao final, `terraform destroy` remove os recursos. Nenhum recurso será provisionado durante esta etapa de especificação.

```text
Aluno
  ├─ Terraform CLI ── AWS Provider ── S3 (us-east-1)
  │    └─ state local, ignorado pelo Git
  └─ AWS CLI ──────────────────────── S3 (consultas de validação)
```

### Componentes propostos

- `labs/lab002-terraform/README.md`: pré-requisitos, comandos, verificações esperadas e limpeza.
- `labs/lab002-terraform/main.tf`: provider AWS em `us-east-1`, bucket e política HTTPS.
- `labs/lab002-terraform/variables.tf`: prefixo/nome lógico do bucket e região, com validações necessárias.
- `labs/lab002-terraform/outputs.tf`: nome e ARN do bucket para facilitar validação.
- `labs/lab002-terraform/.gitignore`: state local, backups, `.terraform/`, variáveis locais, planos salvos e logs de crash.
- `.terraform.lock.hcl`: versionamento dos providers selecionados para reprodutibilidade.
- Recursos AWS: `aws_s3_bucket`, `aws_s3_bucket_public_access_block`, `aws_s3_bucket_ownership_controls`, `aws_s3_bucket_server_side_encryption_configuration` e `aws_s3_bucket_policy`.

O provider usará o namespace S3 `account-regional` e derivará um nome que inclua identificadores de conta/região e o prefixo escolhido. Isso reduz colisões globais; não substitui autorização IAM nem garante que o nome não esteja em uso no próprio namespace.

## 2. Fluxo de dados e execução

1. Terraform lê a configuração local e as credenciais de uma identidade IAM existente.
2. `terraform init` baixa o provider declarado e registra a seleção em `.terraform.lock.hcl`.
3. `terraform plan` calcula as alterações antes de qualquer chamada de criação.
4. `terraform apply` cria o bucket e suas configurações no S3 em `us-east-1`.
5. AWS CLI faz consultas somente de leitura ao bucket para validar existência e controles.
6. `terraform destroy` remove os recursos; `terraform state list` confirma que não restam recursos gerenciados.

Não há objetos, dados de aplicação, serviços AWS adicionais nem integrações externas. Não há backend remoto: o state fica local, é de uso individual e não oferece coordenação ou recuperação compartilhada. Execuções concorrentes com o mesmo diretório/state não são suportadas.

## 3. Decisões técnicas

| ID | Decisão | Justificativa e consequência |
|---|---|---|
| ADR-0002 | Usar state Terraform local, ignorado pelo Git, para este exercício individual e temporário. | Evita criar bucket/tabela de backend e outros custos. Não permite trabalho concorrente nem recuperação compartilhada; o aluno deve preservar o state até concluir `destroy`. |
| ADR-0003 | Usar namespace S3 `account-regional` com nome derivado do prefixo do aluno, conta e região. | Reduz colisões e risco de reuso global do nome, sem adicionar serviços. Requer versão compatível do AWS Provider; colisão dentro da conta/região ainda deve ser tratada como erro. |
| ADR-0004 | Limitar a implementação ao bucket e aos cinco recursos/configurações Terraform listados nesta SPEC. | Mantém baixo custo e esforço e exclui IAM, logging, CloudTrail data events e métricas adicionais. |

Detalhes completos das decisões estão em `docs/adrs/ADR-0002-terraform-local-state.md`, `docs/adrs/ADR-0003-s3-account-regional-namespace.md` e `docs/adrs/ADR-0004-lab-scope.md`.

## 4. Segurança

### Controles do bucket

- Ativar as quatro opções de S3 Block Public Access.
- Desativar ACLs com `BucketOwnerEnforced`.
- Configurar SSE-S3 (`AES256`), sem KMS.
- Aplicar política que nega transporte inseguro (`aws:SecureTransport=false`). A política deve cobrir bucket e objetos e ser verificada por sua configuração, sem teste HTTP separado.
- Não enviar nem armazenar dados no bucket.

### Identidade e permissões

- Usar somente identidade IAM preexistente, nomeada e de privilégio mínimo; nunca usar credenciais root para `plan`, `apply` ou `destroy`.
- Permissões devem se limitar ao bucket derivado e ao ARN de objetos quando necessário, incluindo as ações de consulta e configuração exigidas pelo fluxo. Não solicitar `s3:ListAllMyBuckets` nem `s3:*` amplo.
- Criação de usuários, roles, políticas IAM e credenciais está fora do escopo; a identidade é pré-requisito externo.

### State e repositório

- Não versionar `.terraform/`, `terraform.tfstate*`, arquivos `*.tfvars`, planos salvos ou logs de crash. Versionar `.terraform.lock.hcl`.
- State pode conter metadados e valores sensíveis de configuração; não deve ser enviado, compartilhado ou publicado.
- O state deve permanecer disponível localmente até o `destroy` terminar e ficar vazio.

### Limites e ameaças consideradas

- A política `aws:SecureTransport=false` pode afetar futuras integrações service-to-service quando a chave de condição for redigida. Qualquer integração futura exige revisão da política; nenhuma está no escopo atual.
- `account-regional` restringe o namespace, mas não concede autorização e não impede colisões dentro da mesma conta/região. Após o destroy, outro principal da mesma conta pode usar o nome; não tratá-lo como segredo ou identidade permanente.
- Se o bucket receber objetos, `destroy` pode falhar; remover conteúdo e repetir conforme o PRD.
- State ou credenciais no Git, uso de root, permissões amplas, exposição pública, transporte sem TLS e recursos esquecidos são riscos mitigados pelas regras acima e pelo escopo temporário.
- Não criar logs de acesso, CloudTrail S3 data events ou métricas de requisição, por decisão de custo/escopo do PRD.

## 5. Dados e IA

Não se aplica: bucket vazio, sem dados de aplicação, pipelines, migrações ou governança de dados complexa. Não há componentes de IA.

## 6. Tratamento de falhas

- Falhas de `init`, `plan`, `apply`, comandos de validação ou `destroy` interrompem o fluxo e exibem comando e erro, sem declarar sucesso.
- Falta de credenciais ou permissões exige correção fora do Terraform; não criar IAM automaticamente.
- Colisão do nome requer novo prefixo/nome configurado e novo plano.
- Criação parcial é reconciliada usando o state Terraform preservado.
- Se `destroy` falhar por bucket não vazio, remover objetos e repetir.
- `terraform state list` vazio confirma apenas que não restam recursos rastreados pelo state do exercício; não substitui confirmação de remoção na AWS.

## 7. Riscos e mitigação

| Risco | Mitigação prevista |
|---|---|
| Namespace ou nome já em uso | Prefixo configurável e erro explícito; alterar prefixo e repetir. |
| State, credenciais ou plano salvos no Git | `.gitignore`, instruções claras e state local não compartilhado. |
| Identidade com permissão excessiva ou root | Pré-requisito de IAM nomeado e mínimo; root proibido para operações do laboratório. |
| Bucket público ou sem TLS | BPA completo, ownership controls e política HTTPS com validação CLI. |
| `destroy` bloqueado por objetos | Bucket permanece vazio; se conteúdo existir, removê-lo e repetir. |
| Recurso esquecido ou custo residual | Um bucket temporário; `destroy` e state sem recursos como encerramento obrigatório. |
| Política HTTPS afetar integração futura | Revisão explícita antes de adicionar integrações AWS. |

## 8. Deliberações e aprovação dos arquitetos

| Revisão | Resultado | Registro |
|---|---|---|
| Solution Architect | Aprovado pelo usuário | Arquitetura local, namespace `account-regional`, sem recursos além do bucket e proteções. |
| Security Architect | Recomendação aceita sob delegação do usuário | Usar identidade IAM de privilégio mínimo, nunca root; proteger state; uso individual; revisar HTTPS antes de integração futura. |
| Data Architect | Não acionado | PRD não contém dados complexos, pipelines ou migrações. |
| AI Architect | Não acionado | PRD não contém IA. |

## 9. Referências técnicas

- [AWS S3 — namespaces de nomes de buckets](https://docs.aws.amazon.com/AmazonS3/latest/userguide/gpbucketnamespaces.html)
- [AWS S3 — práticas de segurança](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)
- [AWS Provider — recurso aws_s3_bucket](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket)
- [Terraform — state](https://developer.hashicorp.com/terraform/language/state)

## 10. Aprovação

Questões em aberto: nenhuma identificada na SPEC.
Gate: aprovado pelo usuário em 2026-11-07; Etapa 5 (PLAN) iniciada.
