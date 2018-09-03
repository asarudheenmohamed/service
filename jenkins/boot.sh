#!/usr/bin/env bash
# This file installs the related packages for php and does the migrations for
# django.


# For django we do the package installation directly in the django's Dockerfile.
echo "Installing php package";
docker exec -t -u root $(docker ps -aqf "name=magento") \
    sh -c "cd /var/www/html && php composer.phar install"

echo "Env is up and running, doing all dj migrations";
docker exec -t -u root $(docker ps -aqf "name=django") \
    sh -c "python services/tendercuts/manage.py migrate"

