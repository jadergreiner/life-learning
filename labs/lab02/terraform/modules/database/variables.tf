variable "identifier" {
  description = "Identificador da instância RDS do LAB02."
  type        = string
  default     = "lab02-postgres"

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{0,61}[a-z0-9]$|^[a-z]$", var.identifier)) && !strcontains(var.identifier, "--")
    error_message = "identifier deve começar com letra minúscula, conter somente letras, números e hífens, não terminar em hífen e não conter hífens duplos."
  }
}

variable "database_name" {
  description = "Nome inicial do database PostgreSQL; não cria schema ou tabelas."
  type        = string
  default     = "lab02"

  validation {
    condition     = can(regex("^[A-Za-z][A-Za-z0-9_]{0,62}$", var.database_name))
    error_message = "database_name deve começar com letra e conter até 63 letras, números ou underscores."
  }
}

variable "master_username" {
  description = "Nome do usuário master. A senha é gerada e gerenciada pelo RDS em Secrets Manager."
  type        = string
  default     = "lab02_admin"

  validation {
    condition     = can(regex("^[A-Za-z][A-Za-z0-9_]{0,15}$", var.master_username))
    error_message = "master_username deve começar com letra e conter até 16 letras, números ou underscores."
  }
}

variable "engine_version" {
  description = "Versão do PostgreSQL RDS, verificada para disponibilidade regional antes do apply."
  type        = string
  default     = "16.15"

  validation {
    condition     = can(regex("^[0-9]+\\.[0-9]+(-rds\\.[0-9]+)?$", var.engine_version))
    error_message = "engine_version deve ser uma versão PostgreSQL RDS completa, como 16.15."
  }
}

variable "instance_class" {
  description = "Classe da instância RDS; verificar orderability e custo na região antes do apply."
  type        = string
  default     = "db.t4g.micro"

  validation {
    condition     = can(regex("^db\\.[a-z0-9]+\\.[a-z0-9]+$", var.instance_class))
    error_message = "instance_class deve usar o formato db.<family>.<size>."
  }
}

variable "allocated_storage_gib" {
  description = "Armazenamento gp3 inicial em GiB."
  type        = number
  default     = 20

  validation {
    condition     = var.allocated_storage_gib >= 20 && var.allocated_storage_gib <= 65536 && floor(var.allocated_storage_gib) == var.allocated_storage_gib
    error_message = "allocated_storage_gib deve ser um inteiro entre 20 e 65536 GiB."
  }
}

variable "backup_retention_days" {
  description = "Dias de retenção dos backups automatizados."
  type        = number
  default     = 1

  validation {
    condition     = var.backup_retention_days >= 1 && var.backup_retention_days <= 35 && floor(var.backup_retention_days) == var.backup_retention_days
    error_message = "backup_retention_days deve ser um inteiro entre 1 e 35."
  }
}

variable "deletion_protection" {
  description = "Proteção contra exclusão acidental da instância. Desabilitar somente em procedimento explícito de teardown."
  type        = bool
  default     = true
}

variable "lambda_security_group_id" {
  description = "Security group da Lambda autorizada a conectar ao PostgreSQL do LAB02."
  type        = string
}

variable "final_snapshot_identifier" {
  description = "Identificador do snapshot final. Atualize para um nome único antes de cada novo ciclo de teardown/recriação."
  type        = string
  default     = "lab02-postgres-final-20261108"

  validation {
    condition     = length(var.final_snapshot_identifier) <= 255 && can(regex("^[a-z][a-z0-9-]*[a-z0-9]$|^[a-z]$", var.final_snapshot_identifier)) && !strcontains(var.final_snapshot_identifier, "--")
    error_message = "final_snapshot_identifier deve começar por letra minúscula, usar letras/números/hífens, não terminar em hífen e não conter hífens duplos."
  }
}
