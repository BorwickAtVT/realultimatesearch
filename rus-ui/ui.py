"""
This code lets people search through the full text index, but only
see the excerpt. It links people to the actual content.

This code does not do any indexing itself--it just serves up
whatever's in Elasticsearch. Fundamentally this exists to keep users
from being able to search directly via full text, which may be
restricted.
"""
import os

from flask import Flask, url_for, redirect
from flask import render_template
from flask import request

from elasticsearch import Elasticsearch
# this makes it easier to build Elasticsearch queries:
from elasticsearch_dsl import Search, Q

app = Flask(__name__)
# app.debug = True
# Connection to Elasticsearch:
client = Elasticsearch(os.environ['ES_PORT_9200_TCP_ADDR'],
                       port=os.environ['ES_PORT_9200_TCP_PORT'],
                       )
PAGE_SIZE = 10                  # How many search results per page?


class Site(object):
    """
    Simple class to let you link (a) a human-readable name to (b) an
    Elasticsearch query to (c) a primary key that can be specified in
    the URL.
    """
    def __init__(self, name, query, pk):
        self.name = name
        self.query = query
        self.pk = pk

SITES = (
         Site(name="FIXME",
              pk="fixme",
              query=Q("prefix", url="http://path.to.site.example.com/subdir/"),
              ),
         Site(name="FIXME 2",
              pk="fixme2",
              query=Q("prefix", url="http://other.example.com/"),
              ),
         Site(name="Bunch o' FIXME sites",
              pk="bunch",
              query=Q("bool",
                      should=[Q("prefix", url="http://site1.example.com/"),
                              Q("prefix", url="http://site2.example.com/test/")
                              ]),
              ),
    )


@app.context_processor
def inject_static_url():
    """
    Inject the variable 'static_url' into the templates. Grab it from
    the environment variable STATIC_URL, or use the default.

    Template variable will always have a trailing slash.

    """
    static_url = os.environ.get('STATIC_URL', app.static_url_path)
    if not static_url.endswith('/'):
        static_url += '/'
    return dict(
        static_url=static_url
    )

@app.route("/")
def index():
    "Redirect to /search"
    return redirect(url_for('search'))


@app.route("/search")
def search():
    """
    The only actually useful function. Shows the search box. If there
    was a search, also displays search results.
    """
    query_string = request.args.get('q') # the search string
    site_pk = request.args.get('site')   # Site's pk
    offset = int(request.args.get('offset', '0')) # start with what result?
    response = None                               # search result object
    prev_link = None                              # URL for previous page
    next_link = None                              # URL for next page
    window_offset = None        # the largest result number seen on the page

    if site_pk:
        # gets very angry on misses--500 error
        try:
            site = [x for x in SITES if x.pk == site_pk][0]
        except IndexError:
            return 'Site not found', 400
    else:
        site = None

    if query_string is not None:
        s = Search(using=client).query("simple_query_string",
                                       query=query_string,
                                       fields=['fulltext', 'title'])

        if site:
            # This ANDs the above simple_string_query with whatever
            # query is specified in the site object.
            s = s.query(site.query)

        # You use the offset syntax [begin:end] to tell Elasticsearch
        # which results to return.
        response = s[offset:offset+PAGE_SIZE].execute()
        # This is the highest-numbered item in the current page of
        # results, so that the code can say "11 to *20* out of 310"
        # (where 20 is the window_offset in this example).
        window_offset = min(offset+PAGE_SIZE, response.hits.total)

        # prev_link only exists if offset>0
        if offset > 0:
            prev_offset = offset - PAGE_SIZE
            if prev_offset < 0:
                prev_offset = 0
            prev_link = u"?q={}&offset={}".format(query_string, prev_offset)
            if site_pk:
                prev_link += '&site={}'.format(site_pk)

        # if there are more results, need next_link
        if response.hits.total > (offset + PAGE_SIZE):
            next_offset = offset + PAGE_SIZE
            next_link = u"?q={}&offset={}".format(query_string, next_offset)
            if site_pk:
                next_link += '&site={}'.format(site_pk)

    # let the template do the rest
    return render_template('search.html',
                           results=response,
                           q=query_string,
                           prev_link=prev_link,
                           next_link=next_link,
                           offset=offset,
                           window_offset=window_offset,
                           sites=SITES,
                           cur_site=site,
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0')
