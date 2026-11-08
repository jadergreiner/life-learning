output "queue_name" {
  description = "Nome da fila principal SQS Standard."
  value       = aws_sqs_queue.main.name
}

output "queue_url" {
  description = "URL da fila principal SQS Standard."
  value       = aws_sqs_queue.main.url
}

output "queue_arn" {
  description = "ARN da fila principal SQS Standard."
  value       = aws_sqs_queue.main.arn
}

output "dead_letter_queue_name" {
  description = "Nome da DLQ SQS Standard."
  value       = aws_sqs_queue.dead_letter.name
}

output "dead_letter_queue_url" {
  description = "URL da DLQ SQS Standard."
  value       = aws_sqs_queue.dead_letter.url
}

output "dead_letter_queue_arn" {
  description = "ARN da DLQ SQS Standard."
  value       = aws_sqs_queue.dead_letter.arn
}
