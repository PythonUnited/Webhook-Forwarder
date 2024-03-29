# Deployment on test or production environments

## Development in docker container

Copy env templates:

- Copy `.env-template` to `.env`
- Copy `.env.django-template` to `.env.django`
- Copy `.env.django.db-template` to `.env.django.db`

Adjust settings in env files as needed.

Run the docker development container:

    docker-compose up -d

(You can use `--build` to force rebuilding the docker container)

There are two ways to debug django inside the container.

1: Debug using by connecting to the remote docker and just debug a django project as usual.
E.g. in Visual Studio Code: install extension: Visual Studio Code Remote - Containers
Then connect to the remote md-api-dvl_django_1 container.
You can now start a debugging session as usual

Note that you can add the /srv/project_root folder as workspace folder so you can use
the git functionality in the IDE as well

2: The one that isn't all that great uses debugpy. You can read more about it here:
To debug a running container, see: [Debugging a Containerized Django App in VS Code](https://testdriven.io/blog/django-debugging-vs-code/)

## Development in using local python

Set-up and enable [pyenv](https://github.com/pyenv/pyenv#getting-pyenv) and 
[pyenv-virtual-env](https://github.com/pyenv/pyenv-virtualenv#installation):

    pyenv install --list
    pyenv install 3.11.7
    pyenv virtualenv 3.11.7 webhook_forwarder
    pyenv local webhook_forwarder__3.11.7

Clone git repo. For any other env than development make sure ssh agent 
forwarding is enabled.
    
    git clone git@github.com:pu/webhook_forwarder.git
    cd webhook_forwarder/src
   
Create `.env` file based on `.env-sample`

## Seting up dev env

When django is used locally (not in a docker env) the `.env` file is used by Django.

Rename `.env-template` to `.env` and adjust settings as needed.

Install dependencies:

    pip install -r requirements/dev.txt

Run migrations to initialize the database:

    python manage.py migrate

Start development server:

    python manage.py runserver

### Dramatiq message queue / RabbitMQ

First start rabbitmq in a docker container:

    docker-compose up -d rabbitmq

Start the dramatiq worker:

    ./manage.py rundramatiq  --threads 2 --processes 1 --reload

Start the periodiq (cron replacement) scheduler:

    ./manage.py runperiodiq

Task queue progress is available in Django admin 
[http://localhost:8000/admin/django_dramatiq/task/](http://localhost:8000/admin/django_dramatiq/task/).


