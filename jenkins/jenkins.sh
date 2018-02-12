#!/usr/bin/env bash

# start the environment
cd $WORKSPACE/jenkins && /usr/local/bin/docker-compose down;
cd $WORKSPACE/jenkins && /usr/local/bin/docker-compose up -d;

echo "Installing packages";
/usr/bin/docker exec -t -u postgres $(/usr/bin/docker ps -aqf "name=django") \
    sh -c "sh /root/entrypoint.sh"

echo "Waiting for env to come up";
for i in $(seq 1 $END); do
    result=$(docker exec -t -u root django bash -c "[[ -f '/var/log/django/all_done' ]] || echo 0")
    if [[ $result -ne 0 ]]; then
        # all done break out of loop
        break;
    fi
    echo $i;
done

# DB NEEDS TO BE SET UP run replace commands.
# CLEAN UP CACHE in php.
# START CELERY

echo "Env is up and running, doing all dj migrations";
/usr/bin/docker exec -t -u postgres $(/usr/bin/docker ps -aqf "name=django") \
    sh -c "python services/tendercuts/manage.py migrate"

echo "Starting tests";
# Log into odoo container and start the tests
/usr/bin/docker exec -t -u root $(/usr/bin/docker ps -aqf "name=django") \
    sh -c "py.test -vvv . --junitxml=/jenkins/jenkins.xml"