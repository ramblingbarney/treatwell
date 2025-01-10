provider "aws" {
  region  = var.aws_region
  profile = var.aws_profile
}

variable "aws_profile" {
  type        = string
  description = "The aws profile to be used"
  default     = "default"
}
