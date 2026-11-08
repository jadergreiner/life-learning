## 1. Criar pacote executável mínimo

- [x] 1.1 Implementar `lambda_function.handler` sem dependências, que retorna `{"status":"ready"}` e não registra a entrada nem altera estado externo.
- [x] 1.2 Declarar o provider `hashicorp/archive` no root/módulo e configurar `archive_file` para gerar um ZIP reproduzível com o handler na raiz; geração e conferência do artefato ocorrem durante o plan.

## 2. Implementar o módulo Terraform processor

- [x] 2.1 Definir inputs e outputs do módulo para nome `lab02-processor`, runtime `python3.14`, handler, 128 MB, timeout de 3 s e retenção de logs default de 7 dias.
- [x] 2.2 Criar log group `/aws/lambda/lab02-processor` e execution role com trust somente de `lambda.amazonaws.com` e permissões apenas de CloudWatch Logs; não incluir ações SQS/RDS.
- [x] 2.3 Criar a função Lambda ZIP dependente do log group e da role, com hash do pacote, sem variáveis de ambiente, trigger, URL pública ou configuração VPC.
- [x] 2.4 Expor nome/ARN da função e ARN da execution role; documentar comportamento preparatório e limites do módulo em `modules/processor/README.md`.

## 3. Compor no ambiente e autorizar o provisionador

- [x] 3.1 Instanciar `modules/processor` no root `environments/lab`, preservar a trava de conta e o state SQS, e atualizar outputs e mensagens de erro.
- [x] 3.2 Ignorar o ZIP gerado em `.gitignore` local do módulo processor; manter as regras existentes de state, tfvars e planos no root.
- [x] 3.3 Preparar e validar policy IAM para `lab02-terraform`, limitada à função, log group e role nomeados, com `iam:PassRole` apenas para Lambda e attach restrito à policy de logging; preservar permissões SQS existentes.
- [x] 3.4 Atualizar README do ambiente com requisitos, perfil, handler sem integração, custo a estimar, comandos de plan/apply e teardown no mesmo state.

## 4. Validar plano e provisionar sob autorização

- [x] 4.1 Executar `terraform fmt -check`, `terraform init` e `terraform validate`; conferir o ZIP e a invocação local do handler sem publicar dados.
- [x] 4.2 Gerar plano com perfil `lab02-terraform` e confirmar conta `325422573352`, região `us-east-1`, nenhuma destruição/alteração nas filas existentes e apenas função, role/policy de logging e log group novos.
- [x] 4.3 Registrar estimativa de custo para invocações e CloudWatch Logs; aplicar o plano revisado somente após autorização operacional explícita, sem `-auto-approve`.
- [x] 4.4 Após apply autorizado, confirmar identidade, configuração Lambda, policy da role, retenção de logs, outputs e state; preservar state para integração e teardown futuros.









