#!/usr/bin/env bash

port=8000

if [ -n "$1" ]; then
  port="$1"
fi

python3 ./manage.py runserver $port
