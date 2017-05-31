#!/usr/bin/env python3

# download paginated json as jsonl

import sys
import requests
import json

url = "https://www.gov.uk/api/search.json?filter_content_store_document_type=form&start=%s&count=%s"
start = 0
count = 1000
total = 999999

while start < total:
    resp = requests.get(url=url % (start, count))
    resp.raise_for_status()
    r = json.loads(resp.text)

    for row in r['results']:
        json.dump(row, sys.stdout, sort_keys=True)
        print()

    start = r['start'] + count
    total = r['total']
