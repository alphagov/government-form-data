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

fields = ['attachment', 'filename', 'page', 'name', 'url', 'ref', 'size', 'mime', 'magic']
sep = '\t'

attachments = {}

for page in csv.DictReader(sys.stdin, delimiter=sep):

    path = 'cache/page/' + page['page']
    dom =  lxml.html.fromstring(open(path).read())

    # GOV.UK specific attachment format URL
    for section in dom.xpath('//div[@class="attachment-details"]'):
        for a in section.xpath('.//h2[@class="title"]/a'):
            url = a.xpath('@href')[0]

            if not url.startswith('https'):
                url = "https://www.gov.uk" + url

            if url.endswith('/preview'):
                url = url[:-len('/preview')]

            if '/attachment_data/' in url:
                row = {}
                row['page'] = page['page']
                row['url'] = url
                row['name'] = ' '.join(a.text_content().split())
                row['filename'] = re.sub(r'^.*/', '', url)

                ref = section.xpath('.//span[@class="unique_reference"]')
                row['ref'] = ' '.join(' '.join([r.text_content() for r in ref]).split())

                #
                # cache file
                #
                row['attachment'] = re.sub(r'^.*/attachment_data/file/(\d+).*$', r'\1', url)
                path = 'cache/attachment/%s/%s' % (row['attachment'], row['filename'])
                if not os.path.isfile(path):
                    directory = os.path.dirname(path)
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    print('downloading %s' % path, file=sys.stderr)
                    req = requests.get(row['url'])
                    try:
                        req.raise_for_status()
                        text = req.text
                    except requests.exceptions.HTTPError as error:
                        print(error, file=sys.stderr)
                        text = ''

                    open(path, 'w').write(req.text)

                row['size'] = os.stat(path).st_size
                row['mime'] = magic.from_file(path, mime=True)
                row['magic'] = magic.from_file(path)

                attachments[row['attachment']] = row


print(sep.join(fields))

for attachment in sorted(attachments):
    row = attachments[attachment]
    print(sep.join([str(row[field]) for field in fields]))
