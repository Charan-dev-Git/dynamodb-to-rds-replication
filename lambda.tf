data "archive_file" "user_processor_zip" {
  type        = "zip"
  source_dir  = "${path.module}/lambda/user_processor"
  output_path = "${path.module}/lambda/user_processor.zip"
}

data "archive_file" "replicator_zip" {
  type        = "zip"
  source_dir  = "${path.module}/lambda/replicator"
  output_path = "${path.module}/lambda/replicator.zip"
}

resource "aws_lambda_function" "user_processor" {
  function_name = local.user_processor_lambda
  role          = aws_iam_role.user_processor_role.arn
  handler       = "app.lambda_handler"
  runtime       = "python3.12"
  filename      = data.archive_file.user_processor_zip.output_path
  source_code_hash = data.archive_file.user_processor_zip.output_base64sha256
  timeout       = 30

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.users.name
    }
  }

  tags = {
    Name    = local.user_processor_lambda
    Project = var.project_name
  }
}

resource "aws_lambda_function" "replicator" {
  function_name = local.replicator_lambda
  role          = aws_iam_role.replicator_role.arn
  handler       = "app.lambda_handler"
  runtime       = "python3.12"
  filename      = data.archive_file.replicator_zip.output_path
  source_code_hash = data.archive_file.replicator_zip.output_base64sha256
  timeout       = 120

  environment {
    variables = {
      SECRET_NAME = aws_secretsmanager_secret.rds_secret.name
    }
  }

  tags = {
    Name    = local.replicator_lambda
    Project = var.project_name
  }
}

resource "aws_lambda_event_source_mapping" "dynamodb_stream_to_replicator" {
  event_source_arn  = aws_dynamodb_table.users.stream_arn
  function_name     = aws_lambda_function.replicator.arn
  starting_position = "LATEST"
  batch_size        = 10
}