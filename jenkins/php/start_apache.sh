#!/usr/bin/env bash

echo "Setting env for magento";
cp /root/env/local.xml /var/www/html/app/etc/;
cp /root/env/constants.php /var/www/html/lib/TenderCutsMessaging/;

service apache2 start;
