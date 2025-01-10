resource "aws_ecr_repository" "repo" {
  name                 = var.client_name
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_lifecycle_policy" "repo-policy" {
  repository = aws_ecr_repository.repo.name

  policy = <<EOF
{
  "rules": [
    {
      "rulePriority": 1,
      "description": "Keep image deployed with tag latest",
      "selection": {
        "tagStatus": "tagged",
        "tagPrefixList": ["latest"],
        "countType": "imageCountMoreThan",
        "countNumber": 1
      },
      "action": {
        "type": "expire"
      }
    },
    {
      "rulePriority": 2,
      "description": "Keep last 2 any images",
      "selection": {
        "tagStatus": "any",
        "countType": "imageCountMoreThan",
        "countNumber": 2
      },
      "action": {
        "type": "expire"
      }
    }
  ]
}
EOF
}

resource "null_resource" "push" {
  provisioner "local-exec" {
    command     = "${var.push_path} ${var.docker_path} ${aws_ecr_repository.repo.repository_url} ${var.tag}"
    interpreter = ["bash", "-c"]
  }
}

# Create an ECS Cluster
resource "aws_ecs_cluster" "ditwl-ecs-01" {
  name = "ditwl-ecs-01"
}

data "template_file" "treatwellapp" {
  template = file("./templates/treatwellapp.json.tpl")
  vars = {
    aws_ecr_repository = aws_ecr_repository.repo.repository_url
    tag                = "latest"
    app_port           = var.app_port
    bucket_name        = var.bucket_name
    categories         = var.categories
    api_url            = var.api_url
    memory             = var.service_memory
  }
}

# ECS Task definition (Define infrastructure and container images)
resource "aws_ecs_task_definition" "ditwl-ecs-td-color-app" {
  family                   = "service"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.service_cpu    # Number of cpu units 1024 units = 1 vCPU
  memory                   = var.service_memory # Amount (in MiB)
  container_definitions    = data.template_file.treatwellapp.rendered
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn
}

# ECS Service 
resource "aws_ecs_service" "ditwl-ecs-serv-color-app" {
  name            = "ditwl-ecs-serv-color-app"
  cluster         = aws_ecs_cluster.ditwl-ecs-01.id
  task_definition = aws_ecs_task_definition.ditwl-ecs-td-color-app.arn
  launch_type     = "FARGATE"
  desired_count   = 1
  network_configuration {
    subnets          = [aws_subnet.ditwl-sn-za-pro-pub-00.id]
    assign_public_ip = "true"
    security_groups  = [aws_security_group.ditwl-sg-ecs-color-app.id]
  }
}
