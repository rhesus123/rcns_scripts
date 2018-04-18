#!/usr/bin/python3

from lxml import etree
import sys

def getText(element, tag):
    for child in element:
        if child.tag == tag:
            return child.text
    return None

def getExpression(element):
    ret = dict()
    for child in element:
        if child.tag == "data":
            tissue = child[0].text
            level  = child[1].text
            ret[tissue] = level
    return ret

xmlfile = open(sys.argv[1], "rb")

allsamples = set()
table = dict()
for _,entry in etree.iterparse(xmlfile, tag = "entry"):
    genename = getText(entry, "name")
    for child in entry:
        if child.tag == "tissueExpression":
            expression = getExpression(child)
            allsamples.update(expression.keys())
            if len(expression.keys()) > 0:
                if genename in table:
                    # Print out problematic parts, but still overwrite old results
                    print("Overwrite " + genename, file=sys.stderr)
                    print(table[genename], file = sys.stderr)
                    print(expression, file = sys.stderr)
                table[genename] = expression
    entry.clear()

allsamples = list(allsamples)
print("\t".join(allsamples))
for genename in table:
    out = [genename]
    for s in allsamples:
        if s in table[genename]:
            out.append(table[genename][s])
        else:
            out.append("NA")
    print("\t".join(out))
