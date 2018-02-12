#!/usr/bin/env bash

echo "Setting env for magento";
cp /root/local.xml /var/www/html/app/etc/;
cp /root/constants.php /var/www/html/lib/TenderCutsMessaging/;
mkdir /var/www/html/var/ && chmod 777 /var/www/html/var/;

service apache2 start;
