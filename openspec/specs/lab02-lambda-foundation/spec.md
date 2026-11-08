# lab02-lambda-foundation Specification

## Purpose
Define a função Lambda preparatória do LAB02, com pacote ZIP reproduzível, role restrita a logging e sem integrações de aplicação.

## Requirements
### Requirement: Módulo processor provisiona uma função Lambda preparatória
O módulo Terraform `labs/lab02/terraform/modules/processor` SHALL provisionar uma única função `lab02-processor`, empacotável e invocável, sem processamento de negócio ou efeitos externos.

#### Scenario: Configuração mínima da função
- **WHEN** o root module planeja uma configuração válida do módulo processor
- **THEN** o plano contém uma função Lambda ZIP com runtime `python3.14`, handler `lambda_function.handler`, memória de 128 MB e timeout de 3 segundos

#### Scenario: Invocação preparatória
- **WHEN** a função recebe uma invocação direta
- **THEN** o handler retorna somente `{"status":"ready"}` e não processa mensagens, registra o evento ou altera estado externo

#### Scenario: Saídas da função
- **WHEN** a função é provisionada
- **THEN** o módulo expõe o nome e o ARN da função e o ARN da execution role

### Requirement: Pacote de implantação reproduzível
O módulo processor SHALL construir localmente um ZIP sem dependências externas que contenha o handler no caminho exigido pelo runtime e calcular seu hash para detectar alteração de código.

#### Scenario: Pacote gerado durante o plan
- **WHEN** Terraform cria o plano para o módulo processor
- **THEN** o arquivo ZIP contém `lambda_function.py` na raiz e permanece disponível no mesmo caminho até o apply

#### Scenario: Artefato local não versionado
- **WHEN** o pacote de implantação é gerado
- **THEN** o ZIP permanece ignorado pelo Git e o código-fonte do handler permanece versionável

### Requirement: Execution role restrita a logging
A função SHALL usar uma execution role cujo principal de confiança seja somente o serviço Lambda e cujas permissões se limitem à gravação de logs para a função.

#### Scenario: Função grava logs
- **WHEN** uma invocação da função registra saída operacional
- **THEN** Lambda consegue criar streams e escrever no log group da função

#### Scenario: Ausência de permissões de aplicação
- **WHEN** a execution role é inspecionada
- **THEN** ela não concede ações SQS, RDS, Secrets Manager, EC2/VPC ou outras permissões de aplicação

### Requirement: Logs com retenção limitada
O módulo processor SHALL criar o log group `/aws/lambda/lab02-processor` antes da função, com retenção configurável e default de 7 dias.

#### Scenario: Retenção configurada
- **WHEN** o plano é gerado sem override de retenção
- **THEN** o log group é criado com retenção de 7 dias e nenhuma política de log sem expiração

### Requirement: Integrações são adiadas
A função preparatória SHALL permanecer sem trigger, event source mapping SQS ou configuração de rede/banco.

#### Scenario: Plano sem integrações externas
- **WHEN** o plano do módulo processor é revisado
- **THEN** não há event source mapping, permissão de leitura SQS, integração RDS/PostgreSQL, VPC, URL pública, segredo ou produtor
