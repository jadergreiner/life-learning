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


## LL-ADR-002 — atualização normativa de 21/11/2026

**Estado:** sete posições aprovadas; operacionalização documentada no Notion. P1 AWS AIF-C01, P2 PREPARAÇÃO, P3 SYSTEMS DESIGN, P4 ROADMAP DATA ENGINEER, P5 LEITURA, P6 INGLÊS, P7 DATABRICKS. CASE-SPEC-ITAU fora da cadência ativa, mantendo-se integralmente seu histórico e repositório. Esta seção prevalece sobre snapshots e referências anteriores a oito posições.

**Modelo híbrido:** SparkLens integrador preferencial e laboratórios independentes quando tecnicamente mais adequados. Contrato: estudar → implementar → testar → diagnosticar → defender → evidenciar; I0 independente, A1 assistido declarado, V1 adversarial, R1 retenção, GATE multidimensional N0–N4 sem média compensatória. Máximo de duas competências técnicas em aprofundamento; inglês e leitura mantêm entregas próprias sem código compulsório. Encerramento de sessão não aprova competência. Reavaliar o método após dois ciclos novos completos.

**Bloqueio de transição:** C20/P1 CASE-SPEC-ITAU estava aberta em 21/11/2026 19h11 BRT. Não classificar como concluída, interrompida ou cancelada sem evidência e confirmação; não criar sessão nova enquanto não houver reconciliação e marco de corte explícito. Não reescrever posições/ciclos históricos. Fonte operacional: [Notion Configuração](https://app.notion.com/p/3d402f2729f981c88688f3acb9ba7b20); [LL-ADR-002 Notion](https://app.notion.com/p/41f02f2729f9812c967ad7040e86b87a).
