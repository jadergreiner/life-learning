# ADR-0004 — Escopo mínimo de recursos do lab002-terraform

- Status: Proposto
- Data: 2026-11-07
- SDD: SDD-0001

## Contexto

O objetivo é demonstrar Terraform criando, validar e remover um bucket S3 temporário, mantendo baixo custo e esforço.

## Decisão

Provisionar somente um bucket S3 e seus controles necessários: Block Public Access, ownership controls, SSE-S3 e política de transporte HTTPS. IAM, backend remoto, logs de acesso, CloudTrail data events e métricas adicionais ficam fora do escopo.

## Consequências

- O exercício tem poucos recursos e deve ser destruído após a validação.
- Credenciais e permissões IAM precisam existir antes da execução.
- Observabilidade adicional e uso de produção não são objetivos deste laboratório.
