#!/usr/bin/env python3

"""
Take a "collapsed" dependency count file and produce a db.
"""

import argparse
import sqlite3

COUNTS = """\
create table if not exists Counts (
    head     text not null,
    dep      text not null,
    deprel   text not null,
    count    integer not null
)"""

ADDINDEX = """\
CREATE INDEX IF NOT EXISTS contents_on_Counts_idx ON Counts(head,dep,deprel)
"""

def get_argparser():
    """Build the argument parser for main."""
    parser = argparse.ArgumentParser(description='firstcut')
    parser.add_argument('--infn', type=str, required=True)
    parser.add_argument('--db', type=str, required=True)
    return parser

def save_counts(countfn, conn):
    """Given the filename of the counts and a connection, store all the
    counts."""
    c = conn.cursor()
    with open(countfn) as infile:
        for line in infile:
            try:
                head, dep, deprel, count = line.split("\t")
            except:
                print("BUSTED LINE:", line)
                continue
            count = int(count)
            sql = "insert into Counts(head,dep,deprel,count) values(?,?,?,?)"
            param = (head, dep, deprel, count)
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
    c.execute(COUNTS)
    c.execute(ADDINDEX)
    conn.commit()

    save_counts(infn, conn)
    c.close()

if __name__ == "__main__": main()
