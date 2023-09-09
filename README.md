# Telegram bridge to chatGPT

## Configuration
```sh
mv .env.dist .env
```
set BOT_TOKEN in **.env**

set LISUM_URL in **.env**
## Install dependencies
```sh
poetry install
```

## Run
```sh
poetry run python -m lisum_bot
```
or
```sh
. start
```

## Build and run with Docker
```sh
docker build -t lisum-bot .
docker run -d lisum-bot
```

## Build and run with Docker-compose
```sh
docker-compose up -d --force-recreate
```

## Misc
### Install docker
```sh
apt install -y wget
wget -qO- https://get.docker.com/ | sh
```

### Update pip
```sh
pip install -U pip
```

### Install poetry
```sh
pip install poetry
```

### Load all from .env
```sh
set -o allexport && source .env && set +o allexport
```
