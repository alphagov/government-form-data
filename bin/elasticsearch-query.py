#!/usr/bin/env python3

import os
import csv
from pprint import pprint
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

query = "dormice"

res = es.search(index="form-explorer", body={
    "from": 0,
    "size": 10,
    "_source": {
         "excludes": ["*"],
         "includes": ["attachment"]
    },
    "query": {
        "query_string": {
            "default_field": "text",
            "query": query
        },
    },
    "highlight" : {
        "fields" : {
             "text" : {
                 "fragment_size": 150,
                 "number_of_fragments" : 1
            }
        }
    }
})

pprint(res)
