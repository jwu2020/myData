#!/bin/bash

echo 'Making migrations...'
python3 manage.py makemigrations
python3 manage.py migrate
