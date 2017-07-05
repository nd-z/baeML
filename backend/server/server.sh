#!/usr/bin/env bash
if [[ "$1" == "--install" ]]; then
  bash ./dependencies.sh
fi

#Start Postgres, for MacOS:
#brew services start postgresql
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
