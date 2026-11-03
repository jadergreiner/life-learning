# Competências e conselho técnico-pedagógico — v0.1 (piloto)

## Catálogo inicial (não representa posições de estudo)

| Código | Domínio |
|---|---|
| ED-01 | Programação, Python e SQL |
| ED-02 | Modelagem e armazenamento |
| ED-03 | Spark e processamento distribuído |
| ED-04 | Integração e orquestração |
| ED-05 | Confiabilidade, qualidade e observabilidade |
| ED-06 | Arquitetura, cloud, segurança e governança |
| ED-07 | Lakehouse, Databricks, DataOps e IA aplicada |

Definir critérios concretos por subcompetência. Um nível não é inferido do cargo, histórico ou quantidade de flashcards.

## Avaliação multidimensional

Dimensões: (1) compreensão conceitual; (2) implementação; (3) diagnóstico; (4) arquitetura/trade-offs; (5) comunicação. Retenção e transferência são atributos reavaliados no tempo.

N0: sem evidência suficiente; N1: fundamentos; N2: aplicação; N3: autonomia avançada; N4: referência técnica. Níveis são rubrica interna, não certificações oficiais. Não usar média para compensar uma dimensão crítica ausente.

Evidências: desafios a frio, artefatos, testes positivos e negativos, métricas, hipóteses, defesa independente, limites do experimento. Uma execução sem erro não prova correção semântica. Resultados do Recall apoiam retenção, mas não substituem implementação.

## Conselho

- **Helena:** método e validade pedagógica.
- **Fernanda:** rigor de testes e correção técnica.
- **Marcelo:** evolução de carreira, comunicação e custo de oportunidade.
- **Ricardo:** relevância e portabilidade no mercado.
- **Mediador:** síntese, desacordos e decisão proposta.
- **Estudante:** decisão final.

Perspectivas são simuladas por IA, não revisores independentes nem tarefas em segundo plano. Preservar divergências; convocar fórum em decisões estratégicas, impasses, estagnação ou avaliações críticas.

Fonte normativa experimental: [catálogo do Notion](https://app.notion.com/p/40c02f2729f981c2bb7acd89a631d32c).

## Protocolo de avaliação, fechamento e recuperação (revisão de 02/11/2026)

- A avaliação oral a frio deve distinguir evidência independente de aprendizagem orientada. Uma explicação correta após dicas e demonstrações não basta para promoção automática a N3.
- Em falhas entre efeitos externos e commit local, exigir distinção explícita entre integridade do estado no banco e entrega/execução fora dele. Uma confirmação local não prova efeito externo único.
- Em laboratório de confiabilidade (ED-05), avaliar: transações curtas, aquisição atômica de leases, expiração, concorrência, fencing tokens, retries, falhas após HTTP 200, observabilidade, testes de recuperação e limites do exactly-once sem idempotência do provedor.
- Fencing tokens podem impedir atualização de estado por workers obsoletos, mas, sem validação pelo sistema externo, não garantem ausência de duplicidade na API HTTP.
- Requerer decisão de política de entrega por criticidade e discussão de duplicidade, omissão e validade temporal, com garantias condicionais e riscos residuais explícitos.
- No encerramento de uma revisão extra, registrar as evidências no catálogo e o fato da sessão no Notion sem inventar minutos ou alterar ciclo/posição. A revisão espaçada usa o deck Recall canônico definido em [contrato de fontes](sources-of-truth.md).
- O próximo gate de comprovação de autonomia é um laboratório reproduzível e uma reavaliação sem consulta; a cadência regular não é afetada pelo diagnóstico.
