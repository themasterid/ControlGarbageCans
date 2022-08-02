# Control of Garbage Cans - контроль мусорных баков на предприятии (более 6000 ед.)

Control of Garbage Cans - контроль мусорных баков, учет их местоположения (используются геоданные), состояния, а так же запись в базу всех необходимых данных
для анализа и учета контейнеров на предприятии. В системе реализованы 2 системы, система для контролирующего администратора, который видит данные о состоянии контейнеров в общей системе учета
данных, вторая система рассчитана на пользователей, которые проверяют состояние и учет по месту контейнеров, где необходимо проверяющему пользователю прибыть на место расположения контейнеров
и удостоверится о наличии/состоянии/отсутствия каких либо контейнеров, с внесением необходимых данных в систему.

Система работает в облаке Яндекс, что дает стабильную работу и доступ 24/7 к данным.

# Стек
- Python 3.10
- Docker
- docker-compose
- Django 4
- CI/CD
- PostgreSQL
- Yandex.Cloud

## Запуск с использованием CI/CD

Установить docker, docker-compose на сервере виртуальной машины Yandex.Cloud:

```bash
ssh username@ip
sudo apt update && sudo apt upgrade -y && sudo apt install curl -y
sudo curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh && sudo rm get-docker.sh
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Создаем папку infra:
```bash
mkdir infra
```

- Переносим файлы docker-compose.yml, default.conf и .env на сервер в папку infra.

```bash
scp .env username@server_ip:/home/username/infra/
```
```bash
scp docker-compose.yml username@server_ip:/home/username/infra/
```
```bash
scp default.conf username@server_ip:/home/username/infra/
```

- Так же, можно создать пустой файл .env в директории infra, позже в него будем добавлять данные с git secrets:

```bash
touch .env
```

- Заполнить в настройках репозитория секреты .env

```
DB_ENGINE='django.db.backends.postgresql'
POSTGRES_DB='db_name'
POSTGRES_USER='db_user'
POSTGRES_PASSWORD='put_your_password'
DB_HOST='db'
DB_PORT='5432'
SECRET_KEY='put_your_code'
ALLOWED_HOSTS='127.0.0.1, localhost, backend, ip_server'
DEBUG=False
```

- Запускаем контейнеры находясь в папке infra:

```bash
sudo docker-compose up -d --build
```

- Затем применяем миграции, собираем статику:

```bash
sudo docker-compose exec backend python manage.py makemigrations
```
```bash
sudo docker-compose exec backend python manage.py migrate --noinput
```
```bash
sudo docker-compose exec backend python manage.py createsuperuser
```
```bash
sudo docker-compose exec backend python manage.py collectstatic --no-input
```

Загружаем данные из csv файлов в базу данных postgresql командами (TODO):

```bash
sudo docker-compose exec backend python manage.py ...
```

- Остановить:
```bash
sudo docker-compose stop/down
```

## Запуск проекта через Docker на локальной машине:

- Устанавливаем Docker на localhost, пример для Linux:

```bash
sudo apt update && sudo apt upgrade -y && sudo apt install curl -y
```
```bash
sudo curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh && sudo rm get-docker.sh
```
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
```bash
sudo chmod +x /usr/local/bin/docker-compose
```

- В папке infra переименовываем файл .env_example в .env и заполняем своими данными согласно шаблона:

```
DB_ENGINE='django.db.backends.postgresql'
POSTGRES_DB='db_name'
POSTGRES_USER='db_user'
POSTGRES_PASSWORD='put_your_password'
DB_HOST='db'
DB_PORT='5432'
SECRET_KEY='put_your_code'
ALLOWED_HOSTS='127.0.0.1, localhost, backend, ip_server'
DEBUG=False
```

- Затем в папке infra выполнить команду, запускаем контейнеры:

```bash
sudo docker-compose up -d --build
```

Для доступа к контейнеру backend выполните следующие команды, это позволит собрать статику, сделать миграции и если нужно создать администратора, для доступа в админку:

```bash
sudo docker-compose exec backend python manage.py makemigrations
```
```bash
sudo docker-compose exec backend python manage.py migrate --noinput 
```
```bash
sudo docker-compose exec backend python manage.py createsuperuser
```
```bash
sudo docker-compose exec backend python manage.py collectstatic --no-input
```

- Остановить:
```bash
sudo docker-compose stop/down
```


## Запуск проекта в dev-режиме

- Установить и активировать виртуальное окружение:

```bash
python3 -m venv venv
```
```bash
source venv/bin/activated
```

- Установить зависимости из файла requirements.txt

```bash
cd ControlGarbageCans
```
```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

- Создайте базу и пользователя в PosgreSQL:

```sql
sudo -u postgres psql
```
```sql
CREATE DATABASE basename;
```
```sql
CREATE USER username WITH ENCRYPTED PASSWORD 'password';
```
```sql
GRANT ALL PRIVILEGES ON DATABASE basename TO username;
```

- Прописываем данные для работы в dev режиме:

```
DB_ENGINE='django.db.backends.postgresql'
POSTGRES_DB='db_name'
POSTGRES_USER='db_user'
POSTGRES_PASSWORD='password'
DB_HOST='db'
DB_PORT='5432'
SECRET_KEY='put_your_code'
ALLOWED_HOSTS='127.0.0.1, localhost, backend, ip_server'
DEBUG=True
```

- Выполняем миграции, собираем статику, создаем администратора:

```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
```bash
python manage.py collectstatic --no-input
```
```bash
python manage.py createsuperuser
```

- Запускаем сервер:
```bash
python manage.py runserver localhost:80
```

Автор: [Клепиков Дмитрий](https://github.com/themasterid)
