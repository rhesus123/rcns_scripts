#!/usr/bin/python3

import json
import sys

data = open(sys.argv[1]).read()
arec = json.loads(data)

for r in arec:
    filename  = r["file_name"]
    submitter = r['associated_entities'][0]['entity_submitter_id']
    patient = "-".join(submitter.split('-')[:4])
    print("%s\t%s\tTCGA-BRCA\tBreast\tBreast Invasive Carcinoma\t%s" % (filename, submitter, patient))
