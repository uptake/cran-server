from continuumio/miniconda3
MAINTAINER Troy de Freitas "troy.defreitas@uptake.com", Nick Paras "nick.paras@uptake.com"

RUN apt-get update -y && apt-get install -y python-pip

RUN pip install flask boto3 gunicorn fasteners

RUN mkdir -p "/opt/cran/uploads" && \
    mkdir -p "/opt/cran/src/contrib/" && \
    mkdir -p "/opt/static" && \
    mkdir -p "/opt/templates" && \
    touch "/opt/cran/src/contrib/PACKAGES"


COPY cran-server/ /opt/cranserver/

ENV FLASK_APP /opt/cranserver/server.py

ENV PYTHONPATH /opt/cranserver/

EXPOSE 8000

CMD gunicorn -w 4 -b "0.0.0.0:80" --timeout 1800 server:app
