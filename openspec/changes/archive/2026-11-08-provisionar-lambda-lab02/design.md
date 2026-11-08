## Context

O root module `labs/lab02/terraform/environments/lab` já gerencia a fila principal e a DLQ SQS na conta aprovada `325422573352`, região `us-east-1`, com state local preservado. `modules/processor` é apenas um README placeholder. O documento ED-05 define Lambda como consumidor único conceitual e descreve concorrência/reentrega como objetivos do laboratório; o diagrama A/B é hipótese visual, não requisito de duas funções. O usuário decidiu preparar uma função e deixar as integrações para outra mudança.

O ambiente é individual e temporário. Qualquer apply requer plano revisado, estimativa atualizada e autorização operacional específica. A identidade de provisionamento Terraform é o usuário IAM `lab02-terraform`, nunca root.

## Goals / Non-Goals

**Goals:**

- Provisionar uma única função Lambda `lab02-processor` executável por invocação direta.
- Criar seu pacote ZIP mínimo de Python e uma execution role limitada a logging.
- Gerenciar um log group com retenção curta e outputs suficientes para inspecionar a função.
- Compor os recursos no root existente, mantendo a trava de account ID e o state da fila/DLQ.

**Non-Goals:**

- Consumir SQS, criar event source mapping, alterar as filas ou garantir concorrência/retries.
- Criar produtor, processador financeiro, esquema de evento, acesso a RDS/PostgreSQL, VPC ou segurança de rede.
- Criar URL pública, publicar versões/aliases, provisionar concorrência dedicada, alarmes ou dashboards.
- Armazenar segredos ou dados de aplicação na configuração da função.

## Decisions

1. **Uma função preparatória, em vez de duas funções A/B.** O SQS entrega mensagens entre event source mappings concorrentes; duas funções ligadas à mesma fila não recebem cópias garantidas de cada mensagem. Uma função pode ter várias execuções simultâneas quando houver demanda. Esta mudança cria somente a função; o teste AWS-03 depende de uma futura integração e de mensagens de teste com o mesmo `event_id`.

2. **Handler mínimo Python 3.14, em ZIP local sem dependências.** Criar um arquivo fonte pequeno que retorna `{"status":"ready"}` sem registrar o evento nem causar efeitos externos. Gerar o ZIP com o data source `archive_file` e usar o hash do arquivo para atualizar o código. Python 3.14 é runtime gerenciado listado pela AWS no momento da proposta; a lista deve ser conferida novamente antes do apply. O pacote e o runtime seguem a estrutura documentada pela [AWS para Python ZIPs](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html) e a [lista de runtimes](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html). O `archive_file` cria o pacote durante o plan, então o arquivo deve permanecer no mesmo caminho até o apply ([HashiCorp archive_file](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file)).

3. **Configuração inicial pequena e explícita.** Usar 128 MB, timeout de 3 segundos, arquitetura `x86_64`, handler `lambda_function.handler` e sem variáveis de ambiente. O timeout de 3 segundos é adequado ao handler sem I/O; não é sizing para processamento futuro. Quando houver event source mapping, recalcular timeout, janela de lote e visibility timeout SQS em conjunto.

4. **Role e logging sem acesso de aplicação.** A execution role confia somente em `lambda.amazonaws.com` e recebe apenas permissões de CloudWatch Logs para a função. Não recebe permissões SQS, RDS, Secrets Manager ou rede. Criar o log group `/aws/lambda/lab02-processor` com retenção configurável e default de 7 dias; criar o grupo antes da função. Não incluir log da entrada nem dados financeiros.

5. **Pacote e recursos locais dentro do módulo processor.** Manter o handler e o arquivo ZIP gerado sob `labs/lab02/terraform/modules/processor/`; ignorar ZIPs gerados no Git. O módulo não declara provider/backend. O root fixa as versões AWS e Archive, configura providers e instancia o módulo, mantendo o provider lockfile versionado.

6. **Expandir permissões do provisionador de forma delimitada.** O usuário `lab02-terraform` mantém as permissões SQS atuais e recebe permissões somente para a função, log group e role nomeados. `iam:PassRole` fica restrita à execution role aprovada e ao serviço Lambda; o attach de policy da role fica restrito à policy AWS gerenciada de logging. Não conceder `iam:*`, `lambda:*` amplo, `iam:CreatePolicy` ou permissões de workload SQS/RDS à função. Validar a policy IAM antes de atualizar o perfil.

7. **Estender o mesmo root/state e proteger o ciclo de vida.** O plano deve preservar os recursos SQS existentes e adicionar somente Lambda, role e log group previstos. Outputs incluem nome/ARN da função e ARN da execution role. `destroy` no mesmo root/state remove a função, role e log group junto das filas existentes; manter state até finalizar o teardown.

## Risks / Trade-offs

- [Uma função sem trigger não consome SQS nem demonstra os critérios AWS-01–AWS-06] → documentar como scaffolding implantável e reservar comportamento/trigger para mudança posterior.
- [Handler placeholder pode ser confundido com processador financeiro] → retornar apenas status fixo, sem event schema, side effect ou claim de aprovação dos critérios AWS.
- [Runtime gerenciado e provider mudam ao longo do tempo] → consultar a documentação oficial e revisar o lockfile no plano imediatamente antes da implantação.
- [Delegação IAM incorreta pode ampliar autoridade do deployer ou da função] → restringir recursos e `iam:PassRole`, anexar apenas policy de logging e revisar/validar o documento IAM antes de aplicar.
- [Retenção de logs incorreta acumula custo ou apaga evidência cedo] → usar retenção configurável de 7 dias como default temporário e incluir logs na estimativa de custo.
- [Timeout de 3 s pode ser insuficiente para o futuro processamento] → tratá-lo como valor exclusivo do handler atual e recalibrar junto com RDS, lote e visibility timeout antes da integração.
- [archive_file exige arquivo ZIP persistente entre plan e apply] → não limpar o pacote gerado até concluir o apply; ignorá-lo no Git.

## Migration Plan

1. Implementar handler mínimo, módulo Terraform e contrato do root; definir e revisar as permissões específicas do provisionador.
2. Executar formatação, inicialização, validação e gerar plano usando o perfil `lab02-terraform`; confirmar conta/região, preservação das filas e somente recursos do escopo.
3. Atualizar a estimativa de custo de Lambda e CloudWatch Logs; só aplicar após revisão e autorização operacional explícita.
4. Após apply autorizado, validar identidade, configuração, role, log group, outputs e state; testar apenas invocação direta do handler mínimo, se autorizado.
5. Para rollback, usar `terraform destroy` no mesmo root/state e confirmar que os recursos foram removidos antes de apagar state ou arquivos de pacote.

## Open Questions

- Nenhuma em aberto para esta base preparatória. O handler de negócio, conexão PostgreSQL, integração SQS, parâmetros de lote e testes AWS-01–AWS-07 permanecem decisões de mudanças posteriores.
