import os

from flask import Flask, url_for, redirect
from flask import render_template
from flask import request

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

app = Flask(__name__)
client = Elasticsearch(os.environ['ES_PORT_9200_TCP_ADDR'],
                       port=os.environ['ES_PORT_9200_TCP_PORT'],
                       )

PAGE_SIZE = 10


class Site(object):
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
    return redirect(url_for('search'))


@app.route("/search")
def search():
    query_string = request.args.get('q')
    site_pk = request.args.get('site')
    offset = int(request.args.get('offset', '0'))
    response = None
    prev_link = None
    next_link = None
    window_offset = None        # the largest result number seen on the page

    if site_pk:
        # gets very angry on misses
        site = [x for x in SITES if x.pk == site_pk][0]
    else:
        site = None

    if query_string is not None:
        s = Search(using=client).query("simple_query_string",
                                       query=query_string,
                                       fields=['fulltext', 'title'])

        if site:
            s = s.query(site.query)

        response = s[offset:offset+PAGE_SIZE].execute()
        window_offset = min(offset+PAGE_SIZE, response.hits.total)

        if offset > 0:
            prev_offset = offset - PAGE_SIZE
            if prev_offset < 0:
                prev_offset = 0
            prev_link = u"?q={}&offset={}".format(query_string, prev_offset)

        if response.hits.total > (offset + PAGE_SIZE):
            next_offset = offset + PAGE_SIZE
            next_link = u"?q={}&offset={}".format(query_string, next_offset)

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
