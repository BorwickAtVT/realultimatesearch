FROM phusion/baseimage:0.9.17

# Set install version
ENV DEBIAN_FRONTEND noninteractive
ENV ES_PKG_NAME elasticsearch-2.0.0
#ENV ES_HEAP_SIZE=8g

# add openjdk repo
RUN add-apt-repository ppa:openjdk-r/ppa

# Install dependencies
RUN apt-get update -qq && \
  apt-get install -y -qq \
  wget \
  python \
  openjdk-8-jdk

# Install ElasticSearch
RUN \
 cd / && \
 wget https://download.elasticsearch.org/elasticsearch/release/org/elasticsearch/distribution/tar/elasticsearch/2.0.0/$ES_PKG_NAME.tar.gz && \
 tar xvzf $ES_PKG_NAME.tar.gz && \
 rm -f $ES_PKG_NAME.tar.gz && \
 mv /$ES_PKG_NAME /elasticsearch

# Plugins
RUN /elasticsearch/bin/plugin -i elastic/sense

# Config
ADD elasticsearch.yml /elasticsearch/config/elasticsearch.yml

# Expose ports
EXPOSE 9200
EXPOSE 9300

# Default command
CMD ["/elasticsearch/bin/elasticsearch"]
