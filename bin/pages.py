#!/usr/bin/env python3

import os
import sys
import json
import csv
import requests

sep = '\t'
list_sep = ';'

#
#  load GOV.UK slug to organisation map
#
slugs = {}
for row in csv.DictReader(open('data/slug.tsv'), delimiter=sep):
    slugs[row['slug']] = row


def organisations(organisations):
    orgs = {}
    for org in organisations:
        orgs[slugs[org['slug']]['organisation']] = org
    return list(orgs.keys())


fields = ['page', 'name', 'url', 'organisations']

print(sep.join(fields))

for line in sys.stdin:
    r = json.loads(line)

    row = {}
    row['page'] = r['_id'].replace('/government/publications/', '')
    row['name'] = ' '.join(r['title'].split())

    row['description'] = ' '.join(r['description'].split())

    row['timestamp'] = r['title']
    row['url'] = 'https://www.gov.uk' +r['_id']
    row['organisations'] = ';'.join(sorted(organisations(r['organisations'])))

    print(sep.join([row[field] for field in fields]))

    #
    #  cache the page ..
    #
    path = 'cache/page/%s' % (row['page'])
    if not os.path.isfile(path):
        print('downloading %s' % path, file=sys.stderr)
        req = requests.get(row['url'])
        req.raise_for_status()
        open(path, 'w').write(req.text)
