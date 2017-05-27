#!/usr/bin/env python3

#
#  assemble organisations from registers
#

import io
import csv
import requests
from natsort import natsorted


class Records:
    "Minimal register client"

    records = {}
    url = 'https://%s.register.gov.uk/records.tsv?page-size=%s'

    def load(self, register, url=None, page_size=5000):
        if url is None:
            url = self.url
        resp = requests.get(url=url % (register, page_size))
        resp.raise_for_status()

        for row in csv.DictReader(io.StringIO(resp.text), delimiter='\t'):
            self.records['%s:%s' % (register, row[register])] = row

    def dump(self, fields, sep='\t'):
        key = fields[0]
        print(sep.join(fields))
        for record in natsorted(self.records):
            row = self.records[record]
            row[key] = record

            print(sep.join([str(row.get(field, '')) for field in fields]))


organisations = Records()
organisations.load('government-organisation')
organisations.dump(['organisation', 'name', 'website', 'start-date', 'end-date'])
