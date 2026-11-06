## Roteiro — U1

**Etapa 1: desenho independente (I0).** Antes do código, documente:

- quais tabelas e restrições serão necessárias;
- limites das transações;
- como tratar concorrência e reentregas;
- quais invariantes serão verificadas.

## DDL antes do ajuste do schema

O DDL abaixo é o snapshot anterior à migração, extraído do schema `lab01` do banco `pipeline_financeiro` em 05/11/2026. Na ocasião, também foi confirmada no catálogo a remoção da unicidade de `transactions.account_id`.

```sql
CREATE SCHEMA lab01;

CREATE TABLE lab01.accounts (
    id integer NOT NULL,
    account_id character varying NOT NULL,
    saldo_atual numeric NOT NULL,
    CONSTRAINT accounts_pk PRIMARY KEY (id),
    CONSTRAINT accounts_unique UNIQUE (account_id)
);

CREATE TABLE lab01.inbound_events (
    event_id character varying NOT NULL,
    account_id character varying NOT NULL,
    operation character varying NOT NULL,
    amount numeric NOT NULL,
    currency character varying NOT NULL,
    status_evento character varying NOT NULL,
    id integer NOT NULL,
    CONSTRAINT inbound_events_pk PRIMARY KEY (id),
    CONSTRAINT inbound_events_unique UNIQUE (event_id)
);

CREATE TABLE lab01.transactions (
    id integer NOT NULL,
    account_id character varying NOT NULL,
    event_id character varying NOT NULL,
    valor numeric NOT NULL,
    operacao character varying,
    currency character varying NOT NULL,
    CONSTRAINT transactions_pk PRIMARY KEY (id),
    CONSTRAINT transactions_unique_1 UNIQUE (event_id),
    CONSTRAINT transactions_accounts_fk
        FOREIGN KEY (id) REFERENCES lab01.accounts (id),
    CONSTRAINT transactions_inbound_events_fk
        FOREIGN KEY (id) REFERENCES lab01.inbound_events (id)
);
```

### Alteração aplicada

```sql
ALTER TABLE lab01.transactions
    DROP CONSTRAINT IF EXISTS transactions_unique;
```

O comando foi executado pelo usuário em 05/11/2026. A constraint removida era `UNIQUE (account_id)`, que impedia mais de uma transação por conta. A consulta ao catálogo confirmou que `transactions_unique` não existe mais.

### Colunas presentes

| Tabela | Colunas |
|---|---|
| `accounts` | `id`, `account_id`, `saldo_atual` |
| `inbound_events` | `event_id`, `account_id`, `operation`, `amount`, `currency`, `status_evento`, `id` |
| `transactions` | `id`, `account_id`, `event_id`, `valor`, `operacao`, `currency` |

### Divergências encontradas antes da migração

- As duas FKs de `transactions` usam a coluna `id`; nenhuma FK usa `account_id`, e não há coluna separada em `transactions` para referenciar `inbound_events.id`.
- As colunas `id` não tinham `DEFAULT`/`IDENTITY` no DDL pré-migração, então o banco não gerava esses valores automaticamente.

Este bloco registra o estado anterior à migração, não o schema atual.

## Implementação da aplicação

O código em `src/` separa configuração, conexão, unidade de trabalho, repositórios e caso de uso:

- `src/config/settings.py` carrega configurações `DB_*` do ambiente ou de `.env`.
- `src/database/connection.py` mantém o engine e cria sessões transacionais.
- `src/database/transaction.py` agrupa repositórios numa unidade de trabalho.
- `src/repositories/` concentra SQL parametrizado para contas, eventos recebidos e transações.
- `src/services/event_processor.py` valida e coordena o processamento idempotente.
- `src/main.py` aceita um payload JSON em argumento para execução local.

O registro do efeito usa `INSERT ... ON CONFLICT (event_id) DO NOTHING`; somente o worker que inserir a transação atualiza o saldo. O saldo é alterado com uma única instrução `UPDATE saldo_atual = saldo_atual + ...`, evitando lost update entre eventos diferentes da mesma conta. As operações compartilham uma transação e sofrem rollback juntas.

### Preparação e execução

Na pasta `labs/lab01`, instale as dependências com `py -m pip install -r requirements.txt`. Copie `.env.example` para `.env` e ajuste as variáveis `DB_*` ao ambiente local. Não versione o arquivo `.env`.

Em 05/11/2026, `migrations/001_align_lab01_schema.sql` foi aplicada ao banco `pipeline_financeiro`. Antes da aplicação, foi verificado que as três tabelas estavam vazias. A consulta posterior ao catálogo confirmou geração `IDENTITY BY DEFAULT` para os três IDs e as FKs `inbound_events.account_id → accounts.account_id`, `transactions.account_id → accounts.account_id` e `transactions.event_id → inbound_events.event_id`.

Para processar o evento de um arquivo JSON: `py -m src.main .\evento.json`. Para passar JSON direto: `py -m src.main '{"event_id":"EVT-123","account_id":"ACC-001","operation":"CREDIT","amount":"100.00","currency":"BRL"}'`.

O script `teste_db.py` verifica apenas a conectividade e a execução de `SELECT 1`; ele não aplica migrações nem comprova os cenários de idempotência e concorrência.

## Desenho arquitetural — U1, Etapa 1 (I0)

Este registro foi escrito depois da implementação inicial. Ele explicita o desenho que deve orientar a revisão do código e os ensaios; não comprova que a etapa de desenho foi concluída antes da codificação.

### Modelo de dados e restrições

- `accounts`: uma linha por conta; `id` como chave primária técnica, `account_id` único e saldo em tipo decimal (`NUMERIC(18,2)`). O saldo pode ser atualizado em concorrência sem perder alterações. O enunciado não define política de saldo negativo, portanto não se adiciona restrição de não negatividade sem decisão de negócio.
- `inbound_events`: registro durável do evento recebido; `id` como chave primária, `event_id` único globalmente, referência à conta, operação, valor, moeda e estado. Restringir operação a `CREDIT`/`DEBIT`, valor a positivo, moeda aceita a `BRL` nesta U1 e estado a `RECEIVED`/`PROCESSED`.
- `transactions`: livro dos efeitos aplicados; `id` como chave primária, `event_id` único, referência à conta e ao evento recebido, valor, operação e moeda. Não deve haver unicidade em `account_id`, pois uma conta pode ter várias transações.
- IDs técnicos são gerados pelo PostgreSQL. As FKs ligam `inbound_events.account_id` e `transactions.account_id` a `accounts.account_id`, e `transactions.event_id` a `inbound_events.event_id`. A aplicação também valida que os atributos de uma reentrega com o mesmo `event_id` correspondem ao evento original; conteúdo divergente é conflito, não duplicata válida.
- Valores monetários entram como string decimal, são convertidos para `Decimal` e persistidos como `NUMERIC`; não usar `float`.

### Limite e fluxo da transação

Uma transação PostgreSQL corresponde ao processamento de um evento: inserir ou validar `inbound_events`; tentar inserir `transactions`; atualizar o saldo somente se a inserção da transação venceu; marcar o evento como `PROCESSED`; então fazer commit. Falha em qualquer etapa antes do commit deve reverter todas as alterações desse evento. Não há chamadas externas dentro desta transação.

### Concorrência e reentregas

- Mesmo `event_id` em workers concorrentes: a unicidade no banco decide o vencedor da inserção em `transactions`. Só o worker que inserir a linha aplica a variação ao saldo; o outro identifica o conflito idempotente e não reaplica o efeito.
- Eventos distintos para a mesma conta: atualizar com uma operação SQL atômica (`saldo_atual = saldo_atual + delta`). O bloqueio de linha do PostgreSQL serializa as alterações daquele saldo sem lost update; não fazer leitura-modificação-escrita em Python.
- Falha antes do commit: rollback integral; uma reentrega pode tentar de novo.
- Commit concluído, mas resposta perdida: a reentrega encontra o `event_id` já aplicado e não repete a atualização do saldo.
- Mesmo `event_id` com conta/operação/valor/moeda diferentes: rejeitar como conflito de conteúdo e preservar o registro original.

### Invariantes e evidências requeridas

1. Existe no máximo um efeito em `transactions` por `event_id`.
2. Um evento sem transação confirmada não altera o saldo.
3. A transação e sua atualização de saldo são confirmadas ou revertidas juntas.
4. Para cada evento aplicado, o saldo muda exatamente por `+amount` em crédito ou `-amount` em débito.
5. Reentregar um evento confirmado não altera o saldo; conteúdo divergente com o mesmo ID não é aceito.
6. Processar eventos distintos em paralelo para a mesma conta produz o mesmo saldo que sua aplicação sequencial.
7. Valores têm precisão decimal de centavos e não usam ponto flutuante binário.

As constraints do schema cobrem PKs, unicidade de `account_id`/`event_id`, geração de IDs, precisão decimal, operações e moedas aceitas, estados de evento e correspondência entre evento e transação. Não foi adicionada regra de saldo não negativo porque a política de cheque especial não está definida. Os itens acima são critérios de projeto; os ensaios T01–T07 e os testes de schema foram executados no ambiente local do Compose.

## Etapa 1 — camada HTTP da API

A API FastAPI está em `src/api/`. `POST /events` valida o contrato HTTP e delega o processamento ao `EventProcessor`; `GET /accounts/{account_id}/balance` consulta o saldo; `/health/live` verifica o processo e `/health/ready` verifica o PostgreSQL. `INSTANCE_ID` é exposto no cabeçalho `X-Instance-ID` para identificar qual instância respondeu. O valor monetário deve ser enviado como string decimal com até duas casas. A API responde somente após o caso de uso concluir a transação.

### Conferência local desta etapa

1. Em `labs/lab01`, instale as dependências: `py -m pip install -r requirements.txt`.
2. Inicie a API: `py -m uvicorn src.api.app:app --host 127.0.0.1 --port 8000`.
3. Em outro terminal, consulte `Invoke-WebRequest http://127.0.0.1:8000/health/live`; esperado HTTP 200 e `X-Instance-ID: local`.
4. Consulte `Invoke-RestMethod http://127.0.0.1:8000/health/ready`; esperado `status=ready` e `database=ready`.
5. Abra `http://127.0.0.1:8000/docs` e confira os endpoints `POST /events`, `GET /accounts/{account_id}/balance` e as duas rotas de health.
6. Interrompa a API com Ctrl+C. O lifespan fecha o pool de conexões da instância.

Nesta etapa não foram enviados eventos financeiros; a validação HTTP de payloads inválidos e as rotas de saúde não alteram o saldo. A infraestrutura Docker é descrita e conferida na etapa seguinte.

## Etapa 2 — ambiente Docker Compose

O `Dockerfile` cria a imagem da API. `docker-compose.yml` inicia PostgreSQL 16 e duas instâncias do mesmo serviço, configuradas com `INSTANCE_ID=A/B`. Ambas usam `DB_HOST=postgres` e compartilham o volume nomeado `postgres_data`. As portas da API ficam limitadas ao host local (`127.0.0.1:8001` e `127.0.0.1:8002`); PostgreSQL é publicado apenas em `127.0.0.1:5433`, separado da porta 5432 do banco local no host. A imagem PostgreSQL 16 foi escolhida por continuar em suporte oficial até novembro de 2028.

As credenciais padrão `pipeline/pipeline` são somente para este ambiente local isolado; Compose aceita substituí-las por `DB_USER` e `DB_PASSWORD` do ambiente ou do arquivo `.env`.

Para conectar ao PostgreSQL do Compose pelo DBeaver, use host `127.0.0.1`, porta `5433`, banco `pipeline_financeiro`, usuário `pipeline` e a senha definida por `DB_PASSWORD` (padrão local: `pipeline`). Se SSL estiver configurado como obrigatório no cliente, desative-o para esta conexão local.

Em um volume vazio, `docker/init/001_schema.sql` inicializa o schema `lab01` e cria `ACC-001` com saldo inicial de R$ 200,00. O script é executado pelo entrypoint oficial do PostgreSQL somente na inicialização de um diretório de dados vazio. Reiniciar os serviços preserva os dados no volume; alteração desse script não migra um volume já inicializado.

### Conferência da infraestrutura Docker

1. Na pasta `labs/lab01`, valide a composição com `docker compose config`.
2. Construa e inicie os serviços com `docker compose up --build -d`.
3. Confirme `postgres`, `api_a` e `api_b` saudáveis com `docker compose ps`.
4. Consulte `http://127.0.0.1:8001/health/ready` e `http://127.0.0.1:8002/health/ready`; ambas devem retornar `ready`.
5. Consulte `/health/live` em cada porta e confira `X-Instance-ID: A` na porta 8001 e `X-Instance-ID: B` na porta 8002.
6. Consulte `/accounts/ACC-001/balance` nas duas instâncias; ambas devem mostrar `200.00` antes dos ensaios de processamento.
7. Use `docker compose logs --tail=100 api_a api_b postgres` para revisar inicialização e erros.

Verificação realizada em 05/11/2026: `docker compose config` válido; os três containers iniciaram saudáveis; liveness/readiness responderam em A e B, com IDs distintos; ambas leram o saldo inicial de R$ 200,00 do banco compartilhado. Nenhum evento financeiro foi enviado nesta conferência.

## Etapa 3 — ensaios de aceitação T01–T07

`tests/test_event_processing.py` contém cinco testes de integração que cobrem os sete critérios: cenário normal e dez reentregas (T01–T03), dois workers para o mesmo evento (T04), exceção injetada antes do commit e rollback (T05), repetição após commit simulando resposta perdida (T06) e eventos distintos paralelos na mesma conta (T07). Cada teste cria uma conta temporária com UUID e a remove junto com seus eventos e transações ao final.

O serviço `test_runner`, habilitado pelo profile `test`, executa a suíte dentro da rede Compose. Ele aguarda PostgreSQL e as duas APIs saudáveis e alcança as instâncias pelos nomes `api_a` e `api_b`.

### Conferência dos ensaios

1. Confirme que os serviços estão ativos: `docker compose ps`.
2. Execute `docker compose --profile test run --build --rm test_runner`.
3. Esperado: cinco testes aprovados (`5 passed`), cobrindo T01–T07.
4. Confira `docker compose ps` para garantir que PostgreSQL e as APIs continuam saudáveis.
5. Confira a limpeza consultando a quantidade de contas `TST-%` no banco; esperado zero. O saldo de `ACC-001` deve permanecer R$ 200,00.

Verificação realizada em 05/11/2026: `docker compose --profile test config` válido; a suíte retornou `5 passed in 0.71s`; após a execução, não restaram contas temporárias e `ACC-001` permaneceu em R$ 200,00. Os containers da aplicação e do banco continuaram saudáveis.

## Etapa 4 — constraints de domínio no PostgreSQL

`migrations/002_domain_constraints.sql` adiciona CHECKs para operação (`CREDIT`/`DEBIT`), valor positivo com até duas casas decimais, moeda `BRL`, estados `RECEIVED`/`PROCESSED` e saldo finito com precisão de centavos. `transactions.operacao` passa a ser obrigatória. A chave composta do evento e a FK composta da transação garantem que evento e efeito concordem em `event_id`, conta, operação, valor e moeda. Nenhuma constraint impede saldo negativo, pois essa política ainda não foi definida.

O schema de bootstrap `docker/init/001_schema.sql` já cria bancos novos com as mesmas constraints. A migração 002 foi aplicada ao banco local `pipeline_financeiro` e ao PostgreSQL do Compose. Antes da aplicação, o banco local estava vazio; no Compose havia somente a conta de demonstração `ACC-001`, sem eventos ou transações. Ambos passaram na consulta ao catálogo após a migração.

A constraint composta do evento também fez o teste de reentrega revelar que `ON CONFLICT (event_id)` não cobria a nova chave única. `InboundEventsRepository` agora usa `ON CONFLICT DO NOTHING` e compara o conteúdo persistido; a segunda execução da suíte confirmou que duplicatas idênticas passam e que T04 continua aplicando o efeito uma única vez.

### Conferência de integridade

1. Execute `docker compose --profile test run --build --rm test_runner`; esperado: `11 passed`.
2. Confirme `docker compose ps`; os três serviços devem permanecer saudáveis.
3. Consulte o catálogo do PostgreSQL para verificar `*_operation_ck`, `*_amount_ck`, `*_currency_ck`, `inbound_events_status_ck` e a FK composta `transactions_inbound_events_fk`.
4. Confirme que não restaram contas `TST-%` e que `ACC-001` segue com saldo R$ 200,00.

Verificação realizada em 05/11/2026: migração aplicada nos dois bancos; constraints confirmadas no catálogo; suíte retornou `11 passed in 0.75s`; nenhum dado de teste permaneceu e os containers continuaram saudáveis.

## Etapa 5 — contenção simultânea controlada

O T04 foi fortalecido em `tests/test_event_processing.py`. Antes das chamadas HTTP, o teste abre uma transação PostgreSQL e insere o evento sem commit, mantendo a chave única de `event_id` reservada. As requisições para `api_a` e `api_b` partem por uma barreira. O teste consulta `pg_stat_activity` e só libera a transação quando confirma que ambas estão ativas, aguardando lock do tipo `transactionid` e bloqueadas pelo PID da mesma transação que reservou o evento. Isso comprova a disputa simultânea no ponto da inserção idempotente; a barreira do cliente sozinha não faria essa comprovação.

Um segundo ensaio repete a contenção por cinco rodadas, com 12 requisições simultâneas (seis por instância) ao mesmo evento em cada rodada. Em cada rodada, uma requisição aplica o efeito e as outras 11 são idempotentes. Os testes usam contas e eventos temporários e os fixtures fazem a limpeza ao final.

### Conferência da concorrência controlada

1. Confirme os containers saudáveis com `docker compose ps`.
2. Execute `docker compose --profile test run --build --rm test_runner`.
3. A suíte atual deve retornar `12 passed`.
4. O T04 controlado exige dois backends simultaneamente bloqueados; o ensaio de carga exige 12 backends bloqueados em cada uma das cinco rodadas.
5. Confirme que não restaram contas `TST-%` e que o saldo de `ACC-001` não foi alterado pela suíte.

Verificação realizada em 05/11/2026: a suíte retornou `12 passed in 3.69s`; T04 observou os waiters esperados em todos os ensaios; os containers permaneceram saudáveis; não restaram contas de teste e `ACC-001` permaneceu em R$ 220,00, sem alteração pela suíte.
