<div align="center">

Very simple Spark interact to Kafka

</div>

### Setup

1. Create python environment

#### Create python virtual environment and prepare data

```shell
python3 -m venv ./venv
source ./venv/bin/activate
```

#### Install package

```shell
pip3 install -r requirements.txt
```

#### Create .env file with same .env.sample format. You can copy .env.sample by following command

```shell
cp .env.sample .env
```

#### Except all sh file

```shell
chmod +x script/*.sh
```

#### Download NASA logging data

```shell
./script/prepare.sh
```

2. Run kafka cluster written by docker

```shell
docker-compose up -d
```

3. Run simple demo spark

```shell
./script/run.sh
```
