#!/usr/bin/python

import sys

region = dict()
for i in open(sys.argv[1]):
	fields = i.rstrip().split()
	if fields[0] not in region:
		region[fields[0]] = dict()
	start = int(fields[1])
	end   = int(fields[2])
	for j in range(start, end + 1):
		region[fields[0]][j] = 0

for i in open(sys.argv[2]):
	fields = i.rstrip().split()
	pos = int(fields[1])
	region[fields[0]][pos] = int(fields[2])

for chrx in region:
	for pos in region[chrx]:
		print region[chrx][pos]
