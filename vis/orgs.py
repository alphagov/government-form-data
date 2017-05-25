#!/usr/bin/env python3

#
#  make json data for a treemap of pages by department
#

import sys
import csv
import json

sep = '\t'

def load(name, key=None):
    rows = {}
    if not key:
        key = name
    for row in csv.DictReader(open('data/%s.tsv' % name), delimiter=sep):
        rows[row[key]] = row
    return rows


pages = load('page')
attachments = load('attachment')
organisations = load('organisation')

#
#  index pages per-organisation
#
for page, p in pages.items():
    for organisation in p['organisations'].split(';'):
        organisations[organisation]['pages'] = organisations[organisation].get('pages', []) + [page]

#
#  index attachments per-page
#
for attachment, a in attachments.items():
    page = a['page']
    p = pages[page]
    for organisation in p['organisations'].split(';'):
        organisations[organisation]['attachments'] = organisations[organisation].get('attachments', []) + [attachment]
        organisations[organisation]['size'] = organisations[organisation].get('size', 0) + int(a['size'])

#
#  index updates per-page
#
for h in csv.DictReader(open('data/history.tsv'), delimiter=sep):
    p = pages[h['page']]
    for organisation in p['organisations'].split(';'):
        organisations[organisation]['updates'] = organisations[organisation].get('updates', 0) + 1

#
#  index downloads per-attachment
#
for h in csv.DictReader(open('data/download.tsv'), delimiter=sep):
    a = attachments[h['attachment']]
    p = pages[a['page']]
    for organisation in p['organisations'].split(';'):
        organisations[organisation]['downloads'] = organisations[organisation].get('downloads', 1) + int(h['count'])


#
#  make treemap json
#
tree = {
    'name': 'pages',
    'children': []
}

for organisation in sorted(organisations):
    org = organisations[organisation]
    if 'pages' in org:
        node = {
            'name': org['name'],
            'pages': len(org['pages']),
            'attachments': len(org.get('attachments', [])),
            'size': org.get('size', 0),
            'updates': org.get('updates', 0),
            'downloads': org.get('downloads', 0)
        }
        tree['children'].append(node)

print(json.dumps(tree, sort_keys=True, indent=2))
