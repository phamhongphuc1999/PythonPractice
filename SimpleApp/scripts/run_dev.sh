#! /bin/bash

Green='\033[0;32m'
NC='\033[0m'

CONTAINER_NAME="sanic_simple_app_container"
SQL_CONTAINER_NAME="dev_sanic_sql_container"
CROSS_CHAIN_NETWORK="sanic_simple_network"

printf "${Green}Step dev1: Create cross chain network${NC}\n"
if [ "$(docker network ls -q -f name=$CROSS_CHAIN_NETWORK)" ]
then
  echo "Network is already exist. Skip create!!!"
else
  docker network create $CROSS_CHAIN_NETWORK
fi

printf "${Green}Step dev2: Run mysql database container${NC}\n"
if [ "$(docker ps -q -f name=$SQL_CONTAINER_NAME)" ]
then
  echo "mysql database container is already exist"
  if [ "$(docker ps -aq -f status=exited -f name=$SQL_CONTAINER_NAME)" ]
  then
    docker start $SQL_CONTAINER_NAME
  fi
else
  docker-compose -f docker-compose-mysql.yaml up -d
fi

printf "${Green}Step dev3: Build and run app container${NC}\n"
./scripts/run.sh -e dev_docker

printf "${Green}Step dev4: Connect sql container to cross chain network${NC}\n"
if [ "$(docker container inspect "$SQL_CONTAINER_NAME" --format='{{json .NetworkSettings.Networks.'$CROSS_CHAIN_NETWORK'}}')" == "null" ]
then
  docker network connect "$CROSS_CHAIN_NETWORK" "$SQL_CONTAINER_NAME"
fi

printf "${Green}step dev5: Connect bridge container to cross chain network${NC}\n"
if [ "$(docker container inspect "$CONTAINER_NAME" --format='{{json .NetworkSettings.Networks.'$CROSS_CHAIN_NETWORK'}}')" == "null" ]
then
  docker network connect "$CROSS_CHAIN_NETWORK" "$CONTAINER_NAME"
fi
