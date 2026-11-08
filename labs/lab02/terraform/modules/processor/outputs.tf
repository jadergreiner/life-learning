output "function_name" {
  description = "Nome da função Lambda preparatória."
  value       = aws_lambda_function.processor.function_name
}

output "function_arn" {
  description = "ARN da função Lambda preparatória."
  value       = aws_lambda_function.processor.arn
}

output "execution_role_arn" {
  description = "ARN da execution role da função Lambda."
  value       = aws_iam_role.processor.arn
}

output "log_group_name" {
  description = "Nome do log group CloudWatch da função."
  value       = aws_cloudwatch_log_group.processor.name
}
