#!/usr/bin/env bash

echo "Setting env for magento";
cp /root/apache2.conf /etc/apache2/apache2.conf

echo "Setting env for magento";
cp /root/local.xml /var/www/html/app/etc/;
cp /root/constants.php /var/www/html/lib/TenderCutsMessaging/;
mkdir -p /var/www/html/var/ && chmod 777 /var/www/html/var/;

a2enmod rewrite;
service apache2 start;
