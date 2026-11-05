# LAB01 — ED-05 U1 | Processador financeiro idempotente (Local)

> **Life Learning · laboratório prático experimental · I0 (desafio independente).**
> Status: **enunciado publicado; implementação e resultados não comprovados**.
> Esta atividade é **extraordinária**: não altera a cadência oficial de oito posições no Notion, não avança o ciclo e não representa aprovação permanente do método.
> Fonte da verdade para sessão e avaliação: Notion. Este repositório guarda enunciados e evidências técnicas, não substitui o histórico operacional.

## Objetivo

Projetar e implementar, **sem receber a solução pronta**, um processador de movimentações financeiras confiável diante de:
- reentregas da mesma mensagem;
- dois workers concorrentes;
- falhas antes e depois do commit;
- reprocessamento após falhas.

Este é o **primeiro** dos três ambientes obrigatórios do piloto ED-05: **Local → AWS → Databricks**. Os três laboratórios terão contratos de aprendizagem relacionados, mas não precisam replicar a mesma arquitetura. Em particular, Databricks será avaliado sob semântica de processamento analítico, e não como substituto de um sistema transacional.

## Stack e pré-requisitos

- Docker e Docker Compose;
- Python (versão compatível com as bibliotecas escolhidas);
- PostgreSQL;
- ferramenta de testes automatizados, como pytest;
- Git.

A escolha das bibliotecas, modelo das tabelas, transações, SQL e mecanismos de concorrência faz parte do desafio — **não é fornecida neste README**.

## Cenário de negócio

Saldo inicial da conta `ACC-001`: **R$ 200,00**.

| Ordem de chegada | event_id | account_id | operation | amount | Significado |
|---|---|---|---|---|---|
| 1 | EVT-123 | ACC-001 | CREDIT | 100.00 | Crédito |
| 2 | EVT-123 | ACC-001 | CREDIT | 100.00 | Reentrega do mesmo evento |
| 3 | EVT-124 | ACC-001 | DEBIT | 80.00 | Débito distinto |

**Resultado de negócio esperado: saldo R$ 220,00.** A reentrega de `EVT-123` não pode gerar segundo crédito.

Exemplo de payload (valores monetários representados como strings decimais):

```json
{
  "event_id": "EVT-123",
  "account_id": "ACC-001",
  "operation": "CREDIT",
  "amount": "100.00",
  "currency": "BRL"
}
```

## Requisitos funcionais

1. RF-01 — Validar e processar eventos financeiros válidos.
2. RF-02 — Atualizar o saldo de forma consistente com os eventos confirmados.
3. RF-03 — Impedir a reaplicação dos efeitos de um `event_id` já confirmado.
4. RF-04 — Tratar tentativas simultâneas sobre o mesmo evento e sobre a mesma conta.
5. RF-05 — Não deixar atualizações parciais quando a transação falhar antes do commit.
6. RF-06 — Permitir reentrega/reprocessamento seguro depois de falhas, inclusive quando o resultado anterior for desconhecido para o chamador.

## Requisitos não funcionais

- PostgreSQL é a fonte transacional do saldo e dos registros de processamento.
- Ambiente local reproduzível usando Docker Compose.
- Código em Python, versionado e testável.
- Testes automatizados com cenários normais e adversos.
- Log de processamento correlacionável por `event_id`, sem expor informações sensíveis.
- Proteção de integridade também no banco; não depender apenas de checagens em memória.
- Representar valores monetários sem aritmética binária de ponto flutuante.

## Roteiro — U1

**Etapa 1: desenho independente (I0).** Antes do código, documente:
- quais tabelas e restrições serão necessárias;
- limites das transações;
- como tratar concorrência e reentregas;
- quais invariantes serão verificadas.

**Etapa 2: implementação mínima.** Faça subir o ambiente, aplique migrações e execute o cenário básico.

**Etapa 3: testes adversos.** Injete duplicidades, concorrência e falhas nas fronteiras transacionais.

**Etapa 4: defesa técnica.** Explique resultados, limites e trade-offs sem depender de uma solução-modelo.

O bloco de referência é de **50 minutos**, mas o gate da unidade não é aprovado por tempo decorrido. Caso necessário, continue em nova oportunidade autorizada, sem avançar automaticamente a cadência.

## Critérios de aceitação

| ID | Ensaio | Resultado esperado |
|---|---|---|
| T01 | Aplicar EVT-123 uma vez | Saldo R$ 300,00; um efeito confirmado |
| T02 | Reentregar EVT-123 dez vezes | Saldo permanece R$ 300,00 |
| T03 | Aplicar EVT-124 depois de EVT-123 | Saldo R$ 220,00 |
| T04 | Dois workers aplicam o mesmo EVT-125 em paralelo | Um único efeito confirmado para EVT-125 |
| T05 | Exceção antes do commit | Nenhum efeito parcial persistido |
| T06 | Falha após commit, antes de confirmar ao chamador; reentrega | Nenhuma reaplicação do efeito já confirmado |
| T07 | Dois eventos distintos na mesma conta, processados em paralelo | Saldo equivalente à aplicação correta de ambos, sem lost update |

**Gate:** testes reproduzíveis, resultados demonstrados, defesa das decisões e registro das intervenções. A aprovação de T01–T03 isoladamente não comprova a confiabilidade pretendida em T04–T07.

## Evidências esperadas

A implementação poderá incluir, conforme as decisões do estudante:
- `docker-compose.yml`, `Dockerfile` e dependências;
- scripts de migração;
- código-fonte do processador e testes;
- comandos e saídas para reproduzir os testes;
- evidências de falhas simuladas;
- relato das escolhas, limitações, resultados e intervenções recebidas.

Evite incluir dados reais de clientes, credenciais ou informações internas de trabalho neste repositório público.

## Avaliação e autonomia

- **I0:** o mentor apresenta somente o problema e os critérios; você projeta e executa.
- **I1:** pergunta orientadora, sem solução.
- **I2:** pista sobre conceito ou área da falha.
- **I3:** explicação pontual ou exemplo mínimo, com reavaliação independente posterior.

Não declarar domínio N3/N4 apenas por executar um pipeline. Avaliar separadamente compreensão, implementação, diagnóstico, arquitetura/trade-offs e defesa técnica.

## Fora do escopo da U1

- Implementação completa de Transactional Outbox e integração com provedor HTTP (aprofundamento em U3).
- Provisionamento AWS (esfera seguinte).
- Processamento analítico Databricks (terceira esfera).
- Alteração da cadência, do schema do Notion ou aprovação permanente do método.

## Primeira pergunta do mentor (I0)

**Como você modelaria os dados e organizaria a transação no PostgreSQL para garantir que dois workers não consigam aplicar o mesmo evento financeiro duas vezes?**

Apresente tabelas, restrições, fluxo transacional e tratamento de concorrência. Não há implementação de referência neste enunciado.

## Referências do projeto

- [Contrato das fontes de verdade](../../docs/sources-of-truth.md)
- [Modelo de competências](../../docs/competency-model.md)
- [Sessão extraordinária ED-05 U1 no Notion](https://app.notion.com/p/40f02f2729f9819da78cffed04628caa)
- [Documentação PostgreSQL — transações](https://www.postgresql.org/docs/current/tutorial-transactions.html)
- [Documentação PostgreSQL — concorrência](https://www.postgresql.org/docs/current/mvcc.html)
