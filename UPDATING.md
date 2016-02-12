## 20151222 ##

  Removed HTTP cache, replacing it with scrapy jobs (which I didn't
  know about before).

  To run a crawl, you will (once) need to erase whatever's in `rus-crawler-data`:

    rm -f rus-crawler-data/*

  The "upgrade path" right now is building a whole new ElasticSearch
  index. I know that's not a great upgrade path. Ideally you run it
  elsewhere and then copy over the data to prod when you're ready.

