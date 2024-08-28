# Videoflix
## Description
This is a backend for my Videoflix (Netflix clone) frontend consisting of:<br>
User registration, activation, login, logout, password resetting. <br>
PostgreSQL is used for Database and RQWorker for background tasks.
After logging in you can watch any movie via VideoJS that has been uploaded and converted to HLS format <br>
Quick reminder: Emails sometimes take a few seconds 

## Documentation
https://bari-sopa.com/docs/backend/videoflix


## Prerequisites for devs

0. make sure you have installed the following on your computer:
pip, redis/redis-server, django-redis,postgresql, postgresql-contrib
(nano redis.conf on your computer and uncheck:
 #password = foobared 
)

1. clone repository
```bash
git clone https://github.com/Khroxx/videoflix.git
```

2. create environment for credentials
```bash 
touch .env
```

3. add variables for email and postgresql in /.env 
```bash
MAIL = yourworkingemail@outlook.com
PASSWORD = passwordtoemail

DB_USER = username
DB_PASS = userpassword

backend_address = your.back-address.com
domain_address = your-domain.com
```

4. create postgresql database
- open terminal and enter postgres
```bash 
sudo su postgres
psql
```
- copy then change username and password and paste
```bash
CREATE DATABASE videoflix; 
CREATE USER username WITH PASSWORD 'userpassword';
ALTER ROLE username SET client_encoding TO 'utf8'; 
ALTER ROLE username SET default_transaction_isolation TO 'read committed';
ALTER ROLE username SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE videoflix TO username;
GRANT ALL ON SCHEMA public TO username;
\q
```
then hit Ctrl+D to exit


## INSTALLATION

1. Run the install script depending on OS:
installOnBash.sh
installOnWindows.bat

- The install script will create the virtual environment, activate it, install all requirements, makes migrations and migrates them and then starts the local server

2. create admin
```bash
python manage.py createsuperuser
```


## TESTS

0. activate RQWorker before testing:
```bash
python manage.py rqworker default
```

1. run a summary of all tests using pytest:
```bash
pytest -s
```

2. For detailed coverage, use:
```bash
pytest --cov
```


## Quick Info
Started: 14.07.24 <br>
Finished: .08.24