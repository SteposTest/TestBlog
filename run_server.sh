#!/usr/bin/env bash

. set_envs.sh

python manage.py migrate
python manage.py runserver