variable "function_name" {
  description = "Nome único da função Lambda preparatória do LAB02."
  type        = string
  default     = "lab02-processor"

  validation {
    condition     = can(regex("^[A-Za-z0-9_-]{1,64}$", var.function_name))
    error_message = "function_name deve ter de 1 a 64 caracteres alfanuméricos, hífen ou sublinhado."
  }
}

variable "runtime" {
  description = "Runtime gerenciado da função Lambda."
  type        = string
  default     = "python3.14"
}

variable "handler" {
  description = "Ponto de entrada do handler contido no pacote ZIP."
  type        = string
  default     = "lambda_function.handler"
}

variable "memory_size" {
  description = "Memória da função Lambda em MB."
  type        = number
  default     = 128

  validation {
    condition     = var.memory_size >= 128 && var.memory_size <= 10240 && floor(var.memory_size) == var.memory_size
    error_message = "memory_size deve ser um inteiro entre 128 e 10240 MB."
  }
}

variable "timeout_seconds" {
  description = "Timeout da função preparatória em segundos."
  type        = number
  default     = 3

  validation {
    condition     = var.timeout_seconds >= 1 && var.timeout_seconds <= 900 && floor(var.timeout_seconds) == var.timeout_seconds
    error_message = "timeout_seconds deve ser um inteiro entre 1 e 900 segundos."
  }
}

variable "log_retention_days" {
  description = "Retenção do log group Lambda em dias."
  type        = number
  default     = 7

  validation {
    condition     = contains([1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1096, 1827, 2192, 2557, 2922, 3288, 3653], var.log_retention_days)
    error_message = "log_retention_days deve ser um período de retenção aceito pelo CloudWatch Logs."
  }
}
