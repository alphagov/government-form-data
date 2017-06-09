#!/usr/bin/env python3

import sys
import re
from collections import Counter
from itertools import chain


pattern = re.compile('[^\w]+')


def word(line):
    line = pattern.sub(' ', line.lower())
    return line.split()


counts = Counter(chain.from_iterable(map(word, sys.stdin)))

for r in counts.most_common():
    if r[1] < 100:
        break
    print("%s\t%s" % r)
