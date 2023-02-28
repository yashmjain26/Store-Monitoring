FROM python:3.10.5-bullseye

# working directory 
WORKDIR /usr/src/app

# environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# system dependencies 
RUN apt-get update && apt-get install -y netcat

# app dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY ./store_Monitoring/ /usr/src/app/
COPY ./migrations/ /usr/src/app/

COPY ./entrypoint.sh /entrypoint.sh

RUN ls

# entrypoint bash script
# ENTRYPOINT ["/entrypoint.sh"]