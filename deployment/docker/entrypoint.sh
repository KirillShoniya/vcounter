#!/bin/sh
# define configurations
cp /code/conf/.env.docker /code/.env
cp /code/conf/config.docker.yaml /code/conf/config.local.yaml

gunicorn run_server:app -b 0.0.0.0:80 --reload --workers 4 --timeout 300
