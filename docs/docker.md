# Development and Deployment of Trinket via Docker

Trinket requires multiple processes to be configured and running during
development. One option is to setup these processes on each development
machine. The other option is to use Docker containers for the dependant
services needed.

Docker files have been setup in the project and can be used to buid a
working development environment for Trinket.

## Local Setup

Start by cloning the trinket repository into a working directory:

    git clone git@github.com:DistrictDataLabs/trinket.git
    
Copy the `.env.docker.sample` file over to this target location:

    cp .env.docker.sample .env.docker
    
Later on, you can edit this file to adjust the values of key parameters. The defaults are intended to work out of the box for a basic development setup.

## Docker Setup

Start by downloading and installing [Docker CE from the Docker Store for your OS](https://www.docker.com/community-edition#/download)..

### Docker Compose Command

The docker-compose command uses a **compose file** with the
default name of docker-compose.yml. For development, we want to use
dev.yml instead.

#### Docker Compose File

If you define the environment variable COMPOSE_FILE, you can change the
default file to use:

    export COMPOSE_FILE=dev.yml

This makes it easier in development. Without the environment variable,
use the -f command for each docker-compose usage:

    docker-compose -f dev.yml <command> [options]

The commands below will not assume that the COMPOSE_FILE variable has
been setup, but in practice, this is highly recommended.

### Building with Docker

The compose file defines the containers and details needed to launch and
load the app. To start and run all of the containers, you must first
build them. By default, the _up_ command will build them if needed, but
it is also easy to explicitly build the containers before starting
them. 

Remember: if you setup your COMPOSE_FILE environment variable, you can leave out the -f dev.yml in
the commmand.

    docker-compose -f dev.yml build

Once all of the containers are up, you can start them all using:

    docker-compose -f dev.yml up -d

This will launch all of the containers in the background. (-d).

The postgres container will have created a database already, but we need
to migrate the Django project to this database. The general way to run
the manage.py command in docker is like this:

    docker-compose exec -f dev.yml django python manage.py <manage command and options>
    
For example:

	docker-compose exec -f dev.yml django python manage.py migrate --list


#### First Instance considerations

The first time that the containers are started, postgres will create the
database, but the database won't be migrated. So, we need to perform migrations and create a
superuser.

Perform the following steps:

    docker-compose exec -f dev.yml django python manage.py migrate
    docker-compose exec -f dev.yml django python manage.py createsuperuser

You should see all of the migrations complete after the first command.

For the 2nd command, answer the questions to create a new superuser.

At this point, it is helpful to take a look at the stdout from the
django container:

    docker-compose -f dev.yml logs django

If everything worked, you should see the standard Django runserver
output, and a development server will be reported running at
http://0.0.0.0:8001, which you can access at [http://localhost:8001](http://localhost:8001).

## Production Use

The current recommendation with Trinket is to run on heroku. The project
includes the required Procfile for this purpose.

It is possible to run the project using docker in production, and the
docker-compose.yml file is provided for this case, but that
configuration has not been tested, and is not currently supported.

## Making Docker a little Easier

Here are a few of my tips for making things easier using docker.

1. docker-compose is a long command. Create an alias:

    alias dc='docker-compose'

2. Running manage.py via docker-compose is a bit a bit long also. Create a local bash script to wrap the long command into a *short* command that works similarly:

    Create a bash script named 'manage'

        #!/bin/bash
        
        docker-compose -f dev.yml python manage.py "$@"
    
    Make the script executable:
    

		chmod a+x manage
		
	Now, you can do this:

        ./manage migrate --list
        
# PostgreSQL Data

The postgres container automatically creates the database when it is first started.
The user, db name and password are taken from the environment. If you later want to
change any of those, you will have to *remove* the docker volumes associated with 
the database completely. If  not removed, postgres will find them in the volumes on
the container server, and re-use them. You can list volumes with this command:

	docker volume ls
	
The data volumes will be on *cultivar_postgres_data_dev*. If you want to remove this,
then stop the postgres container, remove the volume, and then start the postgres
container again.

	docker-compose stop postgres
	docker-compose rm postgres
	docker volume rm cultivar_postgres_data_dev
	docker-compose up -d postgres
	
At this point, you should have a new DB, but none of the data is setup.

	docker-compose exec -f dev.yml python manage.py migrate
	docker-compose exec -f dev.yml python manage.py createsuperuser
	

    
