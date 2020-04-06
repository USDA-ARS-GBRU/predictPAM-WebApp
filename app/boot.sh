#!/bin/bash
source activate predictenv
ls
pwd
cd app
ls
exec gunicorn -b 0.0.0.0:8000 --timeout 180 wsgi:application 