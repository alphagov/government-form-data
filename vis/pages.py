#!/usr/bin/env python3

#
#  make TSV for scatterplot matrix of pages
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


def govuk_name(govuk):
    org = govuks[govuk]['government-organisation']

    if org in government_organisations:
        return government_organisations[org]['name']

    # courts and tribunals are in another register, TBD ..
    return govuk


pages = load('page')
attachments = load('attachment')
files = load('file', 'attachment')
government_organisations = load('government-organisation')
govuks = load('govuk')

#
#  index pages per-GOV.UK publisher
#
for page, p in pages.items():
    for govuk in p['govuks'].split(';'):
        govuks[govuk]['pages'] = govuks[govuk].get('pages', []) + [page]

#
#  index attachments per-page
#
for attachment, a in attachments.items():
    for page in a['pages'].split(';'):
        pages[page]['attachments'] = pages[page].get('attachments', []) + [attachment]


#
#  make treemap json
#
tree = {
    'name': 'pages',
    'children': []
}

for govuk in sorted(govuks):
    if 'pages' in govuks[govuk]:
        node = {
            'name': govuk_name(govuk),
            'size': len(govuks[govuk]['pages'])
        }
        tree['children'].append(node)

print(json.dumps(tree, sort_keys=True, indent=2))
