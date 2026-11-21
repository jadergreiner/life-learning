# LL-ADR-002 — Sete posições orientadas à implementação (modelo híbrido)

- **Status:** Aprovada pelo estudante em 2026-11-21; atualizações de Notion, plugin e docs autorizadas em conversa subsequente.
- **Substitui:** LL-ADR-001 como direção estratégica, sem apagar sua história.
- **Fonte operacional:** [Configuração Notion](https://app.notion.com/p/3d402f2729f981c88688f3acb9ba7b20).

## Contexto
Lacuna prioritária de profundidade de implementação independente: engenharia de dados Sênior capaz de construir, testar, diagnosticar e defender soluções. O CASE-SPEC-ITAU perdeu alinhamento relativo.

## Decisão

| Posição nova | Trilha |
|---|---|
| P1 | AWS AIF-C01 |
| P2 | PREPARAÇÃO |
| P3 | SYSTEMS DESIGN |
| P4 | ROADMAP DATA ENGINEER |
| P5 | LEITURA |
| P6 | INGLÊS |
| P7 | DATABRICKS |

CASE-SPEC-ITAU sai da cadência ativa, mantendo seu repositório, especificações, ADRs e histórico de sessões. Não renumerar registros antigos. Ordem P1→P2→P3→P4→P5→P6→P7→P1 incrementando o ciclo.

## Método e evidências

Estudar → Implementar → Testar → Diagnosticar → Defender → Evidenciar. Desafio I0 independente, A1 assistido com declaração de IA, V1 adversarial, R1 retenção e GATE nas cinco dimensões: conceitual, implementação, diagnóstico, arquitetura/trade-offs e comunicação. Escala N0–N4; sem média compensatória; sessão encerrada não equivale a competência aprovada. Até duas competências técnicas em aprofundamento por vez.

**Modelo híbrido C:** SparkLens é projeto integrador preferencial, laboratórios independentes são válidos quando não há aderência. Inglês e leitura espiritual têm entregas observáveis próprias, sem imposição artificial de código. Revisar eficácia após dois ciclos completos.

## Segurança da migração

Em 21/11/2026, C20/P1 CASE-SPEC-ITAU permanecia aberta. Nunca marcar automaticamente como concluída/interrompida/cancelada: requer fato e confirmação do estudante. Não abrir nova sessão até reconciliar esse legado e definir marco de corte explícito. Preservar histórico, schema e duração real desconhecida. Mudanças na configuração não autorizam provisionar infraestrutura ou publicar commits em SparkLens.

## Autoridade

Notion Configuração = cadência; Notion Life Learning = sessões; catálogo = gates; Recall = revisões; GitHub = specs/ADRs; plugin = aplicação das regras, sempre com consulta ao Notion. Não existe sincronização bidirecional automática.
