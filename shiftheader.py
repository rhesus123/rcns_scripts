#!/usr/bin/python3

import sys

count = 0
for i in open(sys.argv[1]):
    if count == 0 and not i.startswith("genes"):
        i = "genes\t" + i
    print(i.rstrip())
    count += 1
