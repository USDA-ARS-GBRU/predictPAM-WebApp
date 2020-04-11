#!/bin/bash
source activate predictenv
ls
pwd
cd app
ls
exec gunicorn -c gunicorn_config.py wsgi:application 