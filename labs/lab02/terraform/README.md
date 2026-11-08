# Terraform do LAB02

Esta pasta reserva a estrutura para uma futura implementação da infraestrutura do LAB02 (SQS, Lambda e PostgreSQL em RDS). Por enquanto, contém apenas documentação: não há configuração Terraform executável, state ou recursos AWS provisionados.

## Estrutura

```text
terraform/
├── environments/
│   └── lab/             # futuro root module que compõe o laboratório
└── modules/
    ├── queue/           # futura responsabilidade de mensageria SQS
    ├── processor/       # futura responsabilidade de processamento Lambda
    └── database/        # futura responsabilidade do PostgreSQL em RDS
```

Os módulos são reservas organizacionais. Seus contratos, recursos, rede, variáveis, versões de provider e configuração de estado ainda não foram definidos. Uma especificação própria deve preceder qualquer implementação; provisionamento AWS também depende de autorização explícita.

Este laboratório é distinto do exercício temporário de bucket S3 em `labs/lab002-terraform`, que mantém sua própria configuração e ciclo de vida.
