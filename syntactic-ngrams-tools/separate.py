#!/usr/bin/env/python3

"""
Take a file in the syntactic ngrams format, separate out the dependencies when
there's more than one on a line.

Output format looks like:

head<TAB>dependent<TAB>label<TAB>count

... we'll have to add these up next.
"""

import fileinput

for line in fileinput.input():
    line = line.strip()
    headword, relationships, count, years = line.split("\t", maxsplit=3)
    count = int(count)
    
    rels = relationships.split()
    thewords = []
    for rel in rels:
        word, pos, deprel, headindex = rel.rsplit("/", maxsplit=3)
        headindex = int(headindex)
        thewords.append((word,pos,deprel,headindex))

    for word, pos, deprel, headindex in thewords:
        ## if headindex is 0, we didn't find a new dependency. otherwise we did.
        if headindex != 0:
            headword = thewords[headindex - 1][0]
            print("{0}\t{1}\t{2}\t{3}".format(headword, word, deprel, count))
