#!/usr/bin/python3

import sys

for i in sys.argv[1:]:
    matrix = open(i)
    header = matrix.readline().rstrip().split("\t")
    patient = set()
    for h in header[1:]:
        patient.add("-".join(h.split("-")[0:4]))
    matrix.close()
    if(len(header) != len(patient)):
        print(i + " is suck")
