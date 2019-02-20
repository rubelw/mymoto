FROM localstack/java-maven-node-python

MAINTAINER Waldemar Hummer (waldemar.hummer@gmail.com)
LABEL authors="Waldemar Hummer (waldemar.hummer@gmail.com), Gianluca Bortoli (giallogiallo93@gmail.com)"

RUN apk update && apk upgrade

RUN apk add --no-cache python3 python3-dev && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools

RUN if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip; else rm /usr/bin/pip && ln -s /usr/bin/pip3 /usr/bin/pip; fi
RUN if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; else rm /usr/bin/python && ln -sf /usr/bin/python3 /usr/bin/python; fi
RUN rm -r /root/.cache

# Install ruby
RUN apk add autoconf bison bzip2
RUN apk add bzip2-dev ca-certificates coreutils
RUN apk add dpkg-dev dpkg gcc gdbm-dev glib-dev libc-dev
RUN apk add libffi libffi-dev libxml2 libxml2-dev libxslt
RUN apk add libxslt-dev linux-headers make ncurses-dev openssl
RUN apk add openssl-dev procps readline-dev
RUN apk add ruby=2.4.5-r0
RUN apk add ruby-dev=2.4.5-r0
RUN apk add ruby-irb=2.4.5-r0
RUN apk add ruby-rdoc=2.4.5-r0
#RUN apk add ruby-ri
RUN apk add ruby-bundler
RUN apk add ruby-rdoc wget
RUN apk add binutils cmake make libgcc musl-dev gcc g++
RUN apk add musl libstdc++
RUN apk add tar xz yaml-dev zlib-dev
RUN apk add gnupg

# fix some permissions and create local user
RUN mkdir -p /.npm && \
    chmod 777 . && \
    chmod 755 /root && \
    chmod -R 777 /.npm && \
    chown -R `id -un`:`id -gn` .


RUN cd /opt && wget https://releases.hashicorp.com/terraform/0.11.11/terraform_0.11.11_linux_amd64.zip && unzip *.zip && mv terraform /usr/local/bin/

ADD Gemfile /tmp/Gemfile
RUN gem install bundler && bundle config --global silence_root_warning 1 && cd /tmp && bundle install


# logs folder
RUN mkdir -p /var/log/supervisord/ \
  && mkdir -p /var/log/moto/

# install moto_server
ADD /. /moto/
WORKDIR /moto/
RUN pip install ".[server]"

ENTRYPOINT ["supervisord", "--nodaemon", "--configuration", "/moto/docker/supervisord.conf"]



