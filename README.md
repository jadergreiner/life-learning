# Life Learning

Sistema de desenvolvimento profissional orientado por competências, com execução de estudos no Notion e apoio de um conselho técnico-pedagógico virtual.

## Estado (01/11/2026)

- **Operação vigente:** cadência de 8 posições (Notion). Não alterada.
- **Experimento:** aprendizagem adaptativa, avaliação multidimensional e até duas competências ativas após diagnóstico.
- **Plugin publicado:** Life Learning 0.2.0. A publicação do plugin é independente deste repositório.
- **Objetivo dominante:** excelência como Engenheiro de Dados Sênior; Especialista/Staff como horizonte complementar.

## Arquitetura e fontes de verdade

| Sistema | Responsabilidade | Autoridade |
|---|---|---|
| Notion — configuração | Cadência, ordem, duração operacional | Fonte operacional |
| Notion — Life Learning | Sessões, horários, ciclos, conclusões e resultados | Fonte factual |
| Notion — catálogo | Competências e regras do piloto | Fonte pedagógica experimental |
| Google Drive — PDI | Estratégia de carreira histórica | Referência estratégica |
| Google Drive — referências | Material técnico e bibliografia | Referência de conteúdo |
| Plugin Life Learning | Orquestração de sessões e recomendações | Consumidor/aplicador de regras |
| GitHub — este repositório | Versionamento de especificações, contratos e decisões | Fonte do código e documentação, não dos registros |

**Não existe sincronização automática/bidirecional implantada.** As conexões são explicitadas em [docs/sources-of-truth.md](docs/sources-of-truth.md). Evitar sobrescrita cruzada e dados privados em repositório público.

## Documentos

- [Fontes de verdade e sincronização](docs/sources-of-truth.md)
- [Conselho e modelo de competências](docs/competency-model.md)
- [Protocolo do piloto](docs/pilot.md)
- [Integrações e estado](docs/integrations.md)
- [Decisões arquiteturais](docs/decisions/ADR-0001-source-authority.md)

## Próximos passos

Diagnosticar Spark, SQL/modelagem, confiabilidade e System Design; deliberar as duas competências ativas; testar o método sem alterar a cadência oficial; só migrar mediante aprovação expressa.

Projeto experimental. Nenhuma classificação de domínio ou resultado de sessão é presumida.
