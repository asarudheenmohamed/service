#!/usr/bin/env bash

# start the environment
cd $WORKSPACE/jenkins && /usr/local/bin/docker-compose -f docker-compose-jenkins.yml down;
cd $WORKSPACE/jenkins && /usr/local/bin/docker-compose -f docker-compose-jenkins.yml build && /usr/local/bin/docker-compose -f docker-compose-jenkins.yml up -d --force-recreate;

echo "Installing packages";
/usr/bin/docker exec -t -u root $(/usr/bin/docker ps -aqf "name=django") \
    sh -c "sh /root/entrypoint.sh"

echo "Installing php package";
/usr/bin/docker exec -t -u root $(/usr/bin/docker ps -aqf "name=magento") \
    sh -c "cd /var/www/html && php composer.phar install"

echo "Env is up and running, doing all dj migrations";
/usr/bin/docker exec -t -u root $(/usr/bin/docker ps -aqf "name=django") \
    sh -c "pip install -r /root/requirements.txt && python services/tendercuts/manage.py migrate"

echo "Starting tests";
# Log into odoo container and start the tests
/usr/bin/docker exec -t -u root $(/usr/bin/docker ps -aqf "name=django") \
    sh -c "cd /services/tendercuts && (celery -A config worker --loglevel=info --beat &) && py.test -vvv . --cache-clear --junitxml=/jenkins/jenkins.xml --cov=app --cov-report xml:/jenkins/coverage.xml"