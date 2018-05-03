#!/usr/bin/python3

import json
import sys

def getSample(inp):
    for i in inp.split(","):
        raw = i.strip()
        lastpart = raw.split("-")[3][:-1]
        if int(lastpart) < 10:
            return(raw)
    return(inp)

data   = open(sys.argv[1]).read()
ssheet = open(sys.argv[2])
arec   = json.loads(data)

phash  = dict()
ssheet.readline()
for s in ssheet:
    fields = s.rstrip().split("\t")
    sample = getSample(fields[6])
    if sample in phash and fields[4] != phash[sample]:
        print("collision:" + sample + " " + fields[4] + " " + phash[sample], file=sys.stderr)
    phash[sample] = fields[4]

for r in arec:
    filename  = r["file_name"]
    submitter = r['associated_entities'][0]['entity_submitter_id']
    patient = "-".join(submitter.split('-')[:4])
    if int(patient.split("-")[3][:-1]) > 9:
        continue
    print("%s\t%s\t%s\tBreast\tBreast Invasive Carcinoma\t%s" % (filename, submitter, phash[patient], patient))
