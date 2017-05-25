#!/usr/bin/env python3

import os
import sys
import csv

# make download.tsv from CDN counts
# 20150705  385310/ENFORCEMENT_BY_DEDUCTION_FROM_ACCOUNTS.pdf 3

fields = ['date', 'attachment', 'count']
sep = '\t'

#
#  load whitelist of attachments ..
#
attachments = {}
for row in csv.DictReader(open('data/attachment.tsv'), delimiter=sep):
    attachments[row['attachment']] = row

dates = {}
for line in sys.stdin:
    r = line.strip().split(sep)
    date = r[0]

    if len(date) == 8:
        date = date[:6]
        attachment = r[1].split('/')[0]
        if attachment in attachments:
            if date not in dates:
                dates[date] = {}

            dates[date][attachment] = dates[date].get(attachment, 0) + int(r[2])

print(sep.join(fields))

for date in sorted(dates):
    for attachment in sorted(dates[date]):
        print(sep.join([date, attachment, str(dates[date][attachment])]))
