## 1. Avaliar baseline e lacunas

- [x] 1.1 Conferir módulos, root Terraform e specs para registrar o estado de SQS/DLQ, Lambda, RDS e integrações ausentes sem consultar ou alterar recursos AWS.
- [x] 1.2 Mapear dependências entre contrato de mensagem, modelo de dados/migrações, rede privada, IAM/segredos, event source mapping, retries/DLQ e observabilidade.

## 2. Produzir o plano de integração

- [x] 2.1 Criar `labs/lab02/integration-plan.md` com inventário por componente, lacunas atuais e sequência de fases com pré-requisitos, decisões, critérios de saída e evidências.
- [x] 2.2 Relacionar as fases de validação a AWS-01–AWS-07 e manter abertas as decisões que pertencem à defesa independente I0, sem fornecer implementação de idempotência.
- [x] 2.3 Registrar nas fases futuras os gates de estimativa, teto de custo, autorização operacional e teardown antes de mudanças AWS.

## 3. Reconciliar documentação e validar escopo

- [x] 3.1 Atualizar `labs/lab02/README.md` e `labs/lab02/terraform/README.md` para refletir os módulos e recursos existentes, mantendo explícito que não há processamento integrado.
- [x] 3.2 Atualizar `docs/ed05-u2-aws.md` com o inventário factual sem declarar iniciada a sessão U2.1, alterar os critérios de avaliação ou mudar a cadência.
- [x] 3.3 Revisar links, estados e consistência entre o plano, os READMEs, o contrato ED-05 e as specs do LAB02; confirmar que nenhuma configuração/runtime/AWS foi alterada.
