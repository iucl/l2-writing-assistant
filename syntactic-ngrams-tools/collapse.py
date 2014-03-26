#!/usr/bin/env/python3

"""
Input format looks like:

head<TAB>dependent<TAB>label<TAB>count

... if we see two lines next to each other that are the same, add up the counts.
"""

import fileinput

prevbody = None
totalcount = 0
for line in fileinput.input():
    line = line.strip()
    body, count = line.rsplit("\t", maxsplit=1)
    count = int(count)
    if body == prevbody:
        totalcount += count
    else:
        print("{0}\t{1}".format(prevbody, totalcount))
        prevbody = body
        totalcount = count

print("{0}\t{1}".format(prevbody, totalcount))
