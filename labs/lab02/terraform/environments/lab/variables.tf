variable "aws_region" {
  description = "Região AWS aprovada para este ambiente do LAB02."
  type        = string
  default     = "us-east-1"
}

variable "aws_profile" {
  description = "Nome do perfil AWS CLI autorizado."
  type        = string
  default     = "default"
}

variable "approved_account_id" {
  description = "Account ID esperado, validado contra STS antes de planejar a fila."
  type        = string

  validation {
    condition     = can(regex("^[0-9]{12}$", var.approved_account_id))
    error_message = "approved_account_id deve conter exatamente 12 dígitos."
  }
}

variable "queue_name_prefix" {
  description = "Prefixo para a fila SQS principal; a DLQ recebe o sufixo -dlq."
  type        = string
}

variable "message_retention_seconds" {
  description = "Retenção da fila principal em segundos."
  type        = number
}

variable "dlq_message_retention_seconds" {
  description = "Retenção da DLQ em segundos."
  type        = number
}

variable "visibility_timeout_seconds" {
  description = "Visibility timeout da fila principal em segundos."
  type        = number
}

variable "receive_wait_time_seconds" {
  description = "Long polling da fila principal em segundos."
  type        = number
}

variable "max_receive_count" {
  description = "Número de recebimentos sem sucesso antes do redrive para a DLQ."
  type        = number
}
