resource "aws_secretsmanager_secret" "rds_secret" {
  name = local.rds_secret_name

  tags = {
    Name    = local.rds_secret_name
    Project = var.project_name
  }
}

resource "aws_secretsmanager_secret_version" "rds_secret_value" {
  secret_id = aws_secretsmanager_secret.rds_secret.id

  secret_string = jsonencode({
    username = var.db_username
    password = var.db_password
    dbname   = var.db_name
    host     = aws_db_instance.users_db.address
    port     = aws_db_instance.users_db.port
  })
}