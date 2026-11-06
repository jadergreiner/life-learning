# LAB02 — ED-05 U2 AWS (Planejamento)

**Estado: proposta registrada; execução não autorizada.**  
**Método: três esferas obrigatórias, autonomia B, desafio I0 sem solução.**

O LAB02 aplica os princípios de idempotência e confiabilidade aprendidos no LAB01 a um contexto distribuído AWS com SQS Standard, Lambda e PostgreSQL em RDS. **Nenhum recurso foi provisionado e nenhuma sessão foi iniciada.**

O contrato, as contestações R6 e os critérios AWS-01–AWS-07 estão documentados em [docs/ed05-u2-aws.md](../../docs/ed05-u2-aws.md). Consulte o documento antes de qualquer implementação.

## Primeiro desafio independente (I0)

Uma mensagem financeira com `event_id` estável pode ser reentregue por SQS Standard. Duas execuções Lambda podem competir pelo mesmo evento e uma execução pode falhar após confirmar a transação no PostgreSQL.

**Pergunta inicial:** quais garantias cabem ao SQS, quais são responsabilidade da Lambda e quais precisam continuar sendo garantidas pelo PostgreSQL?

Entregáveis futuros: arquitetura justificada, infraestrutura como código, processador, testes AWS-01–AWS-07 e evidências reproduzíveis. Não há implementação de referência para esta etapa.

**Gates de governança:** consultar Notion; obter autorização explícita antes da sessão ou provisionamento; estimar custos e limpeza; não alterar a cadência de oito posições. Próxima regular permanece ciclo 17 P8 Databricks até nova sessão válida no Notion.
