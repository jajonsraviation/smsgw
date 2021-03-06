FROM python:2.7-onbuild
MAINTAINER Vojta Bartos <hi@vojtech.me>

ENV DEBIAN_FRONTEND noninteractive
ENV SHELL /bin/bash
ENV TERM xterm

# default necessary packages
RUN \
  apt-get update && \
  apt-get install -y curl && \
  apt-get install -y python && \
  apt-get install -y git-core && \
  apt-get install -y libmysqlclient-dev && \
  apt-get install -y cmake

# installing gammu
RUN \
  mkdir -p /usr/src/gammu && \
  mkdir -p /var/log/gammu && \
  git clone https://github.com/gammu/gammu.git /usr/src/gammu && \
  (cd /usr/src/gammu; git checkout tags/1.34.0 -b 1.34.0) && \
  (cd /usr/src/gammu; ./configure) && \
  (cd /usr/src/gammu; make) && \
  (cd /usr/src/gammu; make install)
# fixing error gammu-smsd: error while loading shared libraries: libGammu.so.7:
# cannot open shared object file: No such file or directory
# http://comments.gmane.org/gmane.linux.drivers.gammu/10260
RUN ldconfig

# python app port
EXPOSE 5000

# running python app
CMD ["bin/run"]
