## Why

`labs/lab02` já descreve um laboratório de AWS com SQS, Lambda e RDS, mas ainda não possui uma estrutura de diretórios Terraform para organizar sua futura infraestrutura. Preparar essa organização torna o próximo trabalho implementável e revisável sem confundir este laboratório com `labs/lab002-terraform`, que já contém o exercício temporário de S3.

## What Changes

- Definir e documentar uma estrutura inicial de diretórios Terraform dentro de `labs/lab02`.
- Manter a mudança estrutural: nenhum recurso AWS, código Terraform de provisionamento ou execução de infraestrutura é incluído.
- Preservar os materiais e o desafio pedagógico existentes em `labs/lab02`.

## Capabilities

### New Capabilities
- `terraform-lab-layout`: organização inicial e convenções de diretórios para o Terraform do LAB02.

### Modified Capabilities
- Nenhuma.

## Impact

- `labs/lab02`: adiciona a estrutura de diretórios e sua documentação de propósito.
- Não altera o laboratório separado `labs/lab002-terraform`, os contratos AWS existentes, dependências ou recursos na conta AWS.
