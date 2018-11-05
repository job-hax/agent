Install Postgres db:
```
brew install postgres
```
Init and start db server:
```
initdb /usr/local/var/postgres
pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start
```
Create db user and database with owner privileges
```
psql postgres -c 'CREATE USER errorcvuser WITH PASSWORD '123456';';
psql postgres -c 'CREATE DATABASE errorcvdb WITH OWNER errorcvuser;";'
```

- Go to the [Google Google Developers](https://console.developers.google.com/apis/library?project=_) Console and create a project.

- Create OAuth client ID for Web Application under Credentials menu.

- Enter the following URI's in Authorized redirect URIs
```
http://localhost:8000/auth/complete/google-oauth2/
http://127.0.0.1:8000/auth/complete/google-oauth2/
```

- Under the APIs and services tab, search for Google+ API and Gmail API and enable them.

!!!Add your SOCIAL_AUTH_GOOGLE_OAUTH2_KEY and SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET in settings.py!!!
```
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY =''  #Paste CLient Key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '' #Paste Secret Key
```
Install requirements:
```
pip3 install -r requirements.txt
```

Optional - Create superuser for admin panel
```
python3 manage.py createsuperuser
```

Migrate changes:
```
python3 manage.py makemigrations accounts
python3 manage.py makemigrations
python3 manage.py migrate
```

Run Django server:
```
python3 manage.py runserver
```
Fetching emails running on background tasks. Each time your run the server execute following to make it run as well.
```
python3 manage.py process_tasks
```
