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

@app.route("/")
def index():
    return redirect(url_for('search'))


@app.route("/search")
def search():
    query_string = request.args.get('q')
    offset = int(request.args.get('offset','0'))
    response = None
    prev_link = None
    next_link = None
    window_offset = None        # the largest result number seen on the page
    
    if query_string is not None:
        s = Search(using=client).query("simple_query_string",
                                       query=query_string,
                                       fields=['fulltext', 'title'])
        response = s[offset:offset+PAGE_SIZE].execute()
        window_offset = min(offset+PAGE_SIZE, response.hits.total)

        if offset > 0:
            prev_offset = offset - PAGE_SIZE
            if prev_offset < 0:
                prev_offset = 0
            prev_link = u"?q={}&offset={}".format(query_string, prev_offset)

        if response.hits.total > ( offset + PAGE_SIZE ):
            next_offset = offset + PAGE_SIZE
            next_link = u"?q={}&offset={}".format(query_string, next_offset)

    return render_template('search.html',
                           results=response,
                           q=query_string,
                           prev_link=prev_link,
                           next_link=next_link,
                           offset=offset,
                           window_offset=window_offset,
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0')
