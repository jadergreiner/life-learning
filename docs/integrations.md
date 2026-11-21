# Integrações e estado de sincronização

| Componente | Estado verificado | Integração |
|---|---|---|
| Plugin Life Learning | Publicado 0.2.0 | Instruções de sessões e conselho experimental |
| Notion | Configuração 7 posições pela LL-ADR-002; C20/P1 histórica aberta requer conciliação | Fonte oficial dos fatos operacionais |
| Google Drive | PDI e referências técnicas identificados | Documentos de apoio, não substitutos de Notion |
| GitHub | Este repositório | Documentação versionada |
| Recall | Uso previsto | Recuperação de conceitos; não foi validada sync automática |

## Implementação posterior (não implantada)

Um sincronizador futuro deverá operar com identificadores estáveis, autenticação segura, leituras específicas, validação de versão, idempotência, logs sem dados sensíveis e execução manual/CI previamente aprovada. Proibir sincronização bidirecional irrestrita e conflito last-write-wins.

Checklist de verificação manual: configuração no Notion; amostra de sessão válida; catálogo; versão do plugin; links e conteúdo do Drive; README/ADRs no GitHub. Reportar inconsistências sem editar fontes de autoridade por inferência.

## Observações

Esta documentação sincroniza **contratos e links**, não conteúdos pessoais nem bytes dos documentos. Nenhum workflow automático do GitHub, publicação de plugin ou mecanismo de espelhamento do Drive foi ativado.

## Verificação de 01/11/2026

- GitHub: documentação inicial publicada no branch `main`.
- Notion: catálogo do piloto contém ligação para este repositório; cadência operacional preservada.
- Plugin: atualizado para **0.2.1**, com skill `source-contract` apontando para contratos GitHub e fontes Notion/Drive; publicação confirmada por leitura posterior.
- Google Drive: leitura dos documentos históricos confirmada; **tentativa de criar um novo documento de índice negada com HTTP 403 PERMISSION_DENIED**. Nenhum documento do Drive foi modificado. A sincronização com Drive permanece apenas referencial até conceder escrita.

Não existe job automático de sincronização ativo nem espelhamento de conteúdo. Publicação do plugin e commits do GitHub são operações distintas.


## LL-ADR-002 — atualização normativa de 21/11/2026

**Estado:** sete posições aprovadas; operacionalização documentada no Notion. P1 AWS AIF-C01, P2 PREPARAÇÃO, P3 SYSTEMS DESIGN, P4 ROADMAP DATA ENGINEER, P5 LEITURA, P6 INGLÊS, P7 DATABRICKS. CASE-SPEC-ITAU fora da cadência ativa, mantendo-se integralmente seu histórico e repositório. Esta seção prevalece sobre snapshots e referências anteriores a oito posições.

**Modelo híbrido:** SparkLens integrador preferencial e laboratórios independentes quando tecnicamente mais adequados. Contrato: estudar → implementar → testar → diagnosticar → defender → evidenciar; I0 independente, A1 assistido declarado, V1 adversarial, R1 retenção, GATE multidimensional N0–N4 sem média compensatória. Máximo de duas competências técnicas em aprofundamento; inglês e leitura mantêm entregas próprias sem código compulsório. Encerramento de sessão não aprova competência. Reavaliar o método após dois ciclos novos completos.

**Bloqueio de transição:** C20/P1 CASE-SPEC-ITAU estava aberta em 21/11/2026 19h11 BRT. Não classificar como concluída, interrompida ou cancelada sem evidência e confirmação; não criar sessão nova enquanto não houver reconciliação e marco de corte explícito. Não reescrever posições/ciclos históricos. Fonte operacional: [Notion Configuração](https://app.notion.com/p/3d402f2729f981c88688f3acb9ba7b20); [LL-ADR-002 Notion](https://app.notion.com/p/41f02f2729f9812c967ad7040e86b87a).
