# Boon: Web Image Manager API

## Introduction

Boon API is part of the sample code for [Fontoberta's](http://www.fontoberta.com) software development services. It is an image management API to be consumed by client applications via image URLs. It was written using Django (version 2) and Django Rest Framework. 

Complete deployment is available via script using Docker in the [Fontoberta Demo](https://github.com/fontoberta/fontoberta-demo) repository.

## Dependencies

Boon API requires a MySQL server instance running on port 3306. A "boon" database must be created in order to migrate and load initial data.
If you are using the Docker deployment, a MySQL container will be deployed (boon-db) automatically and mapped to the application container.


## Docker Installation

To install the application and database (mysql) in docker containers, execute the script located in the root directory of the project as follows:

`$ source docker-deploy.sh`

This will enable the django app and the database in two different docker containers. The ports available for both apps are default (boon in port 8000, and mysql using port 3306), so make sure your system is not using them to avoid collisions. 

Initial data needed for the Fontoberta Public Website project is included.

## Local Installation

An instance of mysql is required, using the default 3306 port.
Fill out the needed information in file env.sh (on the project's root directory). Add the file content to your environment by executing the following:

`$ source env.sh`

Create the database according to the information provided in env.sh.

Add the project's requirements using a virtualenv, executing the following:

`$ virtualenv env`

`$ source env/bin/activate`

`(env)$ pip install -r requirements.pip`

Run migrations on the database by executing the following:

`(env)$ ./manage.py migrate`

To add initial data needed for project Fontoberta Public Website, execute the following:

`(env) cp -R fixtures/images/fontoberta  media/`
`(env)  cp -R fixtures/images/photography  media/`

`(env)$ ./manage.py loaddata fixtures/fixture.json`

Collect static files executing the following:

`(env)$ ./manage.py collectstatic`

Execute the app as follows:

`(env)$ ./manage.py runserver`

The application will be available on your localhost in port 8000.

## Tests

In order to execute unit tests available for the app, execute the following:

`(env)$ coverage --source='.' manage.py test`

`(env)$ coverage report -m`

# Usage

Boon is an image management app, that groups images into projects and sections, allowing them to be served by the web server on a given URL. Images can be set up as fixed URLs or iterated through code on the client. 

The URL for an image has the following format:

`http://<host>/groups/<group>/projects/<project>/sections/<section>/images/<image>/`

In order to make these URLs readable, slugs are used instead of Ids, with the exception of groups, that use the name field (these groups are Django's standard user groups, and will be explained in further detail in the next section).

#### Users and Groups

`http://<host>/groups/`

To provide team management functionality, we use Django's standard Group class. Every user must belong to at least one group, with the exception of super users, who don't need any groups since they are not meant to add or modify data.

The Admin site `http://<host>/admin/` is only available to super users, and is meant to manage groups and users, as well as Oauth2 applications and tokens.  No other objects from the application is available, since they are meant to be managed using the Django Rest Framework html client, or other clients via API.

In the initial data, two users are provided, with the following credentials:

`username: admin, password: administrator, superuser=True`

`username: webmaster, password: fontobertawebmaster, group=fontoberta`

`username: photographer, password: fontobertaphotographer, group=photograpy`

#### Projects

`http://<host>/groups/<group>/projects/`

Each user group can have several projects. In the example data, one project: Fontoberta public website (slug=website). 

#### Sections

`http://<host>/groups/<group>/projects/<project>/sections/`

Sections are parts of a project, meant for better organization. In the example data, we have sections for Menu (slug=menu), Home (slug=home), About Us (slug=about), and Tools (slug=tools).

#### Image Content

`http://<host>/groups/<group>/projects/<project>/sections/<section>/images`

Image content can be uploaded with the DRF client. URLs are returned by the API, which can be manually inserted by clients, or iterated by client code. 