#! /usr/bin/env bash

kill $(pgrep python)
python manage.py runserver



