# Start Postgres
initdb /usr/local/var/postgres
pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start

# Create db user and database with owner privileges
psql postgres -c "CREATE USER errorcvuser WITH PASSWORD '123456';"
psql postgres -c "CREATE DATABASE errorcvdb WITH OWNER 'errorcvuser';"

# Install python dependencies for application:
pip3 install -r requirements.txt

# Migrate application data changes to postgres:
python3 manage.py makemigrations accounts
python3 manage.py makemigrations
python3 manage.py migrate

# Create superuser for admin panel:
python3 manage.py createsuperuser
