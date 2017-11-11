#!/usr/bin/env  python3

import csv
from operator import itemgetter
from scipy.stats import hmean

sep = '\t'
list_sep = ';'

organisations = {}
pages = {}
attachments = {}

moj_orgs = {
    'government-organisation:EA556',    # Legal Aid Agency
    'government-organisation:EA72',     # Office of the Public Guardian
    'government-organisation:D18',      # Ministry of Justice
    'government-organisation:EA73',     # HM Courts & Tribunals Serivce
    'government-organisation:EA1213',   # Her Majesty’s Prison and Probation Service
}

cols = [
    'organisations', 'page', 'page-name', 'tags',
    'attachment', 'filename', 'ref', 'mime', 'size',
    'downloads-count', 'downloads-mean', 'downloads-peak',
]


def reader(name):
    return csv.DictReader(open('data/%s.tsv' % name), delimiter=sep)


for row in reader('organisation'):
    organisations[row['organisation']] = row

for row in reader('page'):
    row['organisations'] = row['organisations'].split(list_sep)
    pages[row['page']] = row

for row in reader('attachment'):
    row['tags'] = []
    row['downloads'] = {}
    attachments[row['attachment']] = row

for row in reader('download'):
    attachment = row['attachment']
    if attachment in attachments:
        attachments[attachment]['downloads'][row['date']] = int(row['count'])

for row in reader('tag'):
    for attachment in row['attachments'].split(list_sep):
        if attachment in attachments:
            attachments[attachment]['tags'].append(row['tag'])

print(sep.join(cols))

for attachment in sorted(attachments):
    row = attachments[attachment]
    orgs = pages[row['page']]['organisations']

    if set(orgs).intersection(moj_orgs):
        row['page-name'] = pages[row['page']]['name']
        row['tags'] = list_sep.join(row['tags'])
        row['organisations'] = list_sep.join(organisations[org]['name'] for org in orgs)

        counts = [int(row['downloads'][d]) for d in row['downloads']]
        if len(counts):
            row['downloads-count'] = len(counts)
            row['downloads-mean'] = int(round(hmean(counts)))
            row['downloads-peak'] = max(counts)

        print(sep.join([str(row.get(col, '')) for col in cols]))
