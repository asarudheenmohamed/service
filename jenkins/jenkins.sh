#!/usr/bin/env bash

# start the environment
cd $WORKSPACE/jenkins && /usr/local/bin/docker-compose down;
cd $WORKSPACE/jenkins && /usr/local/bin/docker-compose up -d;

echo "Installing packages";
/usr/bin/docker exec -t -u root $(/usr/bin/docker ps -aqf "name=django") \
    sh -c "sh /root/entrypoint.sh"


# DB NEEDS TO BE SET UP run replace commands.
# CLEAN UP CACHE in php.

echo "Starting celery in django container";
/usr/bin/docker exec -t -u root $(/usr/bin/docker ps -aqf "name=django") \
    sh -c "cd /services/tendercuts/ && celery -A config worker --loglevel=info --beat &"

echo "Env is up and running, doing all dj migrations";
/usr/bin/docker exec -t -u root $(/usr/bin/docker ps -aqf "name=django") \
    sh -c "python services/tendercuts/manage.py migrate"

echo "Starting tests";
# Log into odoo container and start the tests
/usr/bin/docker exec -t -u root $(/usr/bin/docker ps -aqf "name=django") \
    sh -c "cd /services/tendercuts && py.test -vvv . --junitxml=/jenkins/jenkins.xml"