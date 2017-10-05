#!/usr/bin/python3

"""
   Extract usefull information from TCGA JSON metadata
"""

import sys
import json

for filename in sys.argv[2:]:
    data = open(filename).read()
    allrecords = json.loads(data)
    for record in allrecords:
        if record["file_name"].endswith(sys.argv[1]):
            filename  = record["file_name"]
            entity    = record["associated_entities"][0]["entity_submitter_id"]

            case      = record["cases"][0]
            project   = case["project"]["project_id"]
            organ     = case["primary_site"]
            disease   = case["disease_type"]

            sample    = case["samples"][0]
            submitter = sample["submitter_id"]
            print(filename, entity, project, organ, disease, submitter, sep = "\t")
