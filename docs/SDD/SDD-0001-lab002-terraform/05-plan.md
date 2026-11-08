# PLAN — SDD-0001 lab002-terraform

Status: Aprovado pelo usuário em 2026-11-07; P01–P08 concluídas.
Data: 2026-11-07

## 1. Objetivo

Implementar a estrutura Terraform local descrita na SPEC, documentar o uso e
validar o ciclo de criação, consulta e remoção do bucket temporário.
Nenhum recurso AWS será criado durante a elaboração ou revisão deste plano.

## 2. Unidades de trabalho

Cada unidade foi estimada para durar no máximo 15 minutos. Interromper a unidade
se surgir uma decisão fora da SPEC e registrar a questão antes de ampliar o
escopo.

| ID | Unidade | Dependências | Estimativa |
|---|---|---|---:|
| P01 | Criar `labs/lab002-terraform/` e os arquivos Terraform previstos na SPEC. | Nenhuma | 10 min |
| P02 | Declarar provider/região, variável de prefixo e derivação do nome usando o namespace `account-regional`; validar formato e comprimento. | P01 | 15 min |
| P03 | Declarar bucket S3, Block Public Access, ownership controls, SSE-S3 e política HTTPS. | P02 | 15 min |
| P04 | Declarar outputs de nome/ARN e regras `.gitignore` para state, planos, variáveis locais, `.terraform/` e crash logs. | P03 | 10 min |
| P05 | Escrever README com pré-requisitos, comandos em ordem, resultados esperados, erros previstos e limpeza. | P01–P04 | 15 min |
| P06 | Rodar `terraform fmt -check`, `terraform init` e `terraform validate`; versionar `.terraform.lock.hcl` e revisar `terraform plan`. | P01–P05 | 15 min |
| P07 | Após aprovação explícita para operação AWS, executar `apply` e as consultas CLI dos CA-002 a CA-005. | P06 | 15 min |
| P08 | Executar `destroy`, confirmar state vazio e registrar evidência dos CA-007 e CA-008. | P07 | 10 min |

Estimativa total: 105 minutos. O tempo de espera por credenciais, aprovação de
`apply` ou resolução de erros externos não está incluído.

## 3. Ordem e gates

1. Concluir P01–P05 sem acessar a AWS.
2. Revisar arquivos, proteção de segredos e comandos documentados.
3. Executar P06 localmente; interromper se provider, namespace ou validação
   exigir decisão fora da SPEC.
4. Apresentar plano e resultados locais ao usuário e aguardar aprovação para
   começar a etapa TASKS.
5. Na etapa TASKS, concluir e reportar uma unidade por vez, aguardando
   confirmação antes de iniciar a seguinte.
6. Antes de P07, obter confirmação explícita para `terraform apply` na conta AWS
   configurada. Nunca aplicar se identidade, conta ou região não forem
   verificáveis.
7. Após P07, preservar o state local até P08 concluir o destroy. Se houver
   objetos ou erro, parar, reportar e seguir o tratamento previsto na SPEC.

## 4. Checklist de validação

- [x] Implementação contém somente o bucket e as configurações de segurança
      aprovadas na SPEC.
- [x] Nome é derivado do prefixo, conta e região no namespace
      `account-regional`.
- [x] `terraform fmt -check`, `terraform init` e `terraform validate` concluem
      sem erro; lockfile do provider é versionado.
- [x] Plano revisado não inclui recursos fora do escopo.
- [x] State, variáveis locais, planos e diretório `.terraform/` não são
      versionados.
- [x] README explica resultados esperados e interrupção em caso de erro.
- [x] Após aprovação e execução AWS, consultas CLI confirmam os controles
      definidos nos CA-002 a CA-005.
- [x] `destroy` conclui e `terraform state list` não apresenta recursos do
      exercício.

## 5. Riscos e decisões pendentes

- Não há decisões de produto pendentes; PRD e SPEC registram nenhuma questão
  em aberto.
- A versão do AWS Provider deve ser escolhida e travada durante a implementação,
  verificando compatibilidade com `account-regional` naquele momento.
- A disponibilidade de credenciais e permissões AWS é pré-requisito externo.
- A criação do bucket é uma operação remota sujeita a aprovação antes de
  `apply`; a aprovação deste PLAN, por si só, não executa comandos AWS.

## 6. Aprovação

Etapa 5 — PLAN: aprovado pelo usuário em 2026-11-07. Etapa 6 — TASKS concluída.
Terraform 1.17.1, AWS Provider 6.72.0; plano revisado em `us-east-1` com cinco
recursos S3 previstos e nenhum recurso adicional. Apply criou os cinco recursos
e CA-002 a CA-005 passaram. Destroy removeu os cinco recursos; `terraform state
list` ficou vazio, e a AWS retornou 404/`NoSuchBucket` para o bucket.
