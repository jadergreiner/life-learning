module "queue" {
  source = "../../modules/queue"

  name_prefix                   = var.queue_name_prefix
  message_retention_seconds     = var.message_retention_seconds
  dlq_message_retention_seconds = var.dlq_message_retention_seconds
  visibility_timeout_seconds    = var.visibility_timeout_seconds
  receive_wait_time_seconds     = var.receive_wait_time_seconds
  max_receive_count             = var.max_receive_count

  depends_on = [data.aws_caller_identity.current]
}

module "database" {
  source = "../../modules/database"

  lambda_security_group_id = aws_security_group.processor.id

  depends_on = [data.aws_caller_identity.current]
}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "processor_az" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }

  filter {
    name   = "availability-zone"
    values = [module.database.availability_zone]
  }
}

resource "aws_security_group" "processor" {
  name        = "lab02-processor"
  description = "Lambda LAB02 sem ingress; egress restrito ao PostgreSQL do RDS."
  vpc_id      = data.aws_vpc.default.id

  tags = {
    Name        = "lab02-processor"
    Lab         = "LAB02"
    ManagedBy   = "Terraform"
    Environment = "lab"
  }

  lifecycle {
    precondition {
      condition     = length(data.aws_subnets.processor_az.ids) > 0
      error_message = "Não existe subnet default na Availability Zone atual do RDS para associar à Lambda."
    }
  }
}

resource "aws_vpc_security_group_egress_rule" "processor_postgres" {
  security_group_id            = aws_security_group.processor.id
  referenced_security_group_id = module.database.security_group_id
  ip_protocol                  = "tcp"
  from_port                    = 5432
  to_port                      = 5432
  description                  = "PostgreSQL somente para o RDS do LAB02."
}

module "processor" {
  source = "../../modules/processor"

  subnet_ids         = data.aws_subnets.processor_az.ids
  security_group_ids = [aws_security_group.processor.id]

  depends_on = [data.aws_caller_identity.current]
}
