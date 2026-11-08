# Módulo de processamento Lambda do LAB02

Este módulo compõe uma única função Lambda preparatória chamada `lab02-processor`, empacotada como ZIP local. O handler Python `lambda_function.handler` retorna somente `{"status":"ready"}`; não consome mensagens, registra o evento, acessa banco ou causa efeitos externos.

## Configuração padrão

| Entrada | Padrão | Descrição |
|---|---:|---|
| `function_name` | `lab02-processor` | Nome da função; também determina o nome da role e do log group. |
| `runtime` | `python3.14` | Runtime gerenciado da AWS. |
| `handler` | `lambda_function.handler` | Ponto de entrada do ZIP. |
| `memory_size` | `128` MB | Memória da função. |
| `timeout_seconds` | `3` s | Timeout do handler vazio. |
| `log_retention_days` | `7` dias | Retenção do log group, ajustável pelo root. |

O data source `archive_file` gera `lambda_function.zip` a partir de `lambda_function.py` e calcula o hash usado para detectar mudanças. Preserve esse ZIP entre `terraform plan` e `terraform apply`; ele é artefato local ignorado pelo Git.

## Recursos e permissões

- Uma função `aws_lambda_function` ZIP, arquitetura `x86_64`, sem variáveis de ambiente, URL pública, VPC ou trigger.
- Uma execution role que confia apenas em `lambda.amazonaws.com` e anexa `AWSLambdaBasicExecutionRole` para logging. A role não recebe permissões SQS, RDS, Secrets Manager ou de rede.
- Um log group `/aws/lambda/lab02-processor` com retenção padrão de 7 dias, criado antes da função.
- Outputs: `function_name`, `function_arn`, `execution_role_arn` e `log_group_name`.

## Limites desta etapa

Esta função não é o processador financeiro do LAB02 e não atende ainda aos critérios AWS-01–AWS-07. Event source mapping SQS, conexão com RDS, VPC, idempotência, concorrência, falhas parciais e redrive pertencem a mudanças futuras. Antes da integração SQS, revisar o timeout da função, batch size/janela e visibility timeout da fila em conjunto.

O root module consumidor fornece os providers AWS e Archive, região, validação da conta e state. Planejar e aplicar somente após revisar o plano, a estimativa de custo e a autorização operacional específica do ambiente.
