#!/usr/bin/env python3

import os
import sys
import re
import csv
import magic
import lxml.html
import requests

#
#  make attachements.tsv from page.tsv and cached files
#

fields = ['attachment', 'filename', 'page', 'name', 'url', 'size', 'mime', 'magic']
sep = '\t'

attachments = {}

for page in csv.DictReader(sys.stdin, delimiter=sep):

    path = 'cache/page/' + page['page']
    dom =  lxml.html.fromstring(open(path).read())

    # GOV.UK specific attachment format URL
    for a in dom.xpath('//a'):
        url = a.xpath('@href')[0]

        if '/attachment_data/' in url:
            if not url.startswith('https'):
                url = "https://www.gov.uk" + url

            if url.endswith('/preview'):
                url = url[:-len('/preview')]

            row = {}
            row['page'] = page['page']
            row['url'] = url
            row['filename'] = re.sub(r'^.*/', '', url)
            row['attachment'] = re.sub(r'^.*/attachment_data/file/(\d+).*$', r'\1', url)
            row['name'] = ' '.join(a.text_content().split())

            #
            # cache file
            #
            path = 'cache/attachment/%s/%s' % (row['attachment'], row['filename'])
            if not os.path.isfile(path):
                directory = os.path.dirname(path)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                print('downloading %s' % path, file=sys.stderr)
                req = requests.get(row['url'])
                req.raise_for_status()
                open(path, 'w').write(req.text)

            row['size'] = os.stat(path).st_size
            row['mime'] = magic.from_file(path, mime=True)
            row['magic'] = magic.from_file(path)

            attachments[row['attachment']] = row


print(sep.join(fields))

for attachment in sorted(attachments):
    row = attachments[attachment]
    print(sep.join([str(row[field]) for field in fields]))
