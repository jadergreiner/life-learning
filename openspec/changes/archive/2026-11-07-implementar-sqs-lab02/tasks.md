## 1. Implementar módulo da fila

- [x] 1.1 Definir variáveis de nomes/prefixo e parâmetros configuráveis para fila principal, DLQ, retenção, visibility timeout, long polling e maxReceiveCount, com validações.
- [x] 1.2 Criar recursos Terraform da fila Standard, DLQ Standard, redrive policy e redrive allow policy restrita à fonte.
- [x] 1.3 Expor outputs de URL, ARN e nome para ambas as filas.
- [x] 1.4 Atualizar README do módulo com semântica Standard, parâmetros, limites, outputs e fronteiras de IAM/Lambda.

## 2. Verificar o módulo sem provisionar

- [x] 2.1 Revisar compatibilidade dos atributos com a versão AWS Provider definida no root module quando ele existir; não inventar versão independente. (O root module ainda não existe; os recursos/atributos foram conferidos na documentação oficial do provider 6.41.0, sem adicionar constraint independente.)
- [x] 2.2 Validar formatação e configuração Terraform usando validação local aplicável; registrar limitações enquanto não houver root module. (`terraform fmt -check` e `terraform validate` passaram com um harness temporário e AWS Provider 6.72.0; nenhum plan/apply foi executado.)
- [x] 2.3 Confirmar que nenhum apply foi executado e que o diff desta implementação permanece restrito ao módulo SQS do LAB02 e artefatos OpenSpec.
