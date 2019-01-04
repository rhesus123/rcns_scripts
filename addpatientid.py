#!/usr/bin/python3

"""
  Read fusion table and add TCGA patient ID from downloaded metadata
"""

import sys
import json

sub2patient = dict()
data = open(sys.argv[2]).read()
allrecords = json.loads(data)
for record in allrecords:
    submitter = record["submitter_id"]
    patient   = "-".join(record["associated_entities"][0]["entity_submitter_id"].split("-")[:4])
    sub2patient[submitter] = patient

for i in open(sys.argv[1]):
    fields = i.rstrip().split("\t")
    if fields[0] in sub2patient:
        fields = [sub2patient[fields[0]]] + fields
    else:
        fields = ["PatientID"] + fields # The only entry where there is no corrispondence is the header
    print("\t".join(fields))
