#!/bin/bash
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py reset_user_sockets_and_clear_rooms
if [ -n "$DJANGO_ROOT_PASSWORD" ] && [ -n "$DJANGO_ROOT_USER" ]; then
    python3 manage.py createsuperuser_from_env --username "$DJANGO_ROOT_USER" --noinput --email root@here.com
fi
python3 manage.py runserver 0:443
