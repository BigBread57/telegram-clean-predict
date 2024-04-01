#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn server.wsgi:application --bind 0.0.0.0:8000 --daemon
python manage.py runbot

exec "$@"