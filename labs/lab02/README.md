# LAB02 — ED-05 U2 AWS (Planejamento)

**Estado: SQS/DLQ, Lambda preparatória e PostgreSQL em RDS provisionados em `325422573352`, região `us-east-1`; sessão pedagógica U2.1 e processamento integrado ainda não iniciados.**  
**Método: três esferas obrigatórias, autonomia B, desafio I0 sem solução.**

O LAB02 aplica princípios de confiabilidade distribuída a SQS Standard, Lambda e PostgreSQL em RDS. O root Terraform do ambiente `lab` compõe a fila `lab02-sqs-20261107`, a DLQ `lab02-sqs-20261107-dlq`, a função preparatória `lab02-processor` e o banco `lab02-postgres`. A tentativa inicial na conta `437537458973` foi removida. O usuário IAM dedicado `lab02-terraform` tem políticas de provisionamento do ambiente; a execution role da Lambda permanece limitada a logs.

Ainda não existe produtor nem processamento integrado: a Lambda só responde `{"status":"ready"}`, não consome SQS, não está associada à VPC e não acessa o RDS. O banco permanece sem schema ou usuário de aplicação, privado e sem ingress. Nenhuma sessão pedagógica foi iniciada.

O contrato, as contestações R6 e os critérios AWS-01–AWS-07 estão documentados em [docs/ed05-u2-aws.md](../../docs/ed05-u2-aws.md). Consulte o documento antes de continuar a implementação ou integrar outros serviços.

Consulte também o [plano de integração](integration-plan.md) para baseline, gaps, decisões independentes e sequência sugerida. Ele não substitui autorização operacional nem inicia U2.1.

## Primeiro desafio independente (I0)

Uma mensagem financeira com `event_id` estável pode ser reentregue por SQS Standard. Duas execuções Lambda podem competir pelo mesmo evento e uma execução pode falhar após confirmar a transação no PostgreSQL.

**Pergunta inicial:** quais garantias cabem ao SQS, quais são responsabilidade da Lambda e quais precisam continuar sendo garantidas pelo PostgreSQL?

Entregáveis futuros: arquitetura justificada, infraestrutura como código, processador, testes AWS-01–AWS-07 e evidências reproduzíveis. Não há implementação de referência para esta etapa.

**Gates de governança:** consultar Notion; obter autorização específica antes de iniciar a sessão ou provisionar componentes adicionais; estimar custos e limpeza; não alterar a cadência de oito posições. Próxima regular permanece ciclo 17 P8 Databricks até nova sessão válida no Notion.
