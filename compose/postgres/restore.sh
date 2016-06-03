#!/bin/bash

# stop on errors
set -e

# we might run into trouble when using the default `postgres` user, e.g. when dropping the postgres
# database in restore.sh. Check that something else is used here
if [ "$POSTGRES_USER" == "postgres" ]
then
    echo "restoring as the postgres user is not supported, make sure to set the POSTGRES_USER environment variable"
    exit 1
fi

# export the postgres password so that subsequent commands don't ask for it
export PGPASSWORD=$POSTGRES_PASSWORD

# check that we have an argument for a filename candidate
if [[ $# -eq 0 ]] ; then
    echo 'usage:'
    echo '    docker-compose run postgres restore <backup-file>'
    echo ''
    echo 'to get a list of available backups, run:'
    echo '    docker-compose run postgres list-backups'
    exit 1
fi

# set the backupfile variable
BACKUPFILE=/backups/$1

# check that the file exists
if ! [ -f $BACKUPFILE ]; then
    echo "backup file not found"
    echo 'to get a list of available backups, run:'
    echo '    docker-compose run postgres list-backups'
    exit 1
fi

echo "beginning restore from $1"
echo "-------------------------"

# delete the db
# deleting the db can fail. Spit out a comment if this happens but continue since the db
# is created in the next step
: ${POSTGRES_DB:=$POSTGRES_USER}
echo "deleting old database $POSTGRES_DB"
if dropdb -h postgres -U $POSTGRES_USER $POSTGRES_DB
then echo "deleted $POSTGRES_DB database"
else echo "database $POSTGRES_DB does not exist, continue"
fi

# create a new database
echo "creating new database $POSTGRES_DB"
createdb -h postgres -U $POSTGRES_USER $POSTGRES_DB -O $POSTGRES_USER

# restore the database
echo "restoring database $POSTGRES_DB"
psql -h postgres -U $POSTGRES_USER -d $POSTGRES_DB < $BACKUPFILE
