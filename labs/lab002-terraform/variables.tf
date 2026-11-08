variable "bucket_prefix" {
  description = "Prefixo curto usado para derivar o nome do bucket S3."
  type        = string

  validation {
    condition = (
      length(var.bucket_prefix) > 0 &&
      can(regex("^[a-z0-9]([a-z0-9-]*[a-z0-9])?$", var.bucket_prefix)) &&
      length(var.bucket_prefix) <= 63 - 17 - length(var.region)
    )
    error_message = "Use um prefixo em minúsculas, com letras, números e hífens, sem hífen no início/fim; ele deve caber no limite de 63 caracteres com a conta e a região."
  }
}

variable "region" {
  description = "Região AWS do laboratório."
  type        = string
  default     = "us-east-1"

  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.region)) && length(var.region) > 0
    error_message = "A região deve ser um identificador AWS em minúsculas, contendo letras, números e hífens."
  }
}
