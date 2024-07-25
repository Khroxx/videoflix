# LINUX
#!/bin/bash

# Wechseln in das Projekt
# cd /videoflix/

# create virtual environment
python3 -m venv env

# activate virtual environment
source env/bin/activate

# install requirements
pip install -r requirements.txt

# make migrations
python manage.py makemigrations

# migrate
python manage.py migrate

# create docs
cd docs/
make html

echo "Installation compelete. Starting Server now"

# start server
python manage.py runserver

