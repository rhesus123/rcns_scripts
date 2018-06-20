#!/usr/bin/python3

import sys

samples = dict()

exp = open(sys.argv[1])
header = exp.readline().rstrip().split("\t")

for i in range(len(header)):
    h = header[i]

    patient = "-".join(h.split("-")[0:3])
    if patient not in samples:
        samples[patient] = dict()
    samples[patient][h] = i

mean = [0.0] * len(header)
n = 0.0
for i in exp:
    fields = i.rstrip().split()
    for j in range(1, len(header)):
        mean[j] += float(fields[j])
    n += 1.0

exp.close()

for j in range(1, len(header)):
    mean[j] = mean[j] / n

keep = set()
keep.add(0) # Always keep the first column
for patient in samples:
    if len(samples[patient].keys()) > 1:
        maxv = 0.0
        maxi = 0
        for sampleid in samples[patient]:
            index = samples[patient][sampleid]
            if mean[index] > maxv:
                maxi = index
                maxv = mean[index]
        keep.add(maxi)
    else:
        l = list(samples[patient].values())
        keep.add(l[0])

exp = open(sys.argv[1])
for i in exp:
    fields = i.rstrip().split("\t")
    out = list()
    for f in range(len(fields)):
        if f in keep:
            out.append(fields[f])
    print("\t".join(out))
exp.close()
