Foodgram
Main Foodgram workflow

Foodgram — онлайн-сервис для обмена кулинарными рецептами и нахождения новых кулинарных идей.

Технологии
Python 3.9
Django 3.2.3
Node.js 13.12.0
React 17.0.1
PostgreSQL 13
Gunicorn 21.2.0
Nginx
Docker
Установка и запуск для удалённого сервера на Linux
Установка Docker на Linux
Cамый простой способ установить Docker на Linux — скачать и выполнить официальный скрипт. Для этого поочерёдно выполните в терминале следующие команды:

Скачайте и установите curl — консольную утилиту, которая умеет скачивать файлы по команде пользователя:
sudo apt update
sudo apt install curl
С помощью утилиты curl скачайте скрипт для установки докера с официального сайта:
curl -fSL https://get.docker.com -o get-docker.sh 
Запустите сохранённый скрипт с правами суперпользователя:
sudo sh ./get-docker.sh
Запуск проекта
Для запуска необходим установленный Docker

Создайте каталок для проекта и войдите в него:
mkdir foodgram
cd foodgram
Скачайте файл docker-compose.production.yml
curl -o docker-compose.production.yml https://raw.githubusercontent.com/Andron1215/kittygram_final/main/docker-compose.production.yml
Скачайте файл .env и отредактируйте его:
curl -o .env https://github.com/Andron1215/foodgram-project-react/main/.env.example
nano .env
Скачайте и запустите проект:
sudo docker compose -f docker-compose.production.yml pull
sudo docker compose -f docker-compose.production.yml down
sudo docker compose -f docker-compose.production.yml up -d
Сделайте миграцию для базы данных:
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
Соберите статику и копируйте в каталог со статикой:
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
sudo docker compose -f docker-compose.production.yml exec backend mkdir -p /static/static/
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/static/. /static/static/
Запуск проекта с файлов репозитория
Клонируйте репозиторий:
git clone https://github.com/Andron1215/foodgram-project-react.git
Запустите проект:
sudo docker compose -f docker-compose.yml down
sudo docker compose -f docker-compose.yml up -d
Сделайте миграцию для базы данных:
sudo docker compose -f docker-compose.yml exec backend python manage.py migrate
Соберите статику и копируйте в каталог со статикой:
sudo docker compose -f docker-compose.yml exec backend python manage.py collectstatic
sudo docker compose -f docker-compose.yml exec backend mkdir -p /static/static/
sudo docker compose -f docker-compose.yml exec backend cp -r /app/static/. /static/static/
Авторы
Backend: Богидаев Андрей
