#! /bin/bash

Green='\033[0;32m'
NC='\033[0m'

IMAGE_NAME="sanic_simple_app"
CONTAINER_NAME="sanic_simple_app_container"
ENVIRONMENT="production"

printf "${Green}Step 1: Untag old docker image${NC}\n"
if [ "$(docker images -q $IMAGE_NAME:v1)" ]
then
  docker image tag $IMAGE_NAME:v1 $IMAGE_NAME-old:v1
  docker rmi $IMAGE_NAME:v1
fi

printf "${Green}Step 2: Build new image${NC}\n"
docker build . -t $IMAGE_NAME:v1

printf "${Green}Step 3: Stop and remove old container${NC}\n"
if [ "$(docker ps -aq -f status=running -f name=$CONTAINER_NAME)" ]
then
  docker stop $CONTAINER_NAME
fi

if [ "$(docker ps -aq -f status=exited -f name=$CONTAINER_NAME)" ]
then
  docker rm $CONTAINER_NAME
fi

printf "${Green}Step 4: Remove old image${NC}\n"
if [ "$(docker images -q $IMAGE_NAME-old:v1)" ]
then
  docker rmi $IMAGE_NAME-old:v1
fi

printf "${Green}Step 5: Run new container${NC}\n"
while getopts e: flag
do
  case "${flag}" in
      e) environment=${OPTARG};;
  esac
done

if [ "$environment" ]
then
  ENVIRONMENT=$environment
fi

printf "${Green}Step 6: Run with $ENVIRONMENT environment${NC}\n"
docker run -d -p 8000:8000 --name $CONTAINER_NAME $IMAGE_NAME:v1 "$ENVIRONMENT"

echo Finish!!
