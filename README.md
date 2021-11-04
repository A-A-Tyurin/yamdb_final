## Проект

Учебный проект YaMDb.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/A-A-Tyurin/infra_sp2
```

Создать файл .env по шаблону .env.template

Запустить Docker:

```
sudo docker-compose up
```

Загрузить тестовые данные:

```
sudo docker-compose exec web python3 manage.py loaddata fixtures.json
```

[![yamdb workflow](https://github.com/A-A-Tyurin/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/A-A-Tyurin/yamdb_final/actions/workflows/yamdb_workflow.yml)
