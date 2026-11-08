## Context

O LAB02 (`labs/lab02`) documenta uma arquitetura de processamento com SQS, Lambda e PostgreSQL em RDS, mas ainda não tem Terraform. O exercício independente de bucket S3 já está implementado em `labs/lab002-terraform` e permanece separado. Esta mudança prepara apenas a organização para um trabalho futuro, respeitando o gate existente contra provisionamento sem autorização explícita.

## Goals / Non-Goals

**Goals:**
- Criar um ponto de entrada Terraform do laboratório e locais explícitos para módulos por responsabilidade.
- Tornar a estrutura autoexplicativa por meio de READMEs curtos, versionáveis e sem recursos AWS.
- Manter o layout enxuto e adequado ao LAB02 descrito atualmente.

**Non-Goals:**
- Escrever `.tf` executável, escolher versões de providers ou definir valores de infraestrutura.
- Criar recursos, executar Terraform ou acessar a AWS.
- Alterar `labs/lab002-terraform`, o desafio I0 ou os critérios AWS-01–AWS-07.

## Decisions

- Criar `labs/lab02/terraform/` como raiz de infraestrutura do laboratório. O `README.md` nessa pasta explica o layout e registra que está preparado para implementação, sem estado ou recursos.
- Criar `labs/lab02/terraform/environments/lab/` como futuro root module de execução do laboratório. Separar o root module dos módulos evita misturar composição/variáveis de ambiente com componentes reutilizáveis.
- Reservar `labs/lab02/terraform/modules/queue/`, `modules/processor/` e `modules/database/` para os componentes SQS, Lambda e PostgreSQL/RDS já descritos no escopo pedagógico. Cada pasta terá um README placeholder que define apenas sua responsabilidade e não antecipa implementação.
- Não criar pasta `network`: a arquitetura documentada não determina topologia, VPC ou subnets, então esse módulo seria prematuro.
- Não incluir `.gitkeep` ou arquivos `.tf` vazios; READMEs dão propósito rastreável aos diretórios e evitam stubs Terraform inválidos.

Alternativas consideradas: colocar toda a configuração diretamente em `terraform/` simplificaria o início, mas não separaria o root module de componentes; criar módulos para rede e outros recursos agora ampliaria o desenho além das decisões registradas. A estrutura modular pequena é preferida como organização preparatória, sujeita à revisão quando a especificação de infraestrutura for aprovada.

## Risks / Trade-offs

- [A estrutura sugere módulos antes de seus contratos estarem definidos] → READMEs devem identificá-los como reservas sem implementação, e a futura etapa de design pode ajustar/remover módulos antes de criar recursos.
- [Diretórios placeholder podem parecer infraestrutura pronta] → O README principal deve afirmar explicitamente que não há configuração executável nem recursos provisionados.

## Migration Plan

Adicionar as pastas e READMEs; não há migração ou rollback de infraestrutura. Para reverter, remover somente os novos arquivos em `labs/lab02/terraform/`.

## Open Questions

Nenhuma para esta mudança estrutural. Contratos e decisões de implementação dos módulos ficam para uma mudança futura.
