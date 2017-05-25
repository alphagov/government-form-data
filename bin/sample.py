#!/usr/bin/env python3

import sys
import csv
import re

#
#  hack script to convert form names to references ..
#
fields = ['form', 'page']
sep = '\t'

def n7e(s):
    s = re.sub('[^a-z0-9]', '', s.lower())
    return ''.join(s.split())

pages = {}
for row in csv.DictReader(open('data/page.tsv'), delimiter=sep):
    pages[n7e(row['name'])] = row

attachments = {}
for row in csv.DictReader(open('data/attachment.tsv'), delimiter=sep):
    attachments[n7e(row['name'])] = row


print(sep.join(fields))

for row in csv.DictReader(sys.stdin, delimiter=sep):

    name = n7e(row['name'])

    if name in pages:
        row['page'] = pages[name]['page']
    elif name in attachments:
        row['page'] = attachments[name]['page']
    else:
        row['page'] = '*-*-*- ' + row['name']

    print(sep.join([str(row[field]) for field in fields]))
