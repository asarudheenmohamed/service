FROM php:5.6.28-apache
# Base packages
RUN apt-get update \
    && apt-get -y install zsh \
         vim \
         git \
         php5-mysql \
         php5-gd \
         libmcrypt-dev \
    && docker-php-ext-install pdo_mysql mcrypt bcmath

RUN apt-get -y install zip unzip

RUN docker-php-ext-configure opcache --enable-opcache \
    && docker-php-ext-install opcache

ADD start_apache.sh /root/

ENTRYPOINT  sh /root/start_apache.sh \
    && /usr/bin/tail -f /dev/null