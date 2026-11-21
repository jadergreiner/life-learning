# Contrato das fontes de verdade

## Identificadores canônicos

- Notion hub: https://app.notion.com/p/3be02f2729f981dc9f20e189249e3f6e
- Notion configuração: https://app.notion.com/p/3d402f2729f981c88688f3acb9ba7b20
- Notion sessões: https://app.notion.com/p/89c62024979f4fa78efe473060ae3490
- Notion data source: `collection://f50e0b81-cc3b-4ecf-b06f-5ca515309e21`
- Notion catálogo experimental: https://app.notion.com/p/40c02f2729f981c2bb7acd89a631d32c
- Drive PDI: https://docs.google.com/document/d/13zSOe_hnWl1mGQKr3qKlDDtusIP6IJHEZjvTxtzq1Ag/edit
- Drive referências: https://docs.google.com/document/d/1zcxt8lWfpdEFBZlZo7S91CkluLiLgAyd_tcgnowUYrU/edit
- Plugin: https://chatgpt.com/plugins/plugins_6ab8471478688191bdf070818f03b3ee

## Matriz de autoridade

1. Decisões explícitas do estudante governam objetivo e mudanças estratégicas.
2. Configuração específica do Notion prevalece em cadência e ordem de posições.
3. Banco de sessões do Notion é único registro factual de sessões, duração e conclusão.
4. Catálogo do Notion representa método e avaliação experimental.
5. PDI no Drive é referência estratégica histórica; referências técnicas do Drive são material de estudo.
6. Plugin aplica as regras verificadas nas fontes, sem criar fatos.
7. GitHub versiona design, regras, ADRs e artefatos sem ser réplica dos dados pessoais.

## Política de sincronização

- **Leitura:** consultar configuração vigente antes de qualquer cálculo de próximo bloco ou sessão.
- **Escrita:** consultar → validar → decidir → executar → reconsultar → reportar.
- **Prioridade:** versão do documento ou data de modificação isoladas não substituem decisão explícita.
- **Conflitos:** sinalizar conflito, não escolher por nome de arquivo; preservar dados e solicitar deliberação quando houver ambiguidade estratégica.
- **Privacidade:** não exportar histórico de sessões nem observações pessoais para GitHub público; nunca commitar credenciais.
- **Mudança de cadência:** requer autorização expressa e atualização da página operacional no Notion, com compatibilidade retroativa.
- **Plugin:** publicar nova versão somente após verificar regras contra Notion; versionar mudanças deste repositório não atualiza o plugin automaticamente.
- **Drive:** não modificar documentos estratégicos históricos sem delimitar mudanças e preservar a versão original.
- **Auditabilidade:** registrar em docs/decisions o motivo e links, não dados sensíveis.

## Cadência vigente — LL-ADR-002 (21/11/2026)

P1 AWS AIF-C01; P2 PREPARAÇÃO; P3 SYSTEMS DESIGN; P4 ROADMAP DATA ENGINEER; P5 LEITURA; P6 INGLÊS; P7 DATABRICKS. P7 → P1 incrementando ciclo. CASE-SPEC-ITAU permanece apenas no histórico. Referência 50+10 min é organização, não duração comprovada nem gate. Marco de corte pendente de conciliação da sessão aberta C20/P1 histórica. O Notion prevalece.

## Recall — deck canônico do Life Learning (02/11/2026)

- Deck único para **novos flashcards do método Life Learning**: [LIFE LEARNING — Revisão Integrada](https://recall.cards/app/decks/etzhanpbigllkhrjmqxe).
- ID de execução Recall: `deck_0GNiZtx9jIeh`. O deck foi renomeado, preservando cartões e histórico de revisão; o acervo anterior permanece intocado, sem migração automática.
- **Notion continua a fonte da verdade** para sessões, ciclos, posição, competências, decisões e evidências pedagógicas. Recall é fonte operacional de cartões e agendamento espaçado, não de domínio técnico ou conclusão de sessão.
- Ao registrar revisão: consultar o Notion, identificar lacunas, buscar cartas existentes, adicionar somente cartões atômicos novos ao deck canônico, conferir persistência e não criar decks paralelos.
- A atualização do plugin é independente do versionamento GitHub. Plugin Life Learning v0.2.2 confirmou o contrato de integração Recall/Notion.
- Não publicar no GitHub público histórico individual, notas, pontuações, respostas de avaliação ou dados pessoais. Registros pedagógicos permanecem no Notion.
- Uma sessão extra de revisão não avança a cadência vigente de oito posições. Nenhum tempo deve ser inferido quando a duração líquida não for fornecida.


## LL-ADR-002 — atualização normativa de 21/11/2026

**Estado:** sete posições aprovadas; operacionalização documentada no Notion. P1 AWS AIF-C01, P2 PREPARAÇÃO, P3 SYSTEMS DESIGN, P4 ROADMAP DATA ENGINEER, P5 LEITURA, P6 INGLÊS, P7 DATABRICKS. CASE-SPEC-ITAU fora da cadência ativa, mantendo-se integralmente seu histórico e repositório. Esta seção prevalece sobre snapshots e referências anteriores a oito posições.

**Modelo híbrido:** SparkLens integrador preferencial e laboratórios independentes quando tecnicamente mais adequados. Contrato: estudar → implementar → testar → diagnosticar → defender → evidenciar; I0 independente, A1 assistido declarado, V1 adversarial, R1 retenção, GATE multidimensional N0–N4 sem média compensatória. Máximo de duas competências técnicas em aprofundamento; inglês e leitura mantêm entregas próprias sem código compulsório. Encerramento de sessão não aprova competência. Reavaliar o método após dois ciclos novos completos.

**Bloqueio de transição:** C20/P1 CASE-SPEC-ITAU estava aberta em 21/11/2026 19h11 BRT. Não classificar como concluída, interrompida ou cancelada sem evidência e confirmação; não criar sessão nova enquanto não houver reconciliação e marco de corte explícito. Não reescrever posições/ciclos históricos. Fonte operacional: [Notion Configuração](https://app.notion.com/p/3d402f2729f981c88688f3acb9ba7b20); [LL-ADR-002 Notion](https://app.notion.com/p/41f02f2729f9812c967ad7040e86b87a).
