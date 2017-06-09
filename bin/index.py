#!/usr/bin/env python3

import os
import csv
from datetime import datetime
from elasticsearch import Elasticsearch

sep = '\t'
index="form-explorer",
doc_type='attachment',

es = Elasticsearch()

for row in csv.DictReader(open("data/attachment.tsv"), delimiter=sep):
    attachment = row['attachment']
    path = "documents/attachment/%s/document.txt" % attachment
    if os.path.isfile(path):
        es.index(index=index, doc_type=doc_type, id=attachment, body={
            'text': open(path).read(),
        })
