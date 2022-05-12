FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update && \
  apt-get install -y \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev \
  autoconf \
  libtool \
  python3.8 \
  python3-pip

RUN apt-get install -y build-essential libssl-dev libffi-dev \
  python3-dev cargo

COPY requirements.txt ./
RUN pip3 install --upgrade pip
RUN pip3 install cryptography --no-binary cryptography
RUN pip3 install --no-cache-dir -r requirements.txt

COPY codes /codes

WORKDIR /codes

ENTRYPOINT [ "/usr/bin/python3.6", "-m", "awslambdaric" ]
CMD [ "main.handler" ]