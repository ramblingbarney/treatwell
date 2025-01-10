# Create a Security Group
resource "aws_security_group" "ditwl-sg-ecs-color-app" {
  name   = "ditwl-sg-ecs-color-app"
  vpc_id = aws_vpc.ditlw-vpc.id
}

# Allow access from the Intert to port 8008
resource "aws_security_group_rule" "ditwl-sr-internet-to-ecs-color-app-8080" {
  security_group_id = aws_security_group.ditwl-sg-ecs-color-app.id
  type              = "ingress"
  from_port         = 5000
  to_port           = 5000
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"] # Internet
}

# Allow all outbound traffic to Internet
resource "aws_security_group_rule" "ditwl-sr-all-outbund" {
  security_group_id = aws_security_group.ditwl-sg-ecs-color-app.id
  type              = "egress"
  from_port         = "0"
  to_port           = "0"
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
}
