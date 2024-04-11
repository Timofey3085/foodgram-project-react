[![Main Foodgram workflow](https://github.com/Timofey3085/foodgram-project-react/actions/workflows/main.yml/badge.svg)](https://github.com/Timofey3085/foodgram-project-react/actions/workflows/main.yml)
## ОПИСАНИЕ ПРОЕКТА 

# Foodgram — онлайн-сервис для обмена кулинарными рецептами и нахождения новых кулинарных идей.

# https://foodgramshop.ddns.net/

Технологии
Python 3.9
Django 3.2.3
Node.js 13.12.0
React 17.0.1
PostgreSQL 13
Gunicorn 21.2.0
Nginx
Docker

# Установка и запуск для удалённого сервера на Linux

# Установка Docker на Linux

Cамый простой способ установить Docker на Linux — скачать и выполнить официальный скрипт. Для этого поочерёдно выполните в терминале следующие команды:

Скачайте и установите curl — консольную утилиту, которая умеет скачивать файлы по команде пользователя:
```bash
sudo apt update
sudo apt install curl
```
С помощью утилиты curl скачайте скрипт для установки докера с официального сайта:
``` bash
curl -fSL https://get.docker.com -o get-docker.sh
```
Запустите сохранённый скрипт с правами суперпользователя:
```bash
sudo sh ./get-docker.sh
```
# Запуск проекта
Для запуска необходим установленный Docker

Создайте каталок для проекта и войдите в него:
```bash
mkdir foodgram
cd foodgram
```
Скачайте файл docker-compose.production.yml
```bash
curl -o docker-compose.production.yml https://raw.githubusercontent.com/Timofey3085/foodgram-project-react/main/docker-compose.production.yml
```
Скачайте файл .env и отредактируйте его:
```bash
curl -o .env https://github.com/Timofey3085/foodgram-project-react/main/.env.example
nano .env
```
# Скачайте и запустите проект:
```bash
sudo docker compose -f docker-compose.production.yml pull
sudo docker compose -f docker-compose.production.yml down
sudo docker compose -f docker-compose.production.yml up -d
```
# Сделайте миграцию для базы данных:
```bash
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
```
# Соберите статику и копируйте в каталог со статикой:
```bash
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
sudo docker compose -f docker-compose.production.yml exec backend mkdir -p /static/static/
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/static/. /static/static/
```
# Запуск проекта с файлов репозитория
Клонируйте репозиторий:
```bash
git clone https://github.com/Timofey3085/foodgram-project-react.git
```
# Запустите проект:
```bash
sudo docker compose -f docker-compose.yml down
sudo docker compose -f docker-compose.yml up -d
```
# Сделайте миграцию для базы данных:
```bash
sudo docker compose -f docker-compose.yml exec backend python manage.py migrate
```
# Соберите статику и копируйте в каталог со статикой:
```bash
sudo docker compose -f docker-compose.yml exec backend python manage.py collectstatic
sudo docker compose -f docker-compose.yml exec backend mkdir -p /static/static/
sudo docker compose -f docker-compose.yml exec backend cp -r /app/static/. /static/static/
```

Автор
[Timofey - Razborshchikov](https://github.com/Timofey3085)
