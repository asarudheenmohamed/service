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

USER root
RUN apt-get update && apt-get install -y zsh git
RUN /usr/bin/zsh && git clone --recursive https://github.com/varunxyz/prezto.git "${ZDOTDIR:-$HOME}/.zprezto" \
  && ln -s ~/.zprezto/runcoms/zlogin ~/.zlogin \
  && ln -s ~/.zprezto/runcoms/zlogout ~/.zlogout \
  && ln -s ~/.zprezto/runcoms/zprofile ~/.zprofile \
  && ln -s ~/.zprezto/runcoms/zshenv ~/.zshenv \
  && ln -s ~/.zprezto/runcoms/zshrc ~/.zshrc \
  && ln -s ~/.zprezto/runcoms/zpreztorc ~/.zpreztorc

ADD env /root/
ADD start_apache.sh /root/

ENTRYPOINT  sh /root/start_apache.sh \
    && /usr/bin/tail -f /dev/null
