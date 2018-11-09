#!/usr/bin/python3

db = open("res")
db.readline()
for i in db:
    fields = i.rstrip().split()
    motifid = fields[0]
    jasparid = fields[2]
    matrixfile = open(jasparid + ".meme")
    counter = 0
    for j in matrixfile:
        mfields = j.rstrip().split()
        if len(mfields) == 4:
            counter = counter + 1
            print(motifid, counter, mfields[0], mfields[1], mfields[2], mfields[3], sep="\t")
    matrixfile.close()
