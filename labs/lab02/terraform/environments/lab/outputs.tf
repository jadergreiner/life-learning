output "aws_account_id" {
  description = "Account ID autenticado e validado contra a variável aprovada."
  value       = data.aws_caller_identity.current.account_id
}

output "aws_region" {
  description = "Região AWS usada pelo provider."
  value       = data.aws_region.current.region
}

output "queue_name" {
  description = "Nome da fila principal SQS Standard."
  value       = module.queue.queue_name
}

output "queue_url" {
  description = "URL da fila principal SQS Standard."
  value       = module.queue.queue_url
}

output "queue_arn" {
  description = "ARN da fila principal SQS Standard."
  value       = module.queue.queue_arn
}

output "dead_letter_queue_name" {
  description = "Nome da DLQ SQS Standard."
  value       = module.queue.dead_letter_queue_name
}

output "dead_letter_queue_url" {
  description = "URL da DLQ SQS Standard."
  value       = module.queue.dead_letter_queue_url
}

output "dead_letter_queue_arn" {
  description = "ARN da DLQ SQS Standard."
  value       = module.queue.dead_letter_queue_arn
}

output "processor_function_name" {
  description = "Nome da função Lambda preparatória do LAB02."
  value       = module.processor.function_name
}

output "processor_function_arn" {
  description = "ARN da função Lambda preparatória do LAB02."
  value       = module.processor.function_arn
}

output "processor_execution_role_arn" {
  description = "ARN da execution role de logging da função preparatória."
  value       = module.processor.execution_role_arn
}

output "processor_log_group_name" {
  description = "Nome do log group da função preparatória."
  value       = module.processor.log_group_name
}

output "database_identifier" {
  description = "Identificador da instância RDS PostgreSQL."
  value       = module.database.identifier
}

output "database_arn" {
  description = "ARN da instância RDS PostgreSQL."
  value       = module.database.arn
}

output "database_endpoint" {
  description = "Endpoint DNS privado do RDS; ainda sem conectividade de aplicação."
  value       = module.database.endpoint
}

output "database_port" {
  description = "Porta PostgreSQL do RDS."
  value       = module.database.port
}

output "database_name" {
  description = "Nome inicial do database PostgreSQL."
  value       = module.database.database_name
}

output "database_master_user_secret_arn" {
  description = "ARN do secret master gerenciado pelo RDS; nenhum valor de credencial é exposto."
  value       = module.database.master_user_secret_arn
}

output "database_security_group_id" {
  description = "Security group dedicado do RDS, sem regras ingress nesta mudança."
  value       = module.database.security_group_id
}
