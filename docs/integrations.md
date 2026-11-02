# Integrações e estado de sincronização

| Componente | Estado verificado | Integração |
|---|---|---|
| Plugin Life Learning | Publicado 0.2.0 | Instruções de sessões e conselho experimental |
| Notion | Configuração 8 posições; banco de sessões e catálogo | Fonte oficial dos fatos operacionais |
| Google Drive | PDI e referências técnicas identificados | Documentos de apoio, não substitutos de Notion |
| GitHub | Este repositório | Documentação versionada |
| Recall | Uso previsto | Recuperação de conceitos; não foi validada sync automática |

## Implementação posterior (não implantada)

Um sincronizador futuro deverá operar com identificadores estáveis, autenticação segura, leituras específicas, validação de versão, idempotência, logs sem dados sensíveis e execução manual/CI previamente aprovada. Proibir sincronização bidirecional irrestrita e conflito last-write-wins.

Checklist de verificação manual: configuração no Notion; amostra de sessão válida; catálogo; versão do plugin; links e conteúdo do Drive; README/ADRs no GitHub. Reportar inconsistências sem editar fontes de autoridade por inferência.

## Observações

Esta documentação sincroniza **contratos e links**, não conteúdos pessoais nem bytes dos documentos. Nenhum workflow automático do GitHub, publicação de plugin ou mecanismo de espelhamento do Drive foi ativado.
