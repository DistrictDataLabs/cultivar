# Development Documentation

Welcome to the development documentation for Cultivar. For more on contributing to Cultivar, please see [About Cultivar](about.md), which discusses how to contribute, the development board for issues, the way that the project is set up, and includes a list of contributors and the changelog. This documentation is intended to provide guidelines to getting started with and setting up Cultivar, as well as provide notes for how to add features to Cultivar.

## Development of Cultivar using Docker

While developing Cultivar it is possible to setup all dependencies on the local machine. This does take some effort and requires that the local
machine support PostSQL, RabbitMQ, and that you setup two processes, one for Django and one for Celery.

For those that prefer using Docker, the project has been setup to include the necessary Dockerfile's, and compose yml files you will need. 

Detailed instructions can be found in [Developing with Docker](docker.md).

## Database Schema

The proposed Cultivar database schema is as follows:

![Cultivar Database Schema](images/Cultivar_schema.png)

The database is described by Django models and is managed and updated through the use of Django migrations. For more details, and a complete look at the database, please review the code for those models. To get a current snapshot of the structure of the database, I recommend using [ERAlchemy](https://github.com/Alexis-benoist/eralchemy), which will generate a diagram or markdown file describing the schema. 
