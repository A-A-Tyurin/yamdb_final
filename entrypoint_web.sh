#!/bin/sh

while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.1
done

sudo python3 manage.py migrate
sudo python3 manage.py init_superuser
sudo python3 manage.py collectstatic --no-input

exec "$@"