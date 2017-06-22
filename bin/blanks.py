#!/usr/bin/env python3

import sys
import re

s = sys.stdin.read()

# remove trailing whitespace
s = '\n'.join([w.rstrip() for w in s.split('\n')])

# at most one blank line
s = re.sub(r'\n\n+', '\n\n', s)

s = s.strip()
print(s)
