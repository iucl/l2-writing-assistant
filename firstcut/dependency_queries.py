#!/usr/bin/env python3

import sqlite3


# most specific version of PMI
## count specifying all three
## count for head,deprel
## count for dep,deprel

# backoff: similar but for pos tags. (same in the code)

# backoff: backoff by ignoring the deprel
## count specifying head,dep
## count for head
## count for dep

# super backoff: just pos, no deprel (also same in the code)

def get_count_head_dep_deprel(conn, head, dep, deprel):
    """Return the number of times we've seen this head,dep,deprel triple."""
    print("\t***Querying... 22",head,dep,deprel)

    c = conn.cursor()
    sql = ("""select count from Counts
           where head = ? and dep = ? and deprel = ?""")
    param = (head, dep, deprel)
    c.execute(sql, param)
    out = c.fetchone()

    print("###from the DB file", out)
    if out!=None and out[0] != None: 
        print("kkk")
        return out[0] 
    else: 
        print("ppp")
        return 0

def get_count_head_dep(conn, head, dep):
    """Return the number of times we've seen this head,dep tuple."""
    print("\t***Querying... 41",head,dep)

    c = conn.cursor()
    sql = "select sum(count) from Counts where head = ? and dep = ?"
    param = (head, dep)
    c.execute(sql, param)
    out = c.fetchone()
    if out!=None and  out[0] != None:
        return out[0]
    else:
        return 0


def get_count_head_deprel(conn, head, deprel):
    """Return the number of times we've seen this head,deprel tuple."""
    print("\t***Querying... 56",head,deprel)
    c = conn.cursor()
    sql = "select sum(count) from Counts where head = ? and deprel = ?"
    param = (head, deprel)
    c.execute(sql, param)
    out = c.fetchone()
    if out!=None and out[0] != None:
        print(out,out[0], "58")
        return out[0]
    else:
        print("EEEE1")
        return 0


def get_count_dep_deprel(conn, dep, deprel):
    """Return the number of times we've seen this dep,deprel tuple."""

    print("\t***Querying... 73",dep,deprel)
    c = conn.cursor()
    sql = ("select sum(count) from Counts where dep = ? and deprel = ?")
    param = (dep, deprel)
    c.execute(sql, param)
    out = c.fetchone()
    if out!=None and  out[0] != None:
        print(out,out[0],"73")
        return out[0]
    else:
        print("EEEE2")
        return 0


def get_count_head(conn, head):
    """Return the number of times we've seen this head, ignoring deprel."""
    print("\t***Querying... 89",head)

    c = conn.cursor()
    sql = ("select sum(count) from Counts where head = ?")
    param = (head,)
    c.execute(sql, param)
    out = c.fetchone()
    if out!=None and  out[0] != None:
        return out[0]
    else:
        return 0


def get_count_dep(conn, dep):
    """Return the number of times we've seen this dep, ignoring deprel."""
    print("\t***Querying... 104",dep)

    c = conn.cursor()
    sql = ("select sum(count) from Counts where dep = ?")
    param = (dep,)
    c.execute(sql, param)
    out = c.fetchone()
    if out!=None and  out[0] != None:
        return out[0]
    else:
        return 0

def main():
    conn = sqlite3.connect("en-pos.db")
    output = get_count_head_dep_deprel(conn, "NN", "JJ", "tmod")
    print(output)
    output = get_count_head_dep_deprel(conn, "FNORD", "QQQQQZM", "tmod")
    print(output)

if __name__ == "__main__": main()
