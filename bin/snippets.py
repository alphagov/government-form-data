#!/usr/bin/env python3

import sys
import csv
from PIL import Image

prefix = 'https://s3-eu-west-1.amazonaws.com/government-form/'

sep = '\t'
for row in csv.DictReader(sys.stdin, delimiter=sep):

    path = row['url']
    if path.startswith(prefix):
        path = path[len(prefix):]

    original = Image.open(path)
    snippet = original.crop((int(row['left']), int(row['top']), int(row['right']), int(row['bottom'])))

    snippet_path = 'documents/snippet/%s.png' % (row['snippet'])

    f = open(snippet_path, "wb")
    snippet.save(f, format='PNG')
    f.close()
