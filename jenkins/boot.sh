#!/usr/bin/env bash

echo "Installing packages";
docker exec -t -u root $(docker ps -aqf "name=django") \
    sh -c "sh /root/entrypoint.sh"

echo "Installing php package";
docker exec -t -u root $(docker ps -aqf "name=php") \
    sh -c "cd /var/www/html && php composer.phar install"

echo "Env is up and running, doing all dj migrations";
docker exec -t -u root $(docker ps -aqf "name=django") \
    sh -c "python services/tendercuts/manage.py migrate"

