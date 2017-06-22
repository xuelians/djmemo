#!/bin/sh
echo ">> Running manage.py makemigrations"
python3 manage.py makemigrations

echo ">> Running manage.py migrate"
python3 manage.py migrate

echo ">> Done"
