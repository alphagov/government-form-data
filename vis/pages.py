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

pages = load('page')
tasks = load('task')
attachments = load('attachment')

#
#  tag sampled pages
#
for task, t in tasks.items():
    pages[t['page']]['task'] = task

#
#  index attachments per-page
#
for attachment, a in attachments.items():
    page = a['page']
    p = pages[page]
    p['attachments'] = p.get('attachments', []) + [attachment]
    p['size'] = p.get('size', 0) + int(a['size'])

#
#  index updates per-page
#
for h in csv.DictReader(open('data/history.tsv'), delimiter=sep):
    p = pages[h['page']]
    p['history'] = p.get('history', []) + [h['timestamp']]

#
#  index downloads
#
for h in csv.DictReader(open('data/download.tsv'), delimiter=sep):
    a = attachments[h['attachment']]
    p = pages[a['page']]
    p['downloads'] = p.get('downloads', 0) + int(h['count']) /10000


rows = []
for page, p in pages.items():

    row = {}
    row['page'] = page
    row['task'] = p.get('task', '')
    row['sample'] = 'sample' if 'task' in p else 'not'
    row['Number of organisations'] = len(p['organisations'].split(';')) /100
    row['Number of attachments'] = len(p.get('attachments', [])) /100
    row['Total size'] = "{:.8f}".format(p.get('size', 0) / (10*1024*1024))
    row['Number of updates'] = len(p.get('history', [])) / 100
    row['Number of downloads'] = "{:.8f}".format(p.get('downloads', 0) / 10000)

    rows.append(row)


fields = ['page', 'task', 'sample', 'Number of organisations', 'Number of attachments', 'Total size', 'Number of updates', 'Number of downloads']

print(sep.join(fields))
for row in sorted(rows, key=lambda k: k['sample']+k['page']):
    print(sep.join([str(row[field]).strip() for field in fields]))
