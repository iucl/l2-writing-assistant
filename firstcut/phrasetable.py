"""
No longer the simplest possible interface for pulling things out of a
Moses-formatted phrase table; now we're pulling PTEntry tuples from a sqlite
database!
"""

import gzip
import sys
import sqlite3
from collections import namedtuple

## http://www.statmt.org/moses/?n=FactoredTraining.ScorePhrases
## Currently, four different phrase translation scores are computed:
##     inverse phrase translation probability φ(f|e)
##     inverse lexical weighting lex(f|e)
##     direct phrase translation probability φ(e|f)
##     direct lexical weighting lex(e|f)

PTEntry = namedtuple("PTEntry", "source target pdirect pinverse".split())

CONN = None

def set_phrase_table(ptfn):
    global CONN
    CONN = sqlite3.connect(ptfn)

def lookup(phrase):
    c = CONN.cursor()
    sql = "select source,target,pdirect,pinverse from Phrases where source = ?"
    param = (phrase,)
    c.execute(sql, param)
    res = c.fetchall()
    out = []
    for (source,target,pdirect,pinverse) in res:
        entry = PTEntry(source,target,pdirect,pinverse)
        out.append(entry)
    return out
