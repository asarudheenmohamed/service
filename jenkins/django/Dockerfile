FROM selenium/standalone-chrome:3.1.0

USER root
# Base packages
RUN apt-get update \
    && apt-get -y install python python-pip libmysqlclient-dev

ADD entrypoint.sh /root/

ADD requirements.txt /root/
RUN pip install -r /root/requirements.txt;

USER root
RUN apt-get update && apt-get install -y zsh git
RUN /usr/bin/zsh && git clone --recursive https://github.com/varunxyz/prezto.git "${ZDOTDIR:-$HOME}/.zprezto" \
  && ln -s ~/.zprezto/runcoms/zlogin ~/.zlogin \
  && ln -s ~/.zprezto/runcoms/zlogout ~/.zlogout \
  && ln -s ~/.zprezto/runcoms/zprofile ~/.zprofile \
  && ln -s ~/.zprezto/runcoms/zshenv ~/.zshenv \
  && ln -s ~/.zprezto/runcoms/zshrc ~/.zshrc \
  && ln -s ~/.zprezto/runcoms/zpreztorc ~/.zpreztorc
