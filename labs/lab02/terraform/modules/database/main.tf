data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

data "aws_subnet" "default" {
  for_each = toset(data.aws_subnets.default.ids)
  id       = each.value
}

locals {
  default_subnet_availability_zones = toset([
    for subnet in data.aws_subnet.default : subnet.availability_zone
  ])
}

resource "aws_db_subnet_group" "database" {
  name        = "${var.identifier}-subnets"
  description = "Subnets default usadas pelo banco privado do LAB02."
  subnet_ids  = data.aws_subnets.default.ids

  tags = {
    Name        = "${var.identifier}-subnets"
    Lab         = "LAB02"
    ManagedBy   = "Terraform"
    Environment = "lab"
  }

  lifecycle {
    precondition {
      condition     = length(local.default_subnet_availability_zones) >= 2
      error_message = "A VPC default precisa ter subnets em pelo menos duas Availability Zones para o DB subnet group."
    }
  }
}

resource "aws_security_group" "database" {
  name        = "${var.identifier}-database"
  description = "Banco privado do LAB02; nenhuma regra ingress nesta etapa."
  vpc_id      = data.aws_vpc.default.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.identifier}-database"
    Lab         = "LAB02"
    ManagedBy   = "Terraform"
    Environment = "lab"
  }
}

resource "aws_vpc_security_group_ingress_rule" "processor_postgres" {
  security_group_id            = aws_security_group.database.id
  referenced_security_group_id = var.lambda_security_group_id
  ip_protocol                  = "tcp"
  from_port                    = 5432
  to_port                      = 5432
  description                  = "PostgreSQL somente da Lambda LAB02."
}

resource "aws_db_instance" "database" {
  identifier                      = var.identifier
  engine                          = "postgres"
  engine_version                  = var.engine_version
  instance_class                  = var.instance_class
  allocated_storage               = var.allocated_storage_gib
  storage_type                    = "gp3"
  storage_encrypted               = true
  db_name                         = var.database_name
  username                        = var.master_username
  manage_master_user_password     = true
  port                            = 5432
  multi_az                        = false
  publicly_accessible             = false
  db_subnet_group_name            = aws_db_subnet_group.database.name
  vpc_security_group_ids          = [aws_security_group.database.id]
  backup_retention_period         = var.backup_retention_days
  auto_minor_version_upgrade      = true
  deletion_protection             = var.deletion_protection
  skip_final_snapshot             = false
  final_snapshot_identifier       = var.final_snapshot_identifier
  copy_tags_to_snapshot           = true
  apply_immediately               = false
  performance_insights_enabled    = false
  monitoring_interval             = 0
  enabled_cloudwatch_logs_exports = []

  tags = {
    Name             = var.identifier
    Lab              = "LAB02"
    ManagedBy        = "Terraform"
    Environment      = "lab"
    created_by       = "rds-oss-skill"
    generation_model = "gpt-6"
  }
}
