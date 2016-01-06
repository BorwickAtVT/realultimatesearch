FROM phusion/baseimage:0.9.17

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -qq && \
    apt-get install -y -qq \
    python python-dev python-pip

ADD requirements.txt ui.py gunicorn.py.ini /data/
ADD templates /data/templates/

WORKDIR /data
RUN pip -q install -r requirements.txt

VOLUME /data/logs

EXPOSE 8000

CMD ["/usr/local/bin/gunicorn","-c","gunicorn.py.ini","ui:app"]
