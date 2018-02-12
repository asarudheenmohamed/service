#!/usr/bin/env bash
pip install -r /services/requirements.txt;

rm -f /var/log/django/all_done;
# create log dirs
mkdir -p /var/log/django/ && touch /var/log/django/tendercuts.log;
mkdir -p /var/log/django/driver/;
mkdir -p /var/log/django/inventory/;

# flag to indicate that we are all set up.
touch /var/log/django/all_done

