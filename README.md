### Quickstart

1. Install Postgres database depending on your [OS](https://www.postgresql.org/download/):
```
brew install postgres
```

2. Initialize and start Postgres server in localhost:
```
initdb /usr/local/var/postgres
pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start
```

3. Create db user and database with owner privileges:
```
psql postgres -c "CREATE USER errorcvuser WITH PASSWORD '123456';"
psql postgres -c "CREATE DATABASE errorcvdb WITH OWNER 'errorcvuser';"
```

4. In [Google Google Developers](https://console.developers.google.com/apis/library?project=_) Console  create a project:

a) Create OAuth client ID for Web Application under Credentials menu.

b) Enter the following URI's in Authorized redirect URIs list: 
```
http://localhost:8000/auth/complete/google-oauth2/
http://127.0.0.1:8000/auth/complete/google-oauth2/
```
c) Under the APIs and services tab, search for Google+ API and Gmail API and enable them.

5. Set SOCIAL_AUTH_GOOGLE_OAUTH2_KEY and SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET environment variables:
```
export SOCIAL_AUTH_GOOGLE_OAUTH2_KEY =''  #Paste CLient Key
export SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '' #Paste Secret Key
```
6. Install python dependencies for application:
```
pip3 install -r requirements.txt
```

7. Create superuser for admin panel:
```
python3 manage.py createsuperuser
```

8. Migrate application data changes to postgres:
```
python3 manage.py makemigrations accounts
python3 manage.py makemigrations
python3 manage.py migrate
```

9. Start Django server:
```
python3 manage.py runserver
```
10. In another terminal run:
```
python3 manage.py process_tasks
```
