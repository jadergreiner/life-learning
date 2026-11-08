output "bucket_name" {
  description = "Nome do bucket S3 do laboratório."
  value       = aws_s3_bucket.lab.id
}

output "bucket_arn" {
  description = "ARN do bucket S3 do laboratório."
  value       = aws_s3_bucket.lab.arn
}
