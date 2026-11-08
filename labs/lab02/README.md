# LAB02 — ED-05 U2 AWS (Planejamento)

**Estado: fila SQS e DLQ provisionadas em 07/11/2026 na conta correta `325422573352`, região `us-east-1`; sessão pedagógica e processamento ainda não iniciados.**  
**Método: três esferas obrigatórias, autonomia B, desafio I0 sem solução.**

O LAB02 aplica os princípios de idempotência e confiabilidade aprendidos no LAB01 a um contexto distribuído AWS com SQS Standard, Lambda e PostgreSQL em RDS. A fila `lab02-sqs-20261107` e a DLQ `lab02-sqs-20261107-dlq` estão vazias em `us-east-1` na conta `325422573352`. A tentativa anterior na conta `437537458973` foi removida. Foi criado o usuário IAM dedicado `lab02-terraform` com acesso restrito ao ciclo de vida dessas filas. Não foram criados produtor, consumidor, Lambda ou RDS. Nenhuma sessão foi iniciada.

O contrato, as contestações R6 e os critérios AWS-01–AWS-07 estão documentados em [docs/ed05-u2-aws.md](../../docs/ed05-u2-aws.md). Consulte o documento antes de continuar a implementação ou integrar outros serviços.

## Primeiro desafio independente (I0)

Uma mensagem financeira com `event_id` estável pode ser reentregue por SQS Standard. Duas execuções Lambda podem competir pelo mesmo evento e uma execução pode falhar após confirmar a transação no PostgreSQL.

**Pergunta inicial:** quais garantias cabem ao SQS, quais são responsabilidade da Lambda e quais precisam continuar sendo garantidas pelo PostgreSQL?

Entregáveis futuros: arquitetura justificada, infraestrutura como código, processador, testes AWS-01–AWS-07 e evidências reproduzíveis. Não há implementação de referência para esta etapa.

**Gates de governança:** consultar Notion; obter autorização específica antes de iniciar a sessão ou provisionar componentes adicionais; estimar custos e limpeza; não alterar a cadência de oito posições. Próxima regular permanece ciclo 17 P8 Databricks até nova sessão válida no Notion.
