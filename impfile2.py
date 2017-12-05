#!/usr/bin/python3

import MySQLdb
import sys
import json

db = MySQLdb.connect(host="localhost", user="XXX", passwd="XXXX", db="TCGA")
c = db.cursor()
d = open(sys.argv[1]).read()
j = json.loads(d)
for rec in j:
    c.execute("select patientid from patient where patientname = '" + rec["cases"][0]["submitter_id"] + "';")
    print(rec["file_name"], rec["cases"][0]["submitter_id"])
    userid = c.fetchone()
    if userid is None:
        continue
    userid = userid[0]
    cmd = ("insert into BAM (filename, istumour, patientid, type) values('%s', 1, %d, 'rna-seq');") % (rec["file_name"], userid)
    print(cmd)
    c.execute(cmd)
db.commit()
db.close()
