output "identifier" {
  description = "Identificador da instância RDS."
  value       = aws_db_instance.database.identifier
}

output "arn" {
  description = "ARN da instância RDS PostgreSQL."
  value       = aws_db_instance.database.arn
}

output "resource_id" {
  description = "Resource ID do RDS."
  value       = aws_db_instance.database.resource_id
}

output "endpoint" {
  description = "Endpoint DNS privado do RDS."
  value       = aws_db_instance.database.address
}

output "port" {
  description = "Porta PostgreSQL do RDS."
  value       = aws_db_instance.database.port
}

output "database_name" {
  description = "Nome inicial do database PostgreSQL."
  value       = aws_db_instance.database.db_name
}

output "master_user_secret_arn" {
  description = "ARN do secret gerenciado pelo RDS; não contém o valor da credencial."
  value       = aws_db_instance.database.master_user_secret[0].secret_arn
}

output "subnet_group_name" {
  description = "DB subnet group da instância."
  value       = aws_db_subnet_group.database.name
}

output "security_group_id" {
  description = "Security group dedicado do banco."
  value       = aws_security_group.database.id
}

output "availability_zone" {
  description = "Availability Zone atual da instância RDS Single-AZ."
  value       = aws_db_instance.database.availability_zone
}
