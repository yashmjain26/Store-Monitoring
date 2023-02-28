#!/bin/bash
echo "----- Entrypoint Commands Execution Started ------"

if [ "$DATABASE" = "postgres" ];then
    echo "Waiting for PostgreSQL"

    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
    done

    echo "PostgreSQL Started"
fi

python manage.py db upgrade
python manage.py run -h 0.0.0.0

echo "----- Entrypoint Commands Execution Finished -----"