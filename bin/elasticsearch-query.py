#!/usr/bin/env python3

import os
import csv
from datetime import datetime
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

sep = '\t'
index="form-explorer",
doc_type='attachment',


def env(name):
    return os.environ['ES_' + name]


if 'ES_HOST' in os.environ:
    REGION=env('REGION')
    HOST=env('HOST')

    awsauth = AWS4Auth(env('ACCESS_KEY'), env('SECRET_KEY'), env('REGION'), 'es')
    es = Elasticsearch(
        hosts=[{'host': env('HOST'), 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
else:
    es = Elasticsearch()

res = es.search(index="form-explorer", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print("%s" % hit['_id'])
