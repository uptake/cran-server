FROM continuumio/miniconda3
MAINTAINER Troy de Freitas "troy.defreitas@uptake.com", Nick Paras "nick.paras@uptake.com"

RUN apt-get update -y && apt-get install -y python3-gunicorn

RUN mkdir -p "/opt/cran/uploads" && \
    mkdir -p "/opt/cran/src/contrib/" && \
    touch "/opt/cran/src/contrib/PACKAGES"

COPY . /opt/cran-server/

WORKDIR /opt/cran-server

RUN python setup.py install

ENV FLASK_APP /opt/cran-server/cranserver/server.py

EXPOSE 8000

CMD gunicorn -w 1 -b "0.0.0.0:80" --timeout 1800 server:app
