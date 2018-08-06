#!/usr/bin/env bash

# start the environment
cd $HOME/services/jenkins && /usr/local/bin/docker-compose down;
cd $HOME/services/jenkins && /usr/local/bin/docker-compose build && /usr/local/bin/docker-compose up -d --force-recreate;

echo "Installing packages";
/usr/bin/docker exec -t -u root $(/usr/bin/docker ps -aqf "name=django") \
    sh -c "sh /root/entrypoint.sh"

echo "Installing php package";
/usr/bin/docker exec -t -u root $(/usr/bin/docker ps -aqf "name=php") \
    sh -c "cd /var/www/html && php composer.phar install"

echo "Env is up and running, doing all dj migrations";
/usr/bin/docker exec -t -u root $(/usr/bin/docker ps -aqf "name=django") \
    sh -c "python services/tendercuts/manage.py migrate"
