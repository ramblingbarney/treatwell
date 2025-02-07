#!/bin/bash
# 
# Builds a Docker image and pushes to an AWS ECR repository

# name of the file - push.sh

set -e

docker_path="$1" # 1st argument from command line
repository_url="$2" # 2nd argument from command line
tag="${3:-latest}" # Checks if 3rd argument exists, if not, use "latest"

# splits string using '.' and picks 4th item
region="$(echo "$repository_url" | cut -d. -f4)" 

# splits string using '.' and picks 4th item
aws_account="$(echo "$repository_url" | cut -d. -f1)" 

# splits string using '/' and picks 2nd item
image_name="$(echo "$repository_url" | cut -d/ -f2)" 

# builds docker image
(cd "$docker_path" && docker build -t "$image_name" .) 

# login to ecr
# $(aws ecr get-login-password --region $region | docker login --username AWS --password-stdin ${aws_account}.dkr.ecr.${region}.amazonaws.com)


# tag image
docker tag "$image_name" "$repository_url":"$tag"

# push image
docker push "$repository_url":"$tag" 