## 1. Compor o root module

- [x] 1.1 Criar configuração Terraform do root com versões compatíveis de Terraform/AWS Provider, região, identificação da conta atual e trava contra account ID diferente do aprovado.
- [x] 1.2 Instanciar somente `modules/queue` com os valores confirmados: prefixo `lab02-sqs-20261107`, retenção 4 dias, DLQ 14 dias, visibilidade 30 s, max receive 10 e long polling 20 s.
- [x] 1.3 Expor account ID, região e outputs da fila principal/DLQ.
- [x] 1.4 Ignorar state, variáveis e planos locais; fornecer `terraform.tfvars.example` sem credenciais e atualizar README com init, plan, apply, verificação e teardown.

## 2. Validar e planejar sem provisionar

- [x] 2.1 Executar `terraform fmt -check`, `terraform init` e `terraform validate` no root.
- [x] 2.2 Gerar plano usando o perfil autorizado e confirmar a conta-alvo aprovada, região `us-east-1`, ausência de colisão e somente recursos SQS aprovados.
- [x] 2.3 Registrar estimativa: filas vazias e sem tráfego, sem tarifa mínima SQS, chamadas dentro da franquia de 1 milhão/mês; não executar se o plano incluir outro recurso ou se a estimativa não corresponder às premissas.

## 3. Provisionar e confirmar

- [x] 3.1 Aplicar o plano revisado na conta/região aprovadas; não usar `-auto-approve`.
- [x] 3.2 Confirmar por AWS CLI os atributos SSE-SQS, retenções, visibility timeout, long polling e políticas redrive/redrive-allow, e conferir Terraform outputs/state.
- [x] 3.3 Confirmar que nenhuma mensagem foi enviada e preservar state para teardown futuro.
- [x] 3.4 Atualizar os status locais do LAB02 para registrar as filas provisionadas, a identidade IAM dedicada e que a sessão/fluxo de processamento não foram iniciados.

## 4. Corrigir conta-alvo após provisionamento inicial

- [x] 4.1 Remover a fila, a DLQ e as políticas redrive da conta `437537458973` e confirmar ausência dos recursos e state gerenciado.
- [x] 4.2 Atualizar variáveis locais e documentação para a conta correta `325422573352`.
- [x] 4.3 Criar o usuário IAM `lab02-terraform` com permissões SQS restritas ao prefixo aprovado, revisar o plano e provisionar apenas fila e DLQ na conta-alvo.
- [x] 4.4 Confirmar identidade, atributos AWS, outputs e state na conta-alvo; registrar o resultado e preservar state para teardown.
