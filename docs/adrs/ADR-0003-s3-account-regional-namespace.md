# ADR-0003 — Namespace account-regional para o bucket de teste

- Status: Proposto
- Data: 2026-11-07
- SDD: SDD-0001

## Contexto

O bucket é temporário. Nomes no namespace global podem colidir com outras contas e ficar disponíveis para reuso depois de removidos.

## Decisão

Usar o namespace `account-regional` suportado pelo AWS Provider, derivando o nome a partir de um prefixo configurável, da conta e da região `us-east-1`.

## Consequências

- O namespace reduz colisões entre contas e o risco de reuso global.
- Ainda podem existir colisões dentro da mesma conta/região.
- O namespace não concede permissões; a identidade IAM continua sendo pré-requisito.
- O nome não é segredo nem identidade permanente, pois outros principais da conta podem reutilizá-lo após o destroy.
