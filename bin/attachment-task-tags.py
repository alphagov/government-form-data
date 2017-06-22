#!/usr/bin/env python3

import os
import sys
import csv

sep = '\t'

fields = ['attachment', 'tag']

pages={}
for row in csv.DictReader(open('data/task.tsv'), delimiter=sep):
    pages[row['page']] = row['task']

print(sep.join(fields))

for row in csv.DictReader(open('data/attachment.tsv'), delimiter=sep):
    if row['page'] in pages:
        row['tag'] = pages[row['page']]
        print(sep.join([row[field] for field in fields]))
