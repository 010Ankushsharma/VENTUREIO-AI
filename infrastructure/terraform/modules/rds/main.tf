variable "environment" { type = string }
variable "vpc_id" { type = string }
variable "subnet_ids" { type = list(string) }

resource "aws_db_subnet_group" "main" {
  name       = "ventureiq-${var.environment}"
  subnet_ids = var.subnet_ids
}

resource "aws_db_instance" "postgres" {
  identifier           = "ventureiq-${var.environment}"
  engine               = "postgres"
  engine_version       = "16.3"
  instance_class       = "db.t3.medium"
  allocated_storage    = 100
  storage_encrypted    = true
  db_name              = "ventureiq"
  username             = "ventureiq"
  password             = "CHANGE_ME_IN_SECRETS_MANAGER"
  db_subnet_group_name = aws_db_subnet_group.main.name
  skip_final_snapshot  = false

  tags = { Environment = var.environment }
}

output "endpoint" { value = aws_db_instance.postgres.endpoint }
