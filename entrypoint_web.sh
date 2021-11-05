#!/bin/sh

while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.1
done

python3 manage.py migrate
python3 manage.py init_superuser
python3 manage.py collectstatic --no-input

exec "$@"