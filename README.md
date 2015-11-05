# Real Ultimate Search #

This project will crawl, store, and provide a basic UI for search
results. It uses Elasticsearch as its backend, Scrapy for crawling,
and Flask for its UI.

This is not a very full-featured tool but it should do a basic job of
indexing and providing search results.

## Prerequisites ##

Please install docker and docker-compose.

Go through this project searching for the string `FIXME`. Replace with
the correct settings for your environment.


## Running the thing ##

### Part 1: Data store and UI ###

The main docker-compose config file creates two containers: one for
Elasticsearch, and another as a gunicorn+flask web UI. All this can be
started like so:

    docker-compose up

### Part 2: Running a crawl ###

Right now at least, the crawler is not daemonized. It will crawl once
and then be done. It has its own docker container:

    docker-compose -f docker-compose-crawler.yml up

## User-accessible components ##

Users should access the UI, and that's it. The way this project is
currently designed, they should only access the UI via a trusted
reverse proxy such as nginx.

They definitely should not be able to get to Elasticsearch directly.


## Output/storage ##

Each docker container generates output to stdout and probably stderr.
This should ideally be captured.

* `rus-es-data`: The elasticsearch will save its data store to this directory
unless otherwise specified.

* `rus-crawler-data`: The crawler will save a gzipped HTTP cache to the directory
`httpcache` unless otherwise specified. This is supposed to make it
less painful to stop and restart the crawler.

* `rus-ui-data`: The search UI will write logs into this directory.

## Notes/TODOs ##

* Currently Elasticsearch does not use any usernames/passwords.
