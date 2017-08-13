## Instructions:
+ must run server from backend/server, run 'python manage.py runserver localhost:3333'

## Local DB Setup:
+ Install PostgreSQL 
+ Create user named admin, 'CREATE USER admin;'
+ Create database named "baeML_db" 'CREATE DATABASE baeML_db;'

## Creating the Default Skipgram Model
If running for the first time, need to run 'python skip_pickler.py' from backend/server

<del>## Required pip packages for DB:
+ psycopg2

## Required pip packages:
+ Django
+ Djangorestfrsamework
+ Django_facebook
+ django-cors-headers </del>

All packages needed are now in dependencies.sh. Run server.sh to autoinstall all the packages and start the server.
