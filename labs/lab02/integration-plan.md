# Plano de integração do LAB02

**Escopo:** avaliação documental e roteiro para futuras integrações SQS → Lambda → PostgreSQL. Este documento não inicia a sessão U2.1 nem autoriza alterações AWS.

## Baseline e lacunas

Este inventário foi composto a partir dos módulos, root Terraform e specs do repositório. Reconfirme o estado AWS e custos no início de qualquer etapa operacional; este roteiro não é uma consulta live.

| Peça | Responsabilidade prevista | Estado no repositório | Lacuna para o fluxo integrado |
|---|---|---|---|
| SQS Standard + DLQ | Receber eventos e encaminhar falhas recorrentes segundo redrive policy | Módulo de fila e root Terraform criam fila principal, DLQ, SSE-SQS, redrive e redrive-allow | Não há produtor nem consumidor associado; fila Standard permite redelivery/duplicatas |
| Lambda `lab02-processor` | Futuro consumidor | Módulo cria pacote ZIP, função, role de logging e log group; handler atual apenas responde `{"status":"ready"}` | Sem event source mapping, permissão SQS, VPC, acesso a Secrets Manager ou lógica de negócio |
| PostgreSQL em RDS | Persistência futura de contas, eventos e transações | Módulo cria PostgreSQL Single-AZ privado, storage criptografado, backup de 1 dia e senha master gerenciada | Sem schema/migrations, usuário de aplicação, ingress de rede ou integração Lambda; master não é credencial de aplicação |
| Root Terraform | Compor e reconciliar infraestrutura | Um root compõe fila, Lambda e RDS no ambiente `lab` | Compartilha state/ciclo de vida; plano e teardown podem afetar mais de uma peça |
| Observabilidade | Diagnosticar o fluxo e suas falhas | Lambda possui log group com retenção limitada | Não há correlação por evento, alarmes ou runbook de investigação/redrive descritos como fluxo integrado |

O fluxo está deliberadamente incompleto. A Lambda não alcança o endpoint privado do RDS com a configuração atual, e a role de logging não tem permissões de aplicação. Nenhuma destas lacunas deve ser fechada sem uma etapa aprovada própria.

## Ordem de integração e gates

| Etapa | Pré-requisitos e decisões | Saída/evidência para concluir | Próxima dependência |
|---|---|---|---|
| 0. Reconciliar baseline | Revisar módulos, specs e documentação; confirmar estado AWS, conta/região, custos e recursos ativos antes de qualquer plano operacional | Inventário factual, lacunas e estimativa inicial atualizados; nenhuma afirmação de que o fluxo ou U2.1 já começou | Defesa independente I0 |
| 1. Defender arquitetura I0 | Explicar as responsabilidades distintas de SQS, Lambda e PostgreSQL e analisar redelivery, concorrência, falha antes/depois de commit, lote parcialmente inválido e mensagem venenosa | Decisões do aluno e matriz de falhas justificadas contra o invariante e AWS-01–AWS-07; registrar alternativas descartadas e dúvidas sem receita de implementação | Contrato e modelo de dados |
| 2. Definir contrato e persistência | Definir campos, validação e evolução do evento; modelo de contas/eventos/transações, migrações, restrições e limites transacionais. O aluno deve defender o mecanismo que protege o efeito financeiro | Contrato versionado, plano de migração/rollback e critérios para entrada inválida, duplicada e concorrente; sem dados reais | Rede e identidade de runtime |
| 3. Projetar conectividade e credenciais | Escolher subnets/associação VPC da Lambda, security groups, caminho de acesso ao Secrets Manager, identidade de aplicação e privilégios mínimos. Comparar endpoints privados e saída de rede quanto a custo e exposição | Diagrama/ADR aprovado; plano restrito ao caminho Lambda → RDS na porta PostgreSQL e leitura do secret necessário; segredo master continua fora do runtime de negócio | Integração de eventos |
| 4. Associar SQS e Lambda | Criar permissões SQS mínimas na execution role e event source mapping; justificar batch size, batching window, timeout, visibility timeout, concorrência, retries, falha parcial e redrive count. Conferir a relação timeout/visibility timeout na documentação atual da AWS | Plano Terraform revisado; mapping habilitado somente com handler preparado; evidência de falha parcial e DLQ sem reaplicar efeitos persistidos | Persistência observável |
| 5. Instrumentar e operar | Definir logs estruturados sem dados sensíveis, correlação por identificador de evento, métricas, alarmes, retenção, inspeção de DLQ e procedimento controlado de redrive | Painel/consultas ou evidência equivalente para sucesso, retry, idade da mensagem, erro e DLQ; runbook de investigação e recuperação | Ensaios controlados |
| 6. Validar AWS-01–AWS-07 | Autorizar ambiente e custo; preparar dados sintéticos; definir como cada falha será induzida e como o estado persistido comprovará o resultado | Evidências reproduzíveis de cada critério existente, incluindo estado do banco e da fila; defesa técnica independente. Não substituir evidência real por invocação simulada quando o critério exigir falha real | Revisão pedagógica e operacional |
| 7. Fechar ciclo com custo e teardown | Revisar custo de RDS, rede/endpoints, Lambda, SQS, logs e snapshots; obter autorização específica para apply; seguir state e runbook do root | Estimativa/teto aprovados antes do apply; plano revisado; no encerramento, snapshot final deliberado, state reconciliado e custos remanescentes registrados | Próxima sessão, se autorizada |

## Dependências transversais

- **Entrega:** o event source mapping faz a leitura e invoca a função em lotes. A fila continua sendo Standard, portanto a entrega não é uma garantia de efeito financeiro único. A AWS descreve o polling, timeout e visibility timeout na [configuração de event source mappings SQS](https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-configure.html).
- **Falha parcial:** comportamento de retry precisa combinar o retorno da função com `ReportBatchItemFailures`; se uma invocação falha de forma geral, o lote pode voltar. A decisão e evidência devem considerar as [regras de falha parcial para SQS/Lambda](https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-errorhandling.html).
- **Rede:** para alcançar o RDS privado, uma etapa futura precisa associar a Lambda à VPC e liberar somente a origem Lambda apropriada até o security group do RDS na porta definida. O runtime também precisa de um caminho autorizado para ler o secret; comparar endpoint de interface de Secrets Manager e rota de saída, com custos e policies.
- **Persistência:** o segredo master é de administração. Definir separadamente credencial/role de aplicação, schema e migrações. A decisão de consistência, concorrência e idempotência pertence à defesa I0 e não é resolvida aqui.
- **Parâmetros:** não copiar números de exemplo sem justificar workload. A documentação AWS recomenda relacionar visibility timeout ao timeout da função e ao retry; revalidar recomendações e limites antes da implementação.
- **State compartilhado:** revisar o plano Terraform para garantir escopo e dependências; aplicar mudanças incrementais somente com aprovação específica. Um destroy no root pode remover fila, DLQ, Lambda e RDS.

## Questões para a defesa I0

1. O que constitui um efeito financeiro confirmado, e qual estado do PostgreSQL é a evidência?
2. Como o desenho responderá à redelivery do mesmo `event_id`, a duas execuções concorrentes e a uma queda depois do commit?
3. O que deve acontecer com itens válidos e inválidos no mesmo lote, e como a fila saberá quais podem ser removidos?
4. Quais falhas vão para retry e quais para DLQ? Quem pode inspecionar e redrivear, e com quais controles?
5. Como o modelo de rede permitirá somente o tráfego necessário e como o runtime obterá sua credencial sem usar o master?
6. Quais valores de timeout, visibility timeout, batch, concorrência e retenção cabem na carga e no teto de custo?

Estas são perguntas e critérios de avaliação, não uma resposta de referência. O contrato canônico e seus gates permanecem em [ED-05 U2 AWS](../../docs/ed05-u2-aws.md), incluindo AWS-01–AWS-07. A sessão U2.1 continua exigindo autorização própria e não começa por este documento.
