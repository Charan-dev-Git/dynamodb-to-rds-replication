locals {
  dynamodb_table_name     = "${var.project_name}-table"
  rds_secret_name         = "${var.project_name}-rds-secret"
  user_processor_lambda   = "${var.project_name}-user-processor"
  replicator_lambda       = "${var.project_name}-replicator"
  scheduler_name          = "${var.project_name}-schedule"
}