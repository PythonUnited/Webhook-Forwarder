# pull official base image
FROM python:3.11.7-bullseye

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_DEFAULT_TIMEOUT 60

# install pip dependencies
RUN pip install --upgrade pip

# copy project
COPY . .

RUN pip install -r requirements/dev.txt

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
