# ADR-0001 — Autoridade das fontes e migração gradual

- Status: Aceita para documentação, sujeita às decisões operacionais registradas no Notion
- Data: 2026-11-01

## Contexto

O Life Learning possui plugin de orquestração, histórico e configuração no Notion, material estratégico no Drive e agora repositório público GitHub. A nova metodologia adaptativa ainda é experimental. Múltiplas fontes equivalentes podem causar discrepâncias.

## Decisão

Notion permanece autoritativo para configuração e sessões; página separada contém catálogo do piloto. Google Drive é referência estratégica/técnica; GitHub é fonte de versionamento de especificações, documentação e futuras automações; plugin interpreta e executa procedimentos a partir da fonte operacional. Só aprovar mudanças de cadência mediante decisão explícita e escrita validada no Notion.

## Consequências

- Nenhum espelhamento bidirecional implícito.
- Preservação de histórico e de dados privados.
- Revisões do conselho podem propor, mas não impor, mudanças.
- A implantação futura de sync requer gates de validação e autorização.
