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

metadata = {}

for row in csv.DictReader(open("data/attachment-metadata.tsv"), delimiter=sep):
    metadata[row['attachment']] = row

for row in csv.DictReader(open("data/attachment.tsv"), delimiter=sep):
    attachment = row['attachment']
    path = "documents/attachment/%s/document.txt" % attachment

    if os.path.isfile(path):
        row['text'] = open(path).read()

        if attachment in metadata:
            row = {**row, **metadata[attachment]}

        row = {k: v for k, v in row.items() if len(v) > 0}

        print(attachment)
        es.index(index=index, doc_type=doc_type, id=attachment, body=row)
