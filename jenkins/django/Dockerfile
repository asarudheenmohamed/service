FROM selenium/standalone-chrome:3.1.0

USER root
# Base packages
RUN apt-get update \
    && apt-get -y install python python-pip libmysqlclient-dev

ADD entrypoint.sh /root/
