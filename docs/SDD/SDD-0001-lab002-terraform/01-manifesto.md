# Manifesto — SDD-0001 lab002-terraform

## Demanda
Padronizar o código para entregar o próximo laboratório da especialização em Engenharia de Dados, preparando a infraestrutura necessária para provisionamento na AWS com Terraform.

## Objetivo
Definir uma base padronizada de infraestrutura como código para o laboratório, começando pelo provisionamento de um bucket S3 com Terraform.

## Contexto
Este será o próximo laboratório da especialização em Engenharia de Dados.

## Restrições Conhecidas
- Manter baixo o custo dos recursos na AWS.
- Este SDD não entrega `labs\lab02`.

## Critério de Êxito
- Terraform provisiona um bucket S3.
- AWS CLI valida que o bucket foi criado.
- `terraform destroy` remove o bucket provisionado.
