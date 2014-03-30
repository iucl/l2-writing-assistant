#!/usr/bin/env python3
import pickle
PICPATH = "../cache/"

def cache_head_dep_deprel( handle,count, head, dep, deprel):
    """Return the number of times we've seen this head,dep,deprel triple."""
    newstuff = {("<head-dep-deprel>",head,dep,deprel):count}
    handle.update(newstuff)

def cache_head_dep( handle, count, head, dep):
    newstuff = {("<head-dep>",head,dep):count}
    handle.update(newstuff)


def cache_head_deprel(handle,count, head, deprel):
    newstuff = {("<head-deprel>",head,deprel):count}
    handle.update(newstuff)

def cache_dep_deprel( handle,count, dep, deprel):
    newstuff = {("<dep-deprel>",dep,deprel):count}
    handle.update(newstuff)

def cache_head( handle, count, head):
    newstuff = {("<head>",head):count}
    handle.update(newstuff)

def cache_dep( handle, count, dep):
    newstuff = {("<dep>",dep):count}
    handle.update(newstuff)

##Loading and dumping for English, Spanish, and German

##laod

##dump

##Now this is loading the chaches.
def find_head_dep_deprel( handle,head, dep, deprel):
    """Return the number of times we've seen this head,dep,deprel triple."""
    try: 
        count = handle[("<head-dep-deprel>",head,dep,deprel)]
    except:
        count = 0
    return count

def find_head_dep( handle, head, dep):
    try:
	count = handle[("<head-dep>",head,dep)]
    except:
        count = 0
    return count


def find_head_deprel(handle, head, deprel):
    try:
        count = handle[("<head-deprel>",head,deprel)]
    except:
        count = 0
    return count

def find_dep_deprel( handle, dep, deprel):
    try:
        count = handle[("<dep-deprel>",dep,deprel)]
    except:
        count = 0
    return count

def find_head( handle, head):
    try:
        count = handle[("<head>",head)]
    except:
        count = 0
    return count

def find_dep( handle, dep):
    try:
        count = handle[("<dep>",dep)]
    except:
        count = 0
    return count

    
def main():
    conn = sqlite3.connect("en-pos.db")
    output = get_count_head_dep_deprel(conn, "NN", "JJ", "tmod")
    print(output)
    output = get_count_head_dep_deprel(conn, "FNORD", "QQQQQZM", "tmod")
    print(output)

if __name__ == "__main__": main()
