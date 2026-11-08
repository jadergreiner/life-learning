## Context

O LAB02 descreve SQS Standard como origem de mensagens e uma DLQ para falhas recorrentes, com Lambda como consumidora e PostgreSQL como autoridade da integridade financeira. `modules/queue` contém apenas um README placeholder; o root module ainda não compõe componentes. O contrato ED-05 exige sizing justificado para parâmetros de fila e autorização operacional separada antes de iniciar sessão ou provisionar.

## Goals / Non-Goals

**Goals:**
- Oferecer um módulo Terraform reutilizável com fila Standard, DLQ Standard e redrive configurável.
- Deixar explícitos os parâmetros que afetam retenção, latência/reentrega e número de tentativas.
- Fornecer outputs para composição futura com consumidor e observabilidade.

**Non-Goals:**
- Criar ou integrar Lambda, IAM, RDS, VPC, CloudWatch ou infraestrutura de rede.
- Definir garantia exactly-once, idempotência financeira ou contrato final de processamento em lote.
- Escolher valores operacionais finais sem justificativa do aluno, estimativa de custos e validação.
- Executar `terraform apply`, iniciar sessão pedagógica ou provisionar recursos AWS.

## Decisions

- **Fila principal e DLQ serão SQS Standard.** Isso segue a arquitetura de referência do LAB02 e permite entrega pelo menos uma vez; não promete ordem estrita nem processamento exactly-once. FIFO fica fora do escopo porque mudaria o desafio e o contrato.
- **A fila principal terá redrive policy apontando à DLQ e a DLQ terá redrive allow policy restrita à fila fonte.** Isso torna explícita a relação e impede que a DLQ aceite redrive de fontes não previstas. `maxReceiveCount` será uma entrada obrigatória e validada, não uma escolha silenciosa do módulo.
- **Configurações de retenção e visibility timeout serão inputs explícitos.** A fila e a DLQ permitem valores apropriados ao caso de uso; o módulo valida limites aceitos pelo provider/serviço, mas não escolhe sizing pedagógico. Long polling também será configurável e terá valor seguro documentado, sujeito a revisão quando o consumidor for definido.
- **Outputs incluirão URL, ARN e nome de ambas as filas.** A integração futura poderá conceder permissões ao ARN correto e configurar o event source mapping sem acoplar este módulo à Lambda.
- **Sem recursos de criptografia KMS ou políticas IAM adicionais nesta etapa.** A criptografia gerenciada padrão do SQS será mantida, evitando adicionar chave, permissões e custos/decisões não exigidos pelo contrato atual. O README explicará essa fronteira.
- **O módulo será composto pelo root module apenas em mudança posterior.** Isso mantém a implementação do componente revisável e evita inventar valores de ambiente no root ainda vazio.

Alternativas consideradas: usar FIFO para deduplicação/ordenação não substitui idempotência transacional no PostgreSQL e altera o exercício; uma DLQ sem redrive policy não atende ao critério AWS-06; codificar valores de sizing como constantes esconderia decisões ainda pendentes.

## Risks / Trade-offs

- [Configurações válidas isoladamente podem não ser compatíveis com timeout/batch da futura Lambda] → documentar as relações que precisam ser validadas antes da integração, sem afirmar sizing definitivo.
- [SQS Standard pode entregar duplicatas e fora de ordem] → registrar explicitamente que deduplicação e correção financeira pertencem ao consumidor e PostgreSQL.
- [Recursos provisionados geram custo e podem receber dados] → limitar o change a código/documentação e planos; exigir autorização explícita e plano de teardown antes de qualquer `apply` futuro.
- [Políticas de acesso não são parte do módulo] → outputs fornecem ARNs, e integração futura deverá definir IAM de privilégio mínimo sem abrir acesso público.

## Migration Plan

Não há migração de recursos porque o módulo ainda não provisiona infraestrutura. Implementar os arquivos, validar sintaxe/formatação e executar somente `terraform init`/`validate` e planejamento sem aplicar quando houver configuração de ambiente e autorização. Rollback consiste em reverter os arquivos do módulo; se uma implementação futura tiver sido aplicada, destruir primeiro por meio do state correspondente.

## Open Questions

- Qual região e valores de retenção, visibility timeout, long polling e maxReceiveCount serão defendidos pelo aluno antes da composição do ambiente?
- O contrato de observabilidade do laboratório exigirá alarmes ou métricas dedicadas de fila em um change posterior?
