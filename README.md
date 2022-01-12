[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)

## Проект

Учебный проект YaMDb. Cобирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий может быть расширен администратором. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/A-A-Tyurin/yamdb_final
```

Создать файл .env по шаблону .env.template

Запустить Docker:

```
sudo docker-compose up
```

Выполнить миграции, создать суперпользователя, собрать статику:
```
sudo docker-compose exec web python3 manage.py migrate
sudo docker-compose exec web python3 manage.py init_superuser
sudo docker-compose exec web python3 manage.py collectstatic --no-input
```
или раскомментировать строки в Dockerfile:
```
# RUN chmod 755 entrypoint_web.sh
# ENTRYPOINT ["/yamdb/entrypoint_web.sh"]
```

Загрузить тестовые данные:

```
sudo docker-compose exec web python3 manage.py loaddata fixtures.json
```
