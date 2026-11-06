-- Reforça integridade de domínio e correspondência entre evento e efeito.
BEGIN;

ALTER TABLE lab01.accounts
    ADD CONSTRAINT accounts_balance_precision_ck
    CHECK (
        saldo_atual > '-Infinity'::numeric
        AND saldo_atual < 'Infinity'::numeric
        AND saldo_atual = trunc(saldo_atual, 2)
    );

ALTER TABLE lab01.inbound_events
    ADD CONSTRAINT inbound_events_operation_ck
        CHECK (operation IN ('CREDIT', 'DEBIT')),
    ADD CONSTRAINT inbound_events_amount_ck
        CHECK (
            amount > 0
            AND amount < 'Infinity'::numeric
            AND amount = trunc(amount, 2)
        ),
    ADD CONSTRAINT inbound_events_currency_ck
        CHECK (currency = 'BRL'),
    ADD CONSTRAINT inbound_events_status_ck
        CHECK (status_evento IN ('RECEIVED', 'PROCESSED')),
    ADD CONSTRAINT inbound_events_business_key
        UNIQUE (event_id, account_id, operation, amount, currency);

ALTER TABLE lab01.transactions
    ALTER COLUMN operacao SET NOT NULL,
    ADD CONSTRAINT transactions_operation_ck
        CHECK (operacao IN ('CREDIT', 'DEBIT')),
    ADD CONSTRAINT transactions_amount_ck
        CHECK (
            valor > 0
            AND valor < 'Infinity'::numeric
            AND valor = trunc(valor, 2)
        ),
    ADD CONSTRAINT transactions_currency_ck
        CHECK (currency = 'BRL');

ALTER TABLE lab01.transactions
    DROP CONSTRAINT transactions_inbound_events_fk,
    ADD CONSTRAINT transactions_inbound_events_fk
        FOREIGN KEY (event_id, account_id, operacao, valor, currency)
        REFERENCES lab01.inbound_events
            (event_id, account_id, operation, amount, currency);

COMMIT;
