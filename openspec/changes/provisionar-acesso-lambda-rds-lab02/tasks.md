## 1. Terraform de rede e Lambda

- [x] 1.1 Expor do módulo database a AZ do RDS e adicionar regra ingress PostgreSQL com origem no SG informado da Lambda
- [x] 1.2 Criar SG Lambda sem ingress e com egress TCP/5432 ao SG do RDS; descobrir subnet default na AZ do banco
- [x] 1.3 Configurar VPC da Lambda e anexar política gerenciada AWSLambdaVPCAccessExecutionRole

## 2. IAM e documentação

- [x] 2.1 Atualizar políticas locais do deployer para regras SG, configuração VPC e attachment controlado da política Lambda VPC
- [x] 2.2 Atualizar documentação dos módulos e do root para o caminho privado e seus limites

## 3. Revisão e provisionamento

- [x] 3.1 Validar formatação e revisar Terraform plan contra escopo e ausência de substituição do RDS
- [x] 3.2 Aplicar conectividade AWS e confirmar configuração VPC e regras efetivas
