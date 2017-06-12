#!/usr/bin/env python3

#
#  extract document metadata from Tika json
#

import os
import csv
import json
from datetime import datetime

sep = '\t'
fields = ['attachment', 'created', 'modified', 'page-count']

attachments = {}

for row in csv.DictReader(open("data/attachment.tsv"), delimiter=sep):
    attachment = row['attachment']
    path = "documents/attachment/%s/document.json" % attachment

    if os.path.isfile(path) and os.path.getsize(path) > 0:
        meta = json.load(open(path))

        row['created'] = meta.get('Creation-Date', '')
        row['modified'] = meta.get('Last-Modified', '')
        row['page-count'] = meta.get('xmpTPg:NPages', '')

        attachments[attachment] = row


print(sep.join(fields))

for attachment in sorted(attachments):
    row = attachments[attachment]
    print(sep.join([str(row[field]) for field in fields]))
