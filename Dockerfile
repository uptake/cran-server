FROM continuumio/miniconda3
MAINTAINER Troy de Freitas "troy.defreitas@uptake.com", Nick Paras "nick.paras@uptake.com"

RUN apt-get update -y

RUN pip install flask boto3 gunicorn python-debian

RUN mkdir -p "/opt/cran/uploads" && \
    mkdir -p "/opt/cran/src/contrib/" && \
    mkdir -p "/opt/static" && \
    mkdir -p "/opt/templates" && \
    touch "/opt/cran/src/contrib/PACKAGES"

COPY cranserver/ /opt/cranserver/

ENV FLASK_APP /opt/cranserver/server.py

ENV PYTHONPATH /opt/cranserver/

EXPOSE 8000

CMD gunicorn -w 1 -b "0.0.0.0:80" --timeout 1800 server:app
