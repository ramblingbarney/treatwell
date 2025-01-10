# Treatwell (Data Platform Engineer)

As a data platform engineer, I would like to build a scalable data ingestion application for the "Movie Insights" project.

## Prerequisites

* [Python3](https://www.python.org/)
* [Homebrew](https://docs.brew.sh)
* [Git](https://git-scm.com/downloads)
* create environment variables file (do_not_commit.sh) in the root directory and run these 2 bash commands
    * ```echo 'export CATEGORIES="action-adventure,animation,classic,comedy,drama,horror,family,mystery,scifi-fantasy,western"\n' >> do_not_commit.sh```
    * ```echo 'export API_URL="https://api.sampleapis.com/movies"\n' >> do_not_commit.sh```
    * ```echo 'export BUCKET="movies-raw"\n' >> do_not_commit.sh```

## Installation

* ```git clone git@github.com:ramblingbarney/treatwell.git```
* ```brew install python@3.13```
* ```brew install awscli```
* ```brew install terraform```
* ```python3.13 -m venv .venv```
* ```source .venv/bin/activate```
* ```export PYTHONPATH=.```
* ```pip3 install -r requirements.txt```
* ```pip3 install -r requirements.dev.txt```
* ```source do_not_commit.sh```

### Running Tests
  * ```source do_not_commit.sh``` 
  * ```export PYTHONPATH=.```
  * ```pytest tests/```
  * ```coverage run -m pytest && coverage report```

## Deployment

Create AWS user with programmatic access and configure awscli credentials (secret_access_key, access_key).  Assign this user permissions to

* "ecr:*"
* "s3:*"
* "ec2:*"
*	"iam:*",
* "logs:*",
* "ecs:*",
* "elasticloadbalancing:*",
* 
### Terraform

* ```cd terraform```
* ```terraform init```
* ```terraform apply```

### Docker

#### Login

  * ```aws ecr get-login-password --region <aws region> | docker login --username AWS --password-stdin <aws account id>.dkr.ecr.eu-west-2.amazonaws.com``` 

#### Manual Build Image & Push to AWS ECR

  * ```docker build -t treatwell .``` 
  * ```docker images``` # find image tag id
  * ```docker tag f8eeabc78619 <aws account id>.dkr.ecr.eu-west-2.amazonaws.com/treatwell:latest``` 
  * ```docker push <aws account id>.dkr.ecr.eu-west-2.amazonaws.com/treatwell:latest``` 

#### Automatic Build Image & Push to AWS ECR via Terraform

See Terraform ```push.sh``` 

## Automated Execution Schedule

Application will run at 1am everyday(ToDo)

## Run Locally Without Docker & Execute Movie Categories Processing

Run in terminal ```python -m app```

[Open browser URL](http://127.0.0.1:5000)

## Run Locally With Docker

  * ```docker run -d -p 5000:5000 -e AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID> -e AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY> treatwell:latest``` 
