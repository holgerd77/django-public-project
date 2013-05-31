#!/bin/bash
SERVER_URL='127.0.0.1:8075'
echo "Example server url:  $SERVER_URL/"
echo "Admin url: $SERVER_URL/admin/"
python manage.py runserver --pythonpath=.. $SERVER_URL
