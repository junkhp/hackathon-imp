#!/bin/bash

cd /workspace/hackathon-imp

# get latest version
git checkout master
git pull origin master

# run server
python3 -B manage.py migrate
python3 -B manage.py runserver 0:8099
