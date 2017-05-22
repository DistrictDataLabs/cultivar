# Add keys for postgis to install
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt trusty-pgdg main" >> /etc/apt/sources.list'
wget --quiet -O - http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | sudo apt-key add -

sudo apt-get update -y
sudo apt-get upgrade -y

sudo apt-get install -y postgresql-9.5-postgis-2.2 pgadmin3 postgresql-contrib-9.5 postgresql-server-dev-9.5
sudo apt-get install -y python3-dev git python-pip make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev python-virtualenv libsqlite3-dev zip

cd project/

# setup db and allow django to access it
sudo su
sudo -u postgres createdb cultivar
sudo -u postgres psql cultivar -a -f scripts/db_setup.sql
sudo cp scripts/pg_hba.conf /etc/postgresql/9.5/main/pg_hba.conf
service postgresql restart

#set up virtualenv with python3
virtualenv --python=python3 venv
source venv/bin/activate
pip install -r requirements/local.txt

python manage.py migrate

exit
