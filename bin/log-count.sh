#!/bin/bash

# process GOV.UK digested CDN logs:
# 10 /government/uploads/system/uploads/attachment_data/file/98864/thumbnail_emr-2010-11.pdf.png GET 200 origin,2

# output TSV:
# 20150705  385310/ENFORCEMENT_BY_DEDUCTION_FROM_ACCOUNTS.pdf 3

# TBD: count by status code ..

find daily -type d -name '20??????' |
  while read dir
  do
    date=$(echo "$dir" | sed -e 's/^.*\(20[0-9]*\).*$/\1/')
    zcat $dir/count_cdn-govuk.log-20*.csv.gz |
    sed -e 's/^[0-9][0-9] //' \
        -e '/^\/government\/uploads\/system\/uploads\/attachment_data\/file\//!d' \
        -e 's/^.*\/file\/\([^ ]*\).*,\([0-9]*\).*$/\1 \2/' \
        -e '/\.png/d' |
    awk '{ count[$1] += $2 }
    END { for (key in count) {
      print "'"$date"'\t" key "\t" count[key]
    }}'
  done
