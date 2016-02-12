# Real Ultimate Search #

This project will crawl, store, and provide a basic UI for search
results. It uses Elasticsearch as its backend, Scrapy for crawling,
and Flask for its UI.
So, we want people to be able to *search* all the content but we don't
want them to be able to *see* the content. Therefore we store an
excerpt and have them click through. The linked system then needs to
verify whether they should have access to see the content.

This is not a very full-featured tool but it should do a basic job of
indexing and providing search results.

## Prerequisites ##

Please install docker and docker-compose.

Go through this project searching for the string `FIXME`. Replace with
the correct settings for your environment.


## Running the thing ##

### Part 1: Data store and UI ###

First, set the URL for where to serve static files:

    echo "STATIC_URL=http://example.com/rus/" > ./static.env

The main docker-compose config file creates two containers: one for
Elasticsearch, and another as a gunicorn+flask web UI. All this can be
started like so:

    docker-compose up

### Part 2: Running a crawl ###

Right now at least, the crawler is not daemonized. It will crawl once
and then be done. It has its own docker container:

    docker-compose -f docker-compose-crawler.yml up

## User-serviceable components ##

Users should access the UI, and that's it. They should not be able to
get to Elasticsearch directly.


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

## HOWTOs ##

### Reindexing ###

This project is designed to do a one-time index. Currently at least,
you need to build a whole new index when you want to "reindex." You
can do this on a non-production box and then copy your index to prod.

### Adding a site ###

If you want to add a new site, you need to update two places:

1. `rus-crawler/rus/spiders/rus_spider.py` -- need to add to
   `allowed_domains` and `start_urls`.
   
2. `rus-ui/ui.py` -- if you want to have a faceted search you want to
   add a new "Site" object to the array for your new site.



