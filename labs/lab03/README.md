# LAB03 — ED-07: SparkLens no Databricks (diagnóstico prático I0)

> **Status:** proposta de laboratório / especificação publicada; execução, testes e aprovação **pendentes**.  
> **Trilha:** Life Learning — P8 DATABRICKS; referência à sessão C17/P8 de 08/11/2026.  
> **Competência:** ED-07 — Lakehouse, Delta Lake e operação de pipelines Databricks.  
> **Caso de uso:** [SparkLens](https://github.com/jadergreiner/SparkLens).  
> **Fonte da verdade pedagógica:** [Notion — configuração do Life Learning](https://app.notion.com/p/3d402f2729f981c88688f3acb9ba7b20) e [sessão C17/P8](https://app.notion.com/p/41202f2729f98164b90fd1a01bcd88fa).  
> **Regra:** este documento não constitui gate de aprovação do Conselho. Não provisionar recursos sem autorização.

## 1. Problema

O SparkLens compara duas execuções de um pipeline Spark e identifica variações de desempenho por execução e stage. A ingestão de métricas pode receber duplicatas, reentregas, versões atrasadas, payloads inválidos e gravações concorrentes. Precisamos preservar o histórico observável e publicar um estado coerente para comparações reproduzíveis.

**Diferença essencial:** PySpark + Delta Lake local é uma base portável, mas não comprova competência na **plataforma Databricks**. Este laboratório possui uma preparação local opcional e um gate específico de execução e operação no Databricks.

## 2. Objetivos de aprendizagem verificáveis

| ID | Objetivo | Evidência necessária |
|---|---|---|
| OBJ-01 | Modelar métricas de workflows, stages, eventos e versões | Esquema, chaves, contrato versionado e justificativa |
| OBJ-02 | Implementar ingestão rastreável e validação do contrato | Código, linhas aceitas/rejeitadas, logs e testes |
| OBJ-03 | Publicar CURRENT idempotente em Delta | Código MERGE/estratégia equivalente e testes de replay |
| OBJ-04 | Impedir regressão de versão e tratar conflitos | Testes de eventos fora de ordem e versões iguais divergentes |
| OBJ-05 | Demonstrar execução efetiva no Databricks | Run do notebook/job, runtime, tabelas e resultados |
| OBJ-06 | Aplicar governança pelo Unity Catalog | Objetos catalog.schema.table e evidências de permissões |
| OBJ-07 | Operar com Databricks Workflows | Job, task dependencies, parâmetros, falha/retry e run IDs |
| OBJ-08 | Defender trade-offs, limites e recuperação | ADR curta e defesa sobre concorrência, qualidade, custo e replay |

## 3. Escopo e ambientes

### U0 — Preparação local (apoio, não equivale à aprovação Databricks)

- Montar ambiente reprodutível com Python, PySpark, Delta Lake e pytest, com versões efetivamente utilizadas registradas.
- Criar dataset **inteiramente sintético** e testes locais de contrato, reprocessamento e late arrivals.
- Não usar cloud, credenciais, dados bancários, PII ou logs reais.
- **Gate U0:** testes locais demonstrados. O sucesso em U0 **não** atende OBJ-05 a OBJ-07.

### U1 — Databricks (núcleo da P8)

- Executar o mesmo pipeline num **workspace autorizado**, documentando versão do Databricks Runtime, compute e configuração relevante.
- Criar tabelas Delta governadas no Unity Catalog, conforme permissões e nomenclaturas disponíveis.
- Implementar um workflow reproduzível, com etapas de ingestão, validação, publicação e verificação.
- Demonstrar execução feliz, falha controlada, retentativa e inspeção de métricas/logs.
- Registrar impacto/custo aproximado somente com dados reais de execução disponíveis. Desligar recursos autorizados ao final.
- **Gate U1:** evidências concretas de Databricks e revisão técnica; não presumir aprovação por screenshots isolados.

## 4. Requisitos funcionais

| ID | Requisito | Critério de aceitação |
|---|---|---|
| RF-01 | Ingerir eventos com identificação do workflow, stage, evento e versão | Dataset de exemplo ingressa sem perda silenciosa; contagem auditável |
| RF-02 | Persistir RAW append-only ou histórico equivalente | Reentregas ficam rastreáveis com timestamp de ingestão, payload/hash e status |
| RF-03 | Validar snapshot completo e campos obrigatórios | Registros inválidos não chegam ao CURRENT e ficam diagnosticáveis |
| RF-04 | Atualizar CURRENT por chave lógica | Uma linha vigente por chave, sempre com a maior versão **válida** |
| RF-05 | Reprocessar eventos idênticos | Estado publicado não se altera após replay idêntico |
| RF-06 | Processar versões fora de ordem | V8 válida não é substituída por V7 atrasada |
| RF-07 | Tratar mesma versão com payload conflitante | Política explícita e testada (rejeitar/quarentenar; nunca desempatar arbitrariamente) |
| RF-08 | Permitir comparação de duas execuções SparkLens | Saída reproduzível de diferenças de duração por stage, com chaves e unidades |
| RF-09 | Expor falhas com contexto suficiente | Mensagem/estado com motivo, etapa, run ID, identificação do lote e sem segredos |
| RF-10 | Executar e reexecutar no Databricks Workflows | Run inicial e rerun comprovados; política de retry descrita |
| RF-11 | Restringir acesso por Unity Catalog | Prova de objetos e permissões com identificadores sensíveis mascarados |

**Contrato inicial de evento (proposto; o estudante valida e documenta hipóteses):**

```json
{
  "event_id": "evt-0042",
  "workflow_run_id": "workflow-A",
  "stage_run_id": "stage-02",
  "source_version": 8,
  "schema_version": 1,
  "event_time": "2026-11-08T18:10:00Z",
  "duration_ms": 1420
}
```

Chave lógica proposta: `(workflow_run_id, stage_run_id)`. `event_id` identifica o evento de origem. Versões são comparáveis **por chave lógica**. `event_time` não substitui `source_version` como autoridade de precedência. `duration_ms` deve ser inteiro não negativo; campos obrigatórios não podem ser nulos. Atualização parcial é inválida enquanto o contrato exigir snapshot completo.

## 5. Requisitos não funcionais e invariantes

- **RNF-01 — Correção:** o CURRENT não pode regredir de V8 válida para V7, independentemente da ordem de chegada.
- **RNF-02 — Idempotência:** reexecução com os mesmos eventos preserva o estado publicado, evitando efeitos duplicados.
- **RNF-03 — Auditabilidade:** rejeições, eventos recebidos e decisões de atualização permitem investigar o resultado.
- **RNF-04 — Atomicidade:** a decisão de publicar e a gravação precisam respeitar a transação Delta; leituras de pré-validação separadas não são garantia contra corrida (TOCTOU).
- **RNF-05 — Concorrência:** descrever controle de concorrência otimista, conflitos e retry com reavaliação do estado. Se forem empregados leases/tokens, distinguir expiração, autorização atual e fencing; não atribuir à plataforma garantias não demonstradas.
- **RNF-06 — Segurança:** dados sintéticos, privilégios mínimos e ausência de credenciais, tokens e nomes privados em logs/commits.
- **RNF-07 — Reprodutibilidade:** documentar dependências, versão do runtime, entradas, comandos, parâmetros e critérios de comparação.
- **RNF-08 — Operabilidade:** falhas não podem ser silenciosas; documentar monitoramento, retries e procedimento de replay/reconciliação.
- **RNF-09 — Custos:** não provisionar nem manter compute sem autorização; registrar limpeza e custo verificado quando aplicável.

## 6. Cenários de teste obrigatórios

| ID | Cenário | Resultado esperado |
|---|---|---|
| T01 | Primeira versão válida de uma chave | Inserção no CURRENT |
| T02 | Mesmo evento reentregue | Nenhuma alteração indevida no CURRENT |
| T03 | V7 chega após V8 válida | CURRENT continua V8 |
| T04 | V9 inválida após V8 válida | CURRENT continua V8; V9 diagnosticável |
| T05 | V8 repetida com payload divergente | Conflito detectado conforme política, sem sobrescrita silenciosa |
| T06 | Campo obrigatório ausente | Quarentena/rejeição rastreável |
| T07 | Duração negativa/tipo inválido | Rejeição com motivo |
| T08 | Dois writers com versões diferentes | Sem regressão após conflito, independentemente da ordem de commit |
| T09 | Falha após commit e antes de confirmação ao orquestrador | Retry/replay preserva estado |
| T10 | Comparação de duas execuções com stages ausentes | Contrato de diferença/ausência explicitado e testado |
| T11 | Falha programada de task Workflows | Estado de erro, logs, retry e comportamento observado |
| T12 | Reexecução integral no workspace | Resultados finais determinísticos, salvo metadados auditáveis de ingestão |

**Nota:** testes de concorrência precisam exercer writers/transações sobre estado compartilhado; simulação sequencial isolada não é prova de corrida. Quando um comportamento não puder ser reproduzido, registrar como lacuna e não como teste aprovado.

## 7. Entregáveis e estrutura sugerida

```text
labs/lab03/
  README.md                  # Este descritivo
  EVIDENCIAS.md              # Preencher somente após execução
  data/                      # Eventos sintéticos
  src/                       # Ingestão, validação e publicação
  tests/                     # Testes positivos e adversos
  databricks/                # Notebooks e definições do job, quando autorizado
  adr/                       # Decisões/trade-offs observados
```

Nesta publicação, **somente o descritivo** foi especificado. Os diretórios e entregáveis adicionais são tarefas futuras; não devem ser apresentados como já existentes.

### Evidências mínimas por execução

Preencher futuramente `EVIDENCIAS.md` com:

- **Identificação:** data, commit/PR, autor, fase U0 ou U1, estado (planejado/executado/revisado).
- **Ambiente:** versões efetivas, dependências, configuração e referências de execução.
- **Entrada:** arquivos/dataset sintético e contagens esperadas.
- **Comandos e execução:** instruções reprodutíveis, links de job/run/notebook quando existirem.
- **Saída:** contagens RAW/validação/CURRENT, exemplo de comparação entre execuções.
- **Testes:** tabela T01–T12 com status PASS/FAIL/BLOCKED/NOT RUN, comando e log resumido.
- **Falhas e correções:** hipótese, reprodução, alteração realizada, novo resultado.
- **Segurança e custo:** evidência de permissões UC, remoção de recursos e valores reais quando disponíveis.
- **Defesa técnica:** argumentos sobre versões, concorrência Delta, retries, governança e limitações.
- **Revisão do Conselho:** pareceres de Helena (aprendizagem), Fernanda (correção), Marcelo (impacto) e Ricardo (portabilidade), com discordâncias e decisão datada — somente após apreciação.

## 8. Critérios para gate de avaliação

1. Artefatos de implementação e evidências distinguem trabalho **independente I0** de orientação assistida.
2. RF-01 a RF-09 e T01 a T10 têm resultado verificável ou falha/lacuna explicitamente justificada.
3. Para caracterizar domínio **Databricks**, RF-10/RF-11 e T11/T12 exigem prova específica da plataforma.
4. Correção de dados, atomicidade e segurança são critérios impeditivos; um pipeline que apenas executa não basta.
5. A defesa técnica deve identificar trade-offs e riscos residuais a partir do código e dos testes efetivamente produzidos.
6. O Conselho delibera sobre suficiência das evidências **antes** de qualquer mudança de conteúdo/competência. Entrega do laboratório ≠ competência consolidada.
7. A cadência vigente de **oito posições** e o histórico do Notion não são alterados por este arquivo.

## 9. Primeira atividade independente (I0)

**Começar pequeno:** com um lote sintético contendo V6, V8 e V7 atrasada para a mesma chave, entregar implementação RAW + CURRENT e testes T01/T03. Em seguida adicionar duplicatas, invalidez, concorrência e operação Databricks progressivamente.

A orientação deve incidir sobre código, logs ou bloqueios reais. Evitar rodadas intermináveis de perguntas conceituais. Não antecipar a solução antes da primeira implementação independente.

## 10. Referências

- [Delta Lake — documentação oficial](https://docs.delta.io/latest/index.html)
- [Delta Lake — controle de concorrência](https://docs.delta.io/latest/concurrency-control.html)
- [Databricks — documentação oficial](https://docs.databricks.com/)
- [Unity Catalog — documentação Databricks](https://docs.databricks.com/aws/en/data-governance/unity-catalog/)
- [Lakeflow Jobs / Databricks Workflows](https://docs.databricks.com/aws/en/jobs/)
- [Life Learning — contrato de fontes](../../docs/sources-of-truth.md)

**Registro de especificação:** 08/11/2026. **Não implica execução, aprovação, provisionamento ou sincronização automática entre sistemas.**
