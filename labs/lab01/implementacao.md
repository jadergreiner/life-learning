## Roteiro — U1

**Etapa 1: desenho independente (I0).** Antes do código, documente:

- quais tabelas e restrições serão necessárias;
- limites das transações;
- como tratar concorrência e reentregas;
- quais invariantes serão verificadas.

## DDL atual do PostgreSQL

O DDL abaixo foi extraído do schema `lab01` do banco `pipeline_financeiro` em 05/11/2026, após confirmar no catálogo do PostgreSQL a remoção da unicidade de `transactions.account_id`.

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

### Divergências a resolver

- As duas FKs de `transactions` usam a coluna `id`; nenhuma FK usa `account_id`, e não há coluna separada em `transactions` para referenciar `inbound_events.id`.
- As colunas `id` não têm `DEFAULT`/`IDENTITY` no DDL atual, então o banco não gera esses valores automaticamente.

Este bloco documenta a estrutura atual confirmada no banco. As FKs e a geração dos IDs ainda precisam ser corrigidas antes dos testes de concorrência e reentrega.
