output "dynamodb_table_name" {
  value = local.dynamodb_table_name
}

output "rds_secret_name" {
  value = local.rds_secret_name
}

output "user_processor_lambda_name" {
  value = local.user_processor_lambda
}

output "replicator_lambda_name" {
  value = local.replicator_lambda
}