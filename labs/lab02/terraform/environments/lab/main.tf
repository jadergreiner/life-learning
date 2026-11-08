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

module "processor" {
  source = "../../modules/processor"

  depends_on = [data.aws_caller_identity.current]
}

module "database" {
  source = "../../modules/database"

  depends_on = [data.aws_caller_identity.current]
}
