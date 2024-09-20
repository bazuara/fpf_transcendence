#!/bin/bash
python3 manage.py collectstatic --noinput
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py reset_user_sockets_and_clear_rooms

if [ -n "$DJANGO_ROOT_PASSWORD" ] && [ -n "$DJANGO_ROOT_USER" ]; then
    python3 manage.py createsuperuser_from_env --username "$DJANGO_ROOT_USER" --password "$DJANGO_ROOT_PASSWORD" --noinput --email root@here.com
fi

while [ ! -f /blockchain/build/contract_address.txt ]; do
    echo "Waiting for smart contract deployment..."
    sleep 1
done

daphne -e ssl:443:privateKey=/key.pem:certKey=/cert.pem transcendence.asgi:application
