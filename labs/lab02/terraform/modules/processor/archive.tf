data "archive_file" "processor" {
  type             = "zip"
  source_file      = "${path.module}/lambda_function.py"
  output_path      = "${path.module}/lambda_function.zip"
  output_file_mode = "0644"
}
