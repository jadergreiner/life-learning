# ADR-0002 — State local do Terraform para o lab002-terraform

- Status: Proposto
- Data: 2026-11-07
- SDD: SDD-0001

## Contexto

O exercício cria um único bucket vazio por pouco tempo, para uso individual. Um backend remoto exigiria infraestrutura adicional e configuração fora do esforço mínimo pedido.

## Decisão

Usar state local no diretório do laboratório. Ignorar state e arquivos auxiliares no Git; versionar `.terraform.lock.hcl`. O aluno deve manter o state até o `destroy` terminar.

## Consequências

- Não há custo ou serviço extra de backend.
- O state não deve ser compartilhado nem usado por execuções concorrentes.
- Não há coordenação ou recuperação compartilhada; perda do state pode exigir reconciliação manual.
- O state pode conter metadados ou valores sensíveis e nunca deve ser publicado.
