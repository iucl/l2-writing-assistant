"""
Simplest possible interface for pulling things out of a Moses-formatted phrase
table.
"""

import gzip
import sys
from collections import namedtuple
from collections import defaultdict

PHRASETABLE = defaultdict(list)

def get_lines_source(fn, phrase):
    return get_lines(fn, phrase, True)

def get_lines_target(fn, phrase):
    return get_lines(fn, phrase, False)

def get_lines(fn, phrase, phrase_is_source):
    """For the specified phrase, pull out all the lines where that phrase is in
    the appropriate spot."""
    out = []
    if phrase_is_source:
        test = lambda line: line.startswith(phrase + " |||")
    else:
        test = lambda line: ((" ||| " + phrase + " ||| ") in line)
    with gzip.open(fn) as infile:
        for line in infile:
            line = line.decode('utf-8')
            if test(line):
                out.append(line)
    return out

## http://www.statmt.org/moses/?n=FactoredTraining.ScorePhrases
## Currently, four different phrase translation scores are computed:
##     inverse phrase translation probability φ(f|e)
##     inverse lexical weighting lex(f|e)
##     direct phrase translation probability φ(e|f)
##     direct lexical weighting lex(e|f)

PTEntry = namedtuple("PTEntry", "source target pdirect pinverse".split())

def lines_to_ptentries(lines):
    """Take a list of lines from the phrase table file; return a list with a
    PTEntry for each line."""
    out = []
    for line in lines:
        parts = line.split("|||", maxsplit=3)
        source, target, scores, etc = [s.strip() for s in parts]
        scoreparts = scores.split()
        pinverse, weighti, pdirect, weightd = [float(s) for s in scoreparts]
        out.append(PTEntry(source,target,pdirect,pinverse))
    return out

def lookup_phrase(phrase, pt_fn):
    """Look up the phrase in the phrase table in the named file. Return a list
    of PTEntries."""
    lines = get_lines_target(pt_fn, phrase)
    ptentries = lines_to_ptentries(lines)
    return ptentries

def lookup(phrase):
    return PHRASETABLE[phrase]

def set_phrase_table(ptfn):
    with gzip.open(ptfn) as infile:
        for line in infile:
            line = line.decode('utf-8')
            parts = line.split("|||", maxsplit=3)
            source, target, scores, etc = [s.strip() for s in parts]
            scoreparts = scores.split()
            pinverse,weighti,pdirect,weightd = [float(s) for s in scoreparts]
            entry = PTEntry(source,target,pdirect,pinverse)

            ## XXX: will need to be reversed
            PHRASETABLE[target].append(entry)

def main():
    ptentries = lookup_phrase(sys.argv[1], sys.argv[2])
    for ptentry in ptentries:
        print(ptentry)

if __name__ == "__main__": main()
