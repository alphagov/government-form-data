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
            'size': org.get('size', 0)
        }
        tree['children'].append(node)

print(json.dumps(tree, sort_keys=True, indent=2))
