# videoflix

Emails sometimes take a few seconds 

# Prerequisites for devs

0. make sure you have installed the following on your computer:
pip, redis/redis-server, django-redis,postgresql, postgresql-contrib
(nano redis.conf on your computer and uncheck:
 #password = foobared 
)

1. create envirnment for credentials
```bash 
touch videoflix/.env
```

2. add details for email and postgresql in videoflix/videoflix/.env(nobody will ever see them)
```bash
MAIL = yourworkingemail@email.com
PASSWORD = passwordtoemail

DB_USER = username
DB_PASS = databaseuserpassword
```

3. create database
3.1 open terminal and enter postgres
```bash 
sudo su postgres
psql
```
3.2 copy and paste
```bash
CREATE DATABASE videoflix; 
CREATE USER username WITH PASSWORD 'databaseuserpassword';
ALTER ROLE username SET client_encoding TO 'utf8'; 
ALTER ROLE username SET default_transaction_isolation TO 'read committed';
ALTER ROLE username SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE videoflix TO bari;
\q
```
then hit Ctrl+D to exit

4.  


# INSTALLATION

1. Run the install script


# 