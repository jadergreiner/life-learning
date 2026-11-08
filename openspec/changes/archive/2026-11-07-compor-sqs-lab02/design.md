## Context

O módulo filho SQS está implementado e validado. A autorização para provisionar cobre somente as filas Standard e DLQ, vazias e sem tráfego da aplicação, na conta `325422573352` e região `us-east-1`. A tentativa anterior na conta `437537458973` foi destruída; o prefixo `lab02-sqs-20261107` deve ser verificado novamente na conta-alvo antes do plano.

O acesso Terraform usa o usuário IAM `lab02-terraform` e a policy inline `Lab02TerraformSQS`, limitada às ações necessárias e aos ARNs das filas com prefixo `lab02-sqs-20261107` na conta/região aprovadas. A chave foi guardada no perfil AWS CLI local `lab02-terraform`, fora do repositório.

## Goals / Non-Goals

**Goals:**
- Configurar root module que instancia apenas o módulo `modules/queue`.
- Fixar localmente a identidade alvo e os valores de fila aprovados, mantendo state e plano fora do Git.
- Revisar e aplicar um plano que contenha somente as duas filas SQS e as políticas de redrive.
- Documentar verificação e teardown.

**Non-Goals:**
- Criar produtor/consumidor, Lambda, RDS, IAM, VPC, CloudWatch, budget ou alertas.
- Enviar mensagens, abrir sessão pedagógica ou alterar a cadência do Life Learning.
- Provisionar qualquer recurso além da fila principal e da DLQ.

## Decisions

- **Usar `environments/lab` como root module.** Ele configura região e AWS Provider e instancia o módulo filho, evitando duplicação dos recursos SQS.
- **Restringir a conta por variável local obrigatória e precondition.** O data source `aws_caller_identity` valida que o profile efetivamente autenticado corresponde à conta aprovada antes da composição do módulo. O identificador fica somente em `terraform.tfvars` ignorado pelo Git; credenciais não entram no repositório e o account ID não fica em artefatos versionáveis.
- **Usar state local.** O laboratório é individual e temporário; não criar backend remoto ou novos serviços cobrados. State, variáveis locais e plano são ignorados pelo Git, e o state permanece até `destroy` concluir.
- **Declarar provider AWS compatível com o módulo.** A constraint do root será `>= 6.41.0, < 7.0.0`, coerente com os recursos verificados. O lockfile será versionado após `init`.
- **Usar sizing confirmado pelo usuário.** Prefixo `lab02-sqs-20261107`, retenção principal 345.600 s (4 dias), retenção DLQ 1.209.600 s (14 dias), visibilidade 30 s, `maxReceiveCount` 10 e long polling 20 s.
- **Limitar custo pelo uso acordado.** Filas vazias, sem tráfego de aplicação, sem KMS, alarmes ou outros serviços. SQS não tem tarifa mínima e oferece 1 milhão de requests gratuitos por mês; a estimativa direta é US$ 0 enquanto o uso total da conta permanecer na franquia. Chamadas além da franquia podem cobrar por request. Não há orçamento por fila criado neste escopo.
- **Aplicar somente depois de revisar o plano localmente.** Confirmar conta, região, dois recursos `aws_sqs_queue` e políticas associadas; não executar plan/apply em outra conta.

Alternativas consideradas: usar o diretório do módulo filho como root não permitiria declarar provider, state e parâmetros com clareza; backend remoto exigiria recursos adicionais; usar conta default sem precondition poderia criar recursos no alvo errado.

## Risks / Trade-offs

- [A configuração default pode mudar após o teste] → gravar o account ID esperado localmente e bloquear o plano quando STS retornar conta diferente.
- [State local é essencial para teardown] → ignorá-lo no Git, mantê-lo no workspace e documentar que não deve ser removido antes de `destroy`.
- [Franquia SQS é agregada à conta e outros workloads podem consumi-la] → não produzir mensagens e manter as filas vazias; sem tráfego de aplicação, revisar custos antes de integrar outro componente.
- [Visibility timeout foi dimensionado sem consumidor] → manter somente o valor aprovado para esta etapa e revisá-lo quando a Lambda for especificada.

## Migration Plan

Não há migração. Criar configuração de root e valores locais, executar `terraform init`, `fmt`, `validate` e `plan`, revisar a identidade/escopo, aplicar as duas filas e confirmar atributos/outputs. Para teardown, executar `terraform destroy` no mesmo root e preservar o state até a confirmação de ausência das filas.

## Open Questions

Nenhuma pendente para o provisionamento SQS limitado a filas vazias. O teto de custo assumido é nenhum tráfego de aplicação e uso total de SQS da conta dentro da franquia mensal; integração futura exige nova estimativa.
