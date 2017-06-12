#!/usr/bin/env python3

import sys
import re
from glob import glob
from nltk import ngrams
from collections import Counter
from itertools import chain

length = 3
if len(sys.argv) > 1:
    length = int(sys.argv[1])

pattern = re.compile('[^a-z]+')

grams = []

for path in glob('documents/attachment/*/document.txt'):

    text = open(path).read()
    text = pattern.sub(' ', text.lower())
    text = text.split()

    g = ngrams(text, length)
    g = list(set(list(g)))
    grams = grams + g


counts = Counter(grams)

print("count\tngram")

for r in counts.most_common():
    if r[1] < 10:
        break
    print("%s\t%s" % (r[1], ' '.join(r[0])))
