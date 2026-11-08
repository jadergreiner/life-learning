## Why

O LAB02 agora tem SQS/DLQ, Lambda preparatória e PostgreSQL em RDS, mas esses componentes ainda não formam um fluxo integrado e a documentação de inventário contém estados anteriores ao provisionamento. Um plano único deve avaliar responsabilidades, dependências, riscos e etapas de integração antes de alterar runtime, rede ou permissões, preservando o desafio pedagógico independente I0.

## What Changes

- Avaliar o estado atual dos módulos e dos recursos LAB02 e documentar lacunas, dependências e limites de cada componente.
- Criar um plano de integração SQS → Lambda → PostgreSQL com etapas, critérios de saída, evidências e decisões que permanecem para defesa independente.
- Organizar considerações de rede privada, credenciais/IAM, entrega e falhas, persistência, observabilidade, custos e teardown sem definir uma implementação de idempotência para o desafio I0.
- Corrigir inventários e descrições de infraestrutura que ainda afirmam que Lambda, RDS ou Terraform executável não existem.
- Não provisionar nem alterar recursos AWS, não conectar Lambda ao RDS, não criar schema/usuário de aplicação/event source mapping e não iniciar a sessão pedagógica U2.1.

## Capabilities

### New Capabilities
- `lab02-integration-plan`: avaliação documentada dos componentes existentes e plano governado, verificável e faseado para integrações futuras do LAB02.

### Modified Capabilities
- Nenhuma. Esta mudança entrega um plano e reconcilia documentação; requisitos de runtime e infraestrutura só mudam em uma implementação futura aprovada.

## Impact

- Novo documento `labs/lab02/integration-plan.md` com inventário, gaps, sequência sugerida, gates, critérios de validação e questões de decisão.
- Atualização de `labs/lab02/README.md`, `labs/lab02/terraform/README.md` e `docs/ed05-u2-aws.md` para refletirem o estado provisionado sem afirmar que o processamento ou a sessão U2.1 começou.
- Nenhuma alteração de código Terraform/Lambda, estado AWS, permissões, rede, banco, filas ou cadência pedagógica.
