variable "aws_region" {
  type        = string
  description = "The AWS region to put the bucket into"
  default     = "eu-west-2"
}

variable "client_name" {
  type        = string
  description = "client name"
  default     = "treatwell"
}

variable "docker_path" {
  type        = string
  description = "path to docker file to push to ecr"
  default     = "/home/conor/workspace/treatwell/"
}

variable "push_path" {
  type        = string
  description = "path to docker file to push to ecr"
  default     = "/home/conor/workspace/treatwell/terraform/push.sh"
}

variable "bucket_name" {
  type        = string
  description = "bucket to store raw movies data"
  default     = "movies-raw"
}

variable "categories" {
  type        = string
  description = "movie categories"
  default     = "animation,classic,comedy,drama,horror,family,mystery,western"
}

variable "api_url" {
  type        = string
  description = "base domain url for movies api"
  default     = "https://api.sampleapis.com/movies"
}


variable "tag" {
  type        = string
  description = "docker image tag"
  default     = "latest"
}

variable "az_count" {
  description = "Number of AZs to cover in a given region"
  default     = "2"
}

variable "health_check_path" {
  default = "/"
}

variable "app_port" {
  description = "Port exposed by the docker image to redirect traffic to"
  default     = 5000
}

variable "service_memory" {
  description = "ECS service memory"
  default     = 512
}

variable "service_cpu" {
  description = "ECS service CPU"
  default     = 256
}
