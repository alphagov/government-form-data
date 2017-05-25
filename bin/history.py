#!/usr/bin/env python3

import os
import sys
import json
import csv
import requests
import lxml.html

sep = '\t'

fields = ['page', 'timestamp', 'text']

sep = '\t'

print(sep.join(fields))

for page in csv.DictReader(sys.stdin, delimiter=sep):

    path = 'cache/page/' + page['page']
    dom =  lxml.html.fromstring(open(path).read())

    """
        <div class="js-hidden" id="full-history">
          <ol>
              <li>
                <time datetime="2017-05-12T15:07:46.000+01:00" class="timestamp">12 May 2017</time>
                Updated postal vote form for England
              </li>
    """

    for ol in dom.xpath('//div[@id="full-history"]//ol'):
        for li in ol.xpath('li'):
            row = {}
            row['page'] = page['page']
            row['timestamp'] = li.xpath('//time/@datetime')[0]
            row['text'] = ' '.join(li.text_content().split()[3:])

            print(sep.join([str(row[field]) for field in fields]))
