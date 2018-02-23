#!/usr/bin/python3

import sys
import re

yearpatt = re.compile("\((\d+)\)")

print("Author\tYear\tTitle\tJournal\tVolume\tPage")

for i in open(sys.argv[1]):
    line = i.rstrip()
    if len(line) == 0:
        continue
    first, second = line.split(":", 1)
    match = yearpatt.search(first)
    if match:
        year = match.group(1)
    else:
        print("Fuck")
    authors = first.split("(")[0]
    authors = authors.replace(".,", ".//")
    chunks  = re.split("[.?]", second)
    if len(chunks) != 3:
        print(line, file=sys.stderr)
        continue
    title = chunks[0]
    articlechunks = chunks[1].split(",")
    if len(articlechunks) != 3:
        print(line, file=sys.stderr)
        continue
    journal = articlechunks[0].strip()
    volume  = articlechunks[1]
    page    = articlechunks[2].strip()
    print(authors, year, title, journal, volume, page, sep = "\t")
