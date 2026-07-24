variable "environment" { type = string }
variable "vpc_id" { type = string }
variable "subnet_ids" { type = list(string) }

resource "aws_ecs_cluster" "main" {
  name = "ventureiq-${var.environment}"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

output "cluster_name" { value = aws_ecs_cluster.main.name }
