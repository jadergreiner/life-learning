# Terraform do LAB02

Esta pasta contém módulos Terraform executáveis para SQS, Lambda e PostgreSQL em RDS. O root `environments/lab` compõe os três no mesmo state local para a conta `325422573352`, região `us-east-1`. Os componentes estão provisionados, mas ainda não há fluxo de aplicação SQS → Lambda → banco.

## Estrutura

```text
terraform/
├── environments/
│   └── lab/             # root module, provider, state e outputs do ambiente
└── modules/
    ├── queue/           # fila Standard, DLQ, SSE-SQS e redrive
    ├── processor/       # Lambda preparatória, role de logging e log group
    └── database/        # PostgreSQL privado em RDS e secret master gerenciado
```

A Lambda ainda não tem trigger/event source mapping, VPC ou permissões de aplicação; o handler só responde `{"status":"ready"}`. O RDS não tem ingress, schema ou usuário de aplicação. A configuração, os limites de conectividade, custos e procedimento de teardown estão no [README do ambiente `lab`](environments/lab/README.md). O roteiro proposto para conectar os módulos está em [labs/lab02/integration-plan.md](../integration-plan.md).

State, backups, planos e `terraform.tfvars` são locais e devem ser preservados para reconciliar ou destruir recursos no mesmo root. Use o perfil `lab02-terraform`, confirme conta e região e revise estimativa, plano e autorização operacional antes de qualquer apply. Esta documentação não autoriza uma nova alteração AWS nem inicia a sessão U2.1.

Este laboratório é distinto do exercício temporário de bucket S3 em `labs/lab002-terraform`, que mantém sua própria configuração e ciclo de vida.
