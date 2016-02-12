FROM phusion/baseimage:0.9.18

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -qq && \
    apt-get install -y -qq \
    python python-dev python-pip \
    libxml2-dev libxslt1-dev antiword unrtf \
    poppler-utils pstotext tesseract-ocr \
    flac lame libmad0 libsox-fmt-mp3 sox \
    zlib1g-dev libjpeg-dev libffi-dev libssl-dev

ADD requirements.txt scrapy.cfg /data/
ADD rus /data/rus/

VOLUME /data/.scrapy/httpcache

WORKDIR /data
RUN pip -q install -r requirements.txt

CMD ["/usr/local/bin/scrapy","crawl","rus","-s","JOBDIR=/data/crawljob"]
