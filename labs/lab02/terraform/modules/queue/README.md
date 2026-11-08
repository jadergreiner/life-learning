# Módulo de fila SQS do LAB02

Este módulo define uma fila principal SQS Standard, uma DLQ SQS Standard e a política que encaminha mensagens após o número configurado de recebimentos sem sucesso. A DLQ permite redrive somente da fila principal declarada.

## Entradas

| Entrada | Obrigatória | Limites / padrão | Uso |
|---|---:|---|---|
| `name_prefix` | Sim | 1–76 caracteres: letras, números, `_` ou `-` | Nome da fila; a DLQ recebe o sufixo `-dlq`. |
| `message_retention_seconds` | Sim | Inteiro de 60 a 1.209.600 | Retenção da fila principal. |
| `dlq_message_retention_seconds` | Sim | Inteiro de 60 a 1.209.600 | Retenção da DLQ. Considere o período de investigação e redrive ao escolher o valor. |
| `visibility_timeout_seconds` | Sim | Inteiro de 0 a 43.200 | Tempo que uma mensagem recebida fica invisível para outros consumidores. Deve ser compatível com o timeout e a estratégia de processamento do futuro consumidor. |
| `receive_wait_time_seconds` | Não | Inteiro de 0 a 20; padrão `20` | Long polling da fila principal. `0` seleciona short polling. |
| `max_receive_count` | Sim | Inteiro de 1 a 1.000 | Recebimentos sem sucesso antes de encaminhar a mensagem para a DLQ. |

Os valores obrigatórios permanecem sem defaults para que o root module defina e justifique o sizing do laboratório. As validações rodam durante avaliação do Terraform antes de qualquer criação.

## Saídas

- `queue_name`, `queue_url`, `queue_arn`: fila principal.
- `dead_letter_queue_name`, `dead_letter_queue_url`, `dead_letter_queue_arn`: DLQ.

Use os ARNs em futuras políticas IAM de privilégio mínimo e as URLs ao configurar integrações que as exigirem.

## Semântica e limites

- As filas são Standard: a entrega é pelo menos uma vez, podem ocorrer duplicatas e a ordem não é estrita. A fila não fornece processamento exactly-once.
- A DLQ auxilia a isolar mensagens com falhas recorrentes; definir o procedimento de inspeção e redrive é responsabilidade do laboratório.
- Idempotência do efeito financeiro, tratamento de lotes parciais e consistência de saldo pertencem ao consumidor e ao PostgreSQL.
- O módulo habilita SSE-SQS, com chaves gerenciadas pelo serviço, e não cria chave KMS. Também não cria consumidor Lambda, event source mapping, permissões IAM, banco, rede ou alarmes.
- Antes de compor este módulo com Lambda, revisar timeout do consumidor, visibility timeout, batch size e política de falha parcial em conjunto.

## Compatibilidade do provider

O módulo não declara nem fixa uma versão do AWS Provider. A fila e os recursos dedicados de redrive/allow policy usados aqui constam na documentação do AWS Provider 6.41.0; o root module consumidor deve declarar a versão compatível e configurar a região.

## Uso e ciclo de vida

O root module do laboratório deve configurar o AWS Provider e fornecer os valores requeridos. Este diretório é um módulo filho e não possui configuração de provider, backend ou state próprio. Inicialização, planejamento e eventual teardown pertencem ao ambiente consumidor; não execute `apply` sem autorização operacional explícita, estimativa de custo e plano de limpeza do LAB02.
