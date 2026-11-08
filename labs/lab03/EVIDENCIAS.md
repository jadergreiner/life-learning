# LAB03 — Registro de evidências (ED-07 / SparkLens)

> **Estado inicial:** `NOT RUN`. Este é um formulário de coleta, não é prova de execução.  
> **Referência de requisitos:** [README.md](README.md).  
> **Contexto:** Life Learning C17/P8, competência ED-07, diagnóstico I0.  
> **Fonte de verdade dos resultados e da avaliação:** Notion.

## 1. Identificação da entrega

| Campo | Preenchimento |
|---|---|
| Data e responsável | PENDENTE |
| Etapa | U0 Local / U1 Databricks |
| Tipo de execução | I0 independente / assistida |
| Commit e PR do código | PENDENTE |
| ID de execução / Job run | PENDENTE |
| Status geral | NOT RUN |

**Não registrar credenciais, tokens, PII ou identificadores privados neste repositório público.** Redigir/mascarar os identificadores de workspace quando necessário.

## 2. Ambiente reproduzível

| Informação | Valor efetivamente observado |
|---|---|
| Python | NOT RUN |
| PySpark | NOT RUN |
| Delta Lake | NOT RUN |
| Databricks Runtime (U1) | NOT RUN |
| Compute e configuração (U1) | NOT RUN |
| Unity Catalog (catálogo/schema, U1) | NOT RUN |
| Versões de dependências e lockfile | NOT RUN |
| Comandos para instalar e executar | NOT RUN |

## 3. Contrato, entradas e saídas

- Dataset sintético e hash/commit: **PENDENTE**
- Chaves de workflow/stage, id de evento, versão e event time: **PENDENTE**
- Contagem de eventos recebidos / válidos / inválidos: **PENDENTE**
- RAW: localização lógica, política de retenção, entradas rejeitadas: **PENDENTE**
- CURRENT: chaves, versões finais e contagem: **PENDENTE**
- Comparação entre execuções: amostras de saída e diferença de duração: **PENDENTE**
- Contrato de versão igual com payload divergente: **PENDENTE**

## 4. Evidência dos testes

Marcar somente depois de executar; anexar comando/log ou link por teste. Não converter `NOT RUN` em `PASS` com base em expectativa.

| Teste | Cenário | Status | Comando / log / commit |
|---|---|---|---|
| T01 | Primeira versão válida | NOT RUN | — |
| T02 | Reentrega idêntica | NOT RUN | — |
| T03 | V7 após V8 | NOT RUN | — |
| T04 | Versão superior inválida | NOT RUN | — |
| T05 | Mesma versão, payload divergente | NOT RUN | — |
| T06 | Campo obrigatório ausente | NOT RUN | — |
| T07 | Duração inválida | NOT RUN | — |
| T08 | Writers concorrentes | NOT RUN | — |
| T09 | Retry após commit | NOT RUN | — |
| T10 | Stages ausentes na comparação | NOT RUN | — |
| T11 | Falha e retry em Workflows (U1) | NOT RUN | — |
| T12 | Reexecução determinística no Databricks (U1) | NOT RUN | — |

**Valores permitidos:** `PASS`, `FAIL`, `BLOCKED`, `NOT RUN`.  
Para T08, informar se houve verdadeira concorrência em estado compartilhado; teste apenas sequencial não comprova segurança concorrente.

## 5. Evidência específica de Databricks (U1)

- Notebook ou repositório associado ao workspace: **PENDENTE**
- Job/Workflow: task graph, parâmetros, política de retry: **PENDENTE**
- IDs/links de runs, com dados sensíveis mascarados: **PENDENTE**
- Unity Catalog: objetos, permissões efetivas, controles testados: **PENDENTE**
- Logs de execução e falha controlada: **PENDENTE**
- Custo observado, se disponível, e limpeza de compute: **PENDENTE**

**Nota:** execução local de Spark/Delta não substitui esta seção.

## 6. Registro de investigação

| Problema / hipótese | Como foi reproduzido | Ajuste | Resultado reexecutado |
|---|---|---|---|
| PENDENTE | PENDENTE | PENDENTE | NOT RUN |

## 7. Defesa técnica do estudante

Responder com base em código e testes próprios, após a implementação:

1. Qual invariante impede regressão de versão? Que teste demonstra?
2. Como a transação Delta trata validação, commit, conflito e retry?
3. O que acontece quando uma versão maior é inválida ou tem schema incompatível?
4. O que realmente comprova idempotência sob replay e reentrega?
5. Qual diferença observável entre U0 Local e U1 Databricks?
6. Como reproduzir uma falha de Workflow e verificar o resultado sem efeitos duplicados?

## 8. Gate do Conselho (não preenchido antecipadamente)

| Perspectiva | Parecer e evidência | Estado |
|---|---|---|
| Helena — aprendizagem/autonomia | PENDENTE | NÃO AVALIADO |
| Fernanda — implementação, dados e testes | PENDENTE | NÃO AVALIADO |
| Marcelo — valor de produto e comunicação | PENDENTE | NÃO AVALIADO |
| Ricardo — portabilidade e tecnologia | PENDENTE | NÃO AVALIADO |
| Mediador — divergências, decisão e data | PENDENTE | NÃO DELIBERADO |

**Definição de pronto:** execução e evidências rastreáveis, qualidade de dados e segurança comprovadas, defesa analisada e decisão formal registrada no Notion. Não presumir aprovação pela existência deste documento.

## 9. Referências

- [LAB03 — requisitos e cenários](README.md)
- [Life Learning — fontes de verdade](../../docs/sources-of-truth.md)
- [Notion — sessão C17/P8](https://app.notion.com/p/41202f2729f98164b90fd1a01bcd88fa)
