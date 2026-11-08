# Tasks — SDD-0001 lab002-terraform

Status: P01–P08 concluídas.

| ID | Unidade | Status |
|---|---|---|
| P01 | Criar estrutura inicial e arquivos previstos na SPEC. | Concluída |
| P02 | Declarar provider/região, prefixo e derivação do nome. | Concluída |
| P03 | Declarar bucket S3 e controles de segurança. | Concluída |
| P04 | Declarar outputs e regras de exclusão do Git. | Concluída |
| P05 | Escrever README operacional. | Concluída |
| P06 | Validar formatação, init, validate e revisar plan. | Concluída; Terraform 1.17.1, AWS Provider 6.72.0; plano revisado: 5 recursos S3, sem apply. |
| P07 | Aplicar e executar consultas AWS após aprovação explícita. | Concluída: 5 recursos criados; CA-002 a CA-005 aprovados |
| P08 | Destruir recursos e registrar evidências. | Concluída: 5 recursos destruídos; `terraform state list` vazio; AWS retornou 404/NoSuchBucket |
