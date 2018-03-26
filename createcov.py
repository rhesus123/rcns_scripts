#!/usr/bin/python3

import sys

table = open(sys.argv[1])
header = table.readline().rstrip().split("\t")

metadata = open(sys.argv[2])
meta     = dict()
dummycode= dict()
count    = 0
for i in metadata:
    fields = i.rstrip().split("\t")
    if fields[4] not in dummycode:
        dummycode[fields[4]] = str(count)
        sys.stderr.write("%s\t%s\n" % (fields[4], count))
        count += 1
    meta[fields[5]] = dummycode[fields[4]]

print("\t".join(header))
out = list()
out.append("Cancer")
for i in header[1:]:
    out.append(meta[i])
print("\t".join(out))
