# LINUX and MAC
#!/bin/bash

# Wechseln in das Projekt
# cd /videoflix/

# create virtual environment
python3 -m venv env

# activate virtual environment
source env/bin/activate

# install requirements
pip install -r requirements.txt

# database migrations
python manage.py makemigrations
python manage.py migrate

# create docs
# cd docs/
# make html

echo "Installation complete. Starting Server now"

# start server
python manage.py runserver

