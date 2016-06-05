# Development and Deployment of Trinket via Docker

Trinket requires multiple processes to be configured and running during
development. One option is to setup these processes on each development
machine. The other option is to use Docker containers for the dependant
services needed.

Docker files have been setup in the project and can be used to buid a
working development environment for Trinket. The following instructions
borrow heavily from
[Cookiecutter Django setup](https://realpython.com/blog/python/development-and-deployment-of-cookiecutter-django-via-docker/).

The details for Trinket are a little different however. Lets get started
with Trinket!

## Local Setup

Start by cloning the trinket repository into a working directory:

    git clone git@github.com:DistrictDataLabs/trinket.git
    
Copy the sample.env file over to a development version

    cp sample.env .env.dev
    
Edit this file to adjust the values of key parameters. The defaults are
intended to work for a development setup, not counting the S3 parameters.

## Docker Setup

Start by downloading and installing the latest version of
[Docker Toolbox](https://www.docker.com/products/docker-toolbox) for
your operating system. At the time of this writing there are native
Docker installations for Mac and Windows in
[closed Beta](https://beta.docker.com/). The Beta has come a long way,
and it would be worth requesting access to this as I anticipate it will
be released soon.

### Docker Machine

When using the non-beta version, you will need to create a virtual
machine to work on. If you are using the Beta version, the following
instructions will not apply.

These instructions are adapted from the
[Docker Machine](https://realpython.com/blog/python/development-and-deployment-of-cookiecutter-django-via-docker/)
section of the Cookiecutter Django docker docs.

Create a new Docker host on your development workstation

    $docker-machine create -d virtualbox trinket
    eval "$(docker-machine env trinket)"

Note that the name _trinket_ will name your virtual machine. This
assumes you would have a unique virtual machine for trinket. It is also
possible to re-use an existing virtualmachine, such as the _**default**_
machine created when you setup Docker.

The second **eval** command places some environment variables into
your current shell terminal. These variables **associate** the current
shell with that virtualmachine. This is the only association, but once
you perform that eval, any commands in that shell will target the
associated VM. So, docker ps will list processes on that VM.

To view all of the machines you have installed:

    $ docker-machine ls

#### Docker Machine Address

The virtualbox machines will have their own unique IP address. The Beta
version of docker for mac or Docker for windows will not, and the IP
will be the same as your local machine. For the virtualbox version, you
will need to get the IP of the virtualbox machine:

    $ docker-machine ip trinket

Keep this IP address in mind, as you will use it later. Once you have
Trinket running you will access it at:

	http://<IP>:8001

If you are using the Beta version of Docker, the IP will just be
localhost.

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

If you setup the COMPOSE_FILE, you can leave out the -f dev.yml in
the commmand.

    docker-compose -f dev.yml build

Once all of the containers are up, you can start them all using:

    docker-compose -f dev.yml up -d

This will launch all of the containers in the background. (-d).

The postgres container will have created a database already, but we need
to migrate the Django project to this database. The general way to run
the manage.py command in docker is like this:

    docker-compose -f dev.yml django python manage.py <manage command and options>
    
For example:

	docker-compose -f dev.yml django python manage.py migrate --list
	


#### First Instance considerations

The first time that the containers are started, postgres will create the
database, but the database won't be initialized. Django will try to
start, but error out. So, we need to perform migrations, create a
superuser, and then restart the django container.

Perform the following steps:

    docker-compose -f dev.yml django python manage.py migrate
    docker-compose -f dev.yml django python manage.py createsuperuser
    docker-compose -f dev.yml restart django

You should see all of the migrations complete after the first command.

For the 2nd command, answer the question to create a new superuser.

Finally, the restart will cause the container to start again, and the runserver
command is the default command upon startup.

At this point, it is helpful to take a look at the stdout from the
django container:

    docker-compose -f dev.yml logs django

If everything worked, you should see the standard Django runserver
output, and a development server will be running at
[http://0.0.0.0:8001](http://0.0.0.0:8001).

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
	
The data volumes will be on *trinket_postgres_data_dev*. If you want to remove this,
then stop the postgres container, remove the volume ,and then start the postgres
container again.

	docker-compose stop postgres
	docker-compose rm postgres
	docker volume rm trinket_postgres_data_dev
	docker-compose up -d postgres
	
At this point, you should have a new DB, but none of the data is setup.

	docker-compose -f dev.yml python manage.py migrate
	docker-compose -f dev.yml python manage.py createsuperuser
	

    
