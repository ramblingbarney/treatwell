[
  {
    "name": "treatwellapi",
    "image": "${aws_ecr_repository}:${tag}",
    "essential": true,
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-region": "eu-west-2",
        "awslogs-stream-prefix": "treatwellapi-staging-service",
        "awslogs-group": "awslogs-treatwellapi-staging"
      }
    },
    "portMappings": [
      {
        "containerPort": ${app_port},
        "hostPort": ${app_port},
        "protocol": "tcp"
      }
    ],
    "cpu": 1,
    "environment": [
      {
        "name": "CATEGORIES",
        "value": "${categories}"
      }, 
      {
        "name": "API_URL",
        "value": "${api_url}"
      },
      {
        "name": "BUCKET",
        "value": "${bucket_name}"
      },
      {
        "name": "PORT",
        "value": "${app_port}"
      }
    ],
    "ulimits": [
      {
        "name": "nofile",
        "softLimit": 65536,
        "hardLimit": 65536
      }
    ],
    "mountPoints": [],
    "memory": ${memory},
    "volumesFrom": []
  }
]