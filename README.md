[![Main Foodgram workflow](https://github.com/Timofey3085/foodgram-project-react/actions/workflows/main.yml/badge.svg)](https://github.com/Timofey3085/foodgram-project-react/actions/workflows/main.yml)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![NodeJS](https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white) ![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) ![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white) ![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

[![Typing SVG](https://readme-typing-svg.herokuapp.com?color=%2336BCF7&lines=Timofey+Python+developer)](https://git.io/typing-svg) 
## ОПИСАНИЕ ПРОЕКТА 

# Foodgram — онлайн-сервис для обмена кулинарными рецептами и нахождения новых кулинарных идей.

# https://foodgramshop.ddns.net/

Технологии:
- Python 3.9
- Django 3.2.3
- Node.js 13.12.0
- React 17.0.1
- PostgreSQL 13
- Gunicorn 21.2.0
- Nginx
- Docker

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
