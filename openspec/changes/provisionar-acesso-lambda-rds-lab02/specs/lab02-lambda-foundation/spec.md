## MODIFIED Requirements

### Requirement: Execution role restrita a logging
A função SHALL usar uma execution role cujo principal de confiança seja somente o serviço Lambda e cujas permissões se limitem a gravação de logs e ao gerenciamento de ENIs necessário à configuração VPC.

#### Scenario: Função grava logs
- **WHEN** uma invocação da função registra saída operacional
- **THEN** Lambda consegue criar streams e escrever no log group da função

#### Scenario: Permissões VPC mínimas
- **WHEN** a execution role é inspecionada
- **THEN** ela possui somente a política gerenciada `AWSLambdaVPCAccessExecutionRole` para operações de ENI além das permissões de logs, sem ações SQS, RDS, Secrets Manager ou permissões adicionais de aplicação

### Requirement: Integrações são adiadas
A função preparatória SHALL permanecer sem trigger ou event source mapping SQS, mas poderá ter configuração VPC restrita à conectividade privada com o RDS do LAB02; não terá credenciais de aplicação.

#### Scenario: Rede configurada sem processamento
- **WHEN** o plano do módulo processor é revisado
- **THEN** a função usa subnet da mesma AZ do RDS e SG sem ingress com egress somente TCP/5432 ao SG do banco, sem event source mapping, permissão de leitura SQS, URL pública, segredo ou produtor
