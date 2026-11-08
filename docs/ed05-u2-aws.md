# ED-05 U2 — AWS | Contrato experimental do laboratório

**Estado (atualizado em 08/11/2026):** SQS/DLQ, Lambda preparatória `lab02-processor` e PostgreSQL privado em RDS `lab02-postgres` estão provisionados na conta `325422573352`, região `us-east-1`. As filas da tentativa inicial na conta `437537458973` foram removidas. A sessão pedagógica U2.1 e o fluxo de processamento continuam não iniciados.  
**Data de registro original:** 06/11/2026 (Brasília).  
**Esfera:** AWS (2 de 3: Local → AWS → Databricks obrigatórias no piloto).  
**Método:** autonomia B — desafio independente I0, intervenções I1–I3 somente quando solicitadas/necessárias.  
**Governança:** a autorização operacional registrada em 07/11/2026 cobriu as filas SQS; uma autorização explícita posterior cobriu a criação do PostgreSQL RDS em 08/11/2026 após revisão de plano e custos. O usuário IAM `lab02-terraform` mantém as policies de SQS/Lambda e a policy managed de provisão RDS. A Lambda permanece preparatória, sem trigger, VPC ou permissões de aplicação; o banco permanece sem schema, usuário de aplicação e ingress. Qualquer integração ou alteração AWS futura requer autorização e estimativa próprias. Não alterar a cadência oficial de oito posições, iniciar sessão automaticamente, aprovar competência integral ou presumir custos reais.

## Origem e continuidade

- U1 Local concluída pedagogicamente segundo registro canônico no Notion; relatório do GitHub informa 12 testes aprovados, sem reexecução independente do Conselho.
- Fonte operacional e pedagógica: [Notion — U1 Local](https://app.notion.com/p/40f02f2729f9819da78cffed04628caa).
- Artefatos anteriores: [feature/lab01](https://github.com/jadergreiner/life-learning/tree/feature/lab01).
- Baseline e roteiro de fases para futuras integrações: [Plano de integração do LAB02](../labs/lab02/integration-plan.md).
- U2 introduz falhas distribuídas do SQS e da Lambda; não é simples cópia do laboratório Local. U3 Databricks permanece obrigatória, em contexto analítico.

## Problema de negócio

Uma instituição financeira recebe eventos CREDIT/DEBIT com identificador estável de negócio, account_id, amount decimal e currency BRL. Um mesmo evento pode ser reentregue e processado em execuções concorrentes. O efeito financeiro persistido precisa permanecer correto, mesmo com reentregas, falhas antes/depois do commit e lotes parcialmente inválidos.

**Invariante central:** no máximo um efeito financeiro confirmado por event_id; saldo consistente com os efeitos confirmados. Não afirmar exactly-once de entrega de mensagens ou de efeitos externos.

## Arquitetura de referência — hipótese a ser contestada na I0

- Amazon SQS Standard: origem das mensagens, fila principal e política de DLQ.
- AWS Lambda: consumidor, concorrência e decisão de retorno de falhas individuais de lote.
- Amazon RDS for PostgreSQL: estado das contas, eventos e transações, restrições de integridade e atomicidade dos efeitos.
- Amazon CloudWatch: logs, métricas e alarmes orientados à investigação.
- Terraform: infraestrutura reproduzível, permissões mínimas e destruição documentada.

**Importante:** o aluno deve defender as responsabilidades dos serviços, controles de idempotência, falhas, custos e eventuais alternativas. Este documento não fornece Terraform, código de consumo, diagrama definitivo nem parâmetros prontos.

## Critérios de aceitação congelados para avaliação do escopo proposto

| ID | Ensaio obrigatório | Evidência necessária |
|---|---|---|
| AWS-01 | Evento válido | Efeito confirmado uma única vez; saldo correto |
| AWS-02 | Reentrega da mensagem | Nenhuma duplicação financeira |
| AWS-03 | Execuções simultâneas da mesma chave | Um efeito confirmado para event_id |
| AWS-04 | Falha entre commit do banco e conclusão da execução | Reentrega segura e estado consistente |
| AWS-05 | Falha parcial de lote | Identificação de itens com falha, sem reaplicar efeitos já confirmados |
| AWS-06 | Falha recorrente e DLQ | Evidência de redirecionamento e procedimento controlado de recuperação |
| AWS-07 | Observabilidade | Diagnóstico rastreável do processamento por logs e métricas |

**Gate:** código/infraestrutura versionados + testes reproduzíveis e evidências + defesa técnica independente. Não acrescentar gates retroativos sem aprovação explícita do aluno, seguindo o precedente da U1. A aprovação de U2 não representa aprovação global de ED-05.

## Rodada de contestação R6 (papéis pedagógicos virtuais)

- **Helena — aprendizagem:** preservar o contrato de negócio e exigir adaptação independente; registrar níveis de intervenção I0–I3; avaliar retenção e transferência.
- **Fernanda — rigor:** exigir T01–T07 reformulados para falhas de SQS/Lambda; demonstrar DB state, não apenas resposta da função; não confundir teste simulado com crash real.
- **Marcelo — custo/tempo:** conter escopo; contabilizar estimativa e teto de gastos antes de autorizar provisionamento; separar custos de RDS, rede, Lambda, SQS e CloudWatch.
- **Ricardo — portabilidade:** separar entrega da fila, processamento do runtime e integridade transacional; comparar garantias entre Local e AWS.

Divergência: profundidade de infraestrutura. Síntese: arquitetura mínima que demonstre as invariantes, deixando multi-região, alta disponibilidade avançada, análise de performance prolongada e efeitos externos complexos fora do gate.

## Limites e pré-condições

- Sem processamento integrado nem alteração da cadência por este registro.
- Antes de executar: decidir região/conta autorizada, estimativa de custos, teto, alertas, credenciais/segredos, acesso de rede ao RDS, permissões IAM e plano de teardown.
- Não publicar segredos ou dados reais em repositório público.
- Dimensionar visibility timeout, timeout Lambda, concorrência, batch size e política de DLQ somente após raciocínio independente/validação. Custos variam com região, tempo, VPC e recursos alocados.
- Se o teste exigir efeitos externos, definir contrato e distinguir garantias sobre o PostgreSQL de garantias do provedor externo.
- Não avançar o ciclo 17 P8 (DATABRICKS) ao registrar ou executar uma atividade extraordinária AWS.

## Primeira unidade sugerida — U2.1 (não iniciada)

**Desafio I0:** definir desenho de arquitetura, responsabilidades SQS/Lambda/PostgreSQL, limites transacionais, recursos mínimos, hipóteses de falha, testes e critérios de custos.

**Pergunta a frio:** quais garantias pertencem ao SQS, quais à Lambda e quais precisam permanecer no PostgreSQL?

A sessão pedagógica U2.1 continua aguardando autorização e não foi aberta no Notion. Para provisionar qualquer recurso além da fila SQS, da DLQ e do usuário IAM dedicado já criados, obter autorização operacional específica e revisar os custos primeiro.

## Referências

- [AWS — Using Lambda with Amazon SQS](https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html)
- [AWS — Reporting batch item failures](https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-errorhandling.html)
- [AWS — Pricing Calculator](https://calculator.aws/)
- [Notion — Governança e Catálogo de Competências](https://app.notion.com/p/40c02f2729f981c2bb7acd89a631d32c)
