# <img src="https://avatars.githubusercontent.com/u/82920648?v=4" width="30" height="30"> trampoja.com
> Status: Developing

[![NPM](https://img.shields.io/badge/license-proprietary-red)](https://github.com/TrampoJa/api.trampoja.com/LICENSE)

## Indice:
- [Sobre](#-sobre)
- [Tecnologias utilizadas](#-Tecnologias-utilizadas)
- [Setup](#-setup)


## Sobre
### Software que aproxima o contratante do contratado


## Tecnologias utilizadas

* [Python](https://www.python.org/downloads/release/python-389/)
* [PostgreSQL](https://www.postgresql.org/)
* [Django](https://www.djangoproject.com/)


## Setup

> instale: curl git redis-server build-essential checkinstall libreadline-gplv2-dev libncursesw5-dev libssl-dev
           libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev nodejs
```bash
# instalando python 3.8
$ cd /opt
$ wget https://www.python.org/ftp/python/3.8.7/Python-3.8.7.tgz
$ tar xzf Python-3.8.7.tgz
$ cd Python-3.8.7
$ ./configure --enable-optimizations
$ make altinstall

# Instalando pip para o python 3.8
$ cd /tmp
$ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
$ python3.8 get-pip.py

# Criando o diretório e clonando os repositórios
$ mkdir -p ~/.www
$ cd ~/.www
$ git clone https://github.com/TrampoJa/api.trampoja.com

# Instalando virtual env e bibliotecas para o python
$ cd ~/.www/api.trampoja.com
$ pip3.8 install virtualenv
$ virtualenv env
$ source env/bin/activate
$ pip3.8 install -U django djangorestframework httpie pillow requests django-cors-headers gunicorn redis celery
$ deactivate

$ apt install postgresql postgresql-contrib
$ su - postgres

$ psql
$ CREATE DATABASE trampoja;
$ CREATE USER tj_user WITH PASSWORD 'Gtr400@@';
$ ALTER ROLE tj_user SET client_encoding TO 'utf8';
$ ALTER ROLE tj_user SET default_transaction_isolation TO 'read committed';
$ ALTER ROLE tj_user SET timezone TO 'UTC';
$ GRANT ALL PRIVILEGES ON DATABASE trampoja TO tj_user;
```
