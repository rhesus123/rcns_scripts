#!/usr/bin/python3

import MySQLdb
import sys

db = MySQLdb.connect(host="localhost", user="XXXX", passwd="XXXX", db="TCGA")
c = db.cursor()

for i in open(sys.argv[1]):
    fields = i.rstrip().split("\t")
    user   = fields[0]
    if "tumor" in fields[1]:
        istumour = "1"
    else:
        istumour = "0"
    filename = fields[2]
    c.execute("select patientid from patient where patientname = '" + user + "';")
    userid = str(c.fetchone()[0])
    cmd = "insert into BAM (filename, istumour, patientid, type) values('"+filename+"', "+istumour+", "+userid+", 'exome');"
    c.execute(cmd)
    print(c.lastrowid)
db.commit()
db.close()
