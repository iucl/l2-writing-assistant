#!/usr/bin/env python3

"""
Take a phrase table file and produce a db.
"""

import argparse
import gzip
import sqlite3

PHRASETABLE = """\
create table if not exists Phrases (
    source    text not null,
    target    text not null,
    pdirect   float not null,
    pinverse  float not null
)"""

ADDINDEX = """\
CREATE INDEX IF NOT EXISTS contents_on_Counts_idx ON Phrases(source)
"""

def get_argparser():
    """Build the argument parser for main."""
    parser = argparse.ArgumentParser(description='firstcut')
    parser.add_argument('--infn', type=str, required=True)
    parser.add_argument('--db', type=str, required=True)
    return parser

def save_ptentries(ptfn, conn):
    """Given the filename of the phrase table and a connection, store all the
    counts."""
    c = conn.cursor()
    with gzip.open(ptfn) as infile:
        for line in infile:
            line = line.decode('utf-8')
            parts = line.split("|||", maxsplit=3)
            source, target, scores, etc = [s.strip() for s in parts]
            scoreparts = scores.split()
            pinverse,weighti,pdirect,weightd = [float(s) for s in scoreparts]

            sql = """insert into Phrases(source,target,pdirect,pinverse)
                     values(?,?,?,?)"""
            param = (source,target,pdirect,pinverse)
            c.execute(sql, param)
    conn.commit()

def main():
    parser = get_argparser()
    args = parser.parse_args()
    dbfilename = args.db
    infn = args.infn
    THEDB = args.db

    conn = sqlite3.connect(THEDB)
    c = conn.cursor()
    c.execute(PHRASETABLE)
    c.execute(ADDINDEX)
    conn.commit()

    save_ptentries(infn, conn)
    c.close()

if __name__ == "__main__": main()
