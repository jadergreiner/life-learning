variable "name_prefix" {
  description = "Prefixo base para os nomes da fila principal e da DLQ; use caracteres alfanuméricos, hífen ou sublinhado."
  type        = string

  validation {
    condition     = length(trimspace(var.name_prefix)) > 0 && length(var.name_prefix) <= 76 && can(regex("^[A-Za-z0-9_-]+$", var.name_prefix))
    error_message = "name_prefix deve ter de 1 a 76 caracteres alfanuméricos, hífen ou sublinhado."
  }
}

variable "message_retention_seconds" {
  description = "Tempo de retenção de mensagens da fila principal, em segundos (60 a 1.209.600)."
  type        = number

  validation {
    condition     = var.message_retention_seconds >= 60 && var.message_retention_seconds <= 1209600 && floor(var.message_retention_seconds) == var.message_retention_seconds
    error_message = "message_retention_seconds deve ser um inteiro entre 60 e 1.209.600 segundos."
  }
}

variable "dlq_message_retention_seconds" {
  description = "Tempo de retenção de mensagens da DLQ, em segundos (60 a 1.209.600)."
  type        = number

  validation {
    condition     = var.dlq_message_retention_seconds >= 60 && var.dlq_message_retention_seconds <= 1209600 && floor(var.dlq_message_retention_seconds) == var.dlq_message_retention_seconds
    error_message = "dlq_message_retention_seconds deve ser um inteiro entre 60 e 1.209.600 segundos."
  }
}

variable "visibility_timeout_seconds" {
  description = "Tempo de invisibilidade após recebimento, em segundos (0 a 43.200). Ajuste ao consumidor que será definido posteriormente."
  type        = number

  validation {
    condition     = var.visibility_timeout_seconds >= 0 && var.visibility_timeout_seconds <= 43200 && floor(var.visibility_timeout_seconds) == var.visibility_timeout_seconds
    error_message = "visibility_timeout_seconds deve ser um inteiro entre 0 e 43.200 segundos."
  }
}

variable "receive_wait_time_seconds" {
  description = "Tempo de long polling para a fila principal, em segundos (0 a 20); valores maiores que zero habilitam long polling."
  type        = number
  default     = 20

  validation {
    condition     = var.receive_wait_time_seconds >= 0 && var.receive_wait_time_seconds <= 20 && floor(var.receive_wait_time_seconds) == var.receive_wait_time_seconds
    error_message = "receive_wait_time_seconds deve ser um inteiro entre 0 e 20 segundos."
  }
}

variable "max_receive_count" {
  description = "Número de recebimentos sem sucesso antes de mover a mensagem para a DLQ."
  type        = number

  validation {
    condition     = var.max_receive_count >= 1 && var.max_receive_count <= 1000 && floor(var.max_receive_count) == var.max_receive_count
    error_message = "max_receive_count deve ser um inteiro entre 1 e 1.000."
  }
}
