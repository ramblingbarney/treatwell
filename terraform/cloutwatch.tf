resource "aws_cloudwatch_log_group" "treatwellapi" {
  name = "awslogs-treatwellapi-staging"

  tags = {
    Environment = "staging"
    Application = "treatwellapi"
  }
}