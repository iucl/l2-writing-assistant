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
##load
def load_en():
    en = pickle.load(open(PICPATH + "en.cache","rb"))
    return en

def load_de():
    de = pickle.load(open(PICPATH + "de.cache","rb"))
    print("CHECK LOADING in load_de!! size:", len(de))
    return de

def load_es():
    es = pickle.load(open(PICPATH + "es.cache","rb"))
    return es

##dump
def dump_en(pic):
    pickle.dump(pic,open(PICPATH + "en.cache","wb"))

def dump_es(pic):
    pickle.dump(pic,open(PICPATH + "es.cache","wb"))

def dump_de(pic):
    print("CHECK DUMPING in dump_de!! size:", len(pic))
    pickle.dump(pic,open(PICPATH + "de.cache","wb"))


##Now this is loading the chaches.
def find_head_dep_deprel( handle,head, dep, deprel):
    """Return the number of times we've seen this head,dep,deprel triple."""
    try: 
        count = handle[("<head-dep-deprel>",head,dep,deprel)]
    except:
        count = "empty"
    return count

def find_head_dep( handle, head, dep):
    try:
        count = handle[("<head-dep>",head,dep)]
    except:
        count = "empty"
    return count


def find_head_deprel(handle, head, deprel):
    try:
        count = handle[("<head-deprel>",head,deprel)]
    except:
        count = "empty"
    return count

def find_dep_deprel( handle, dep, deprel):
    try:
        count = handle[("<dep-deprel>",dep,deprel)]
    except:
        count = "empty"
    return count

def find_head( handle, head):
    try:
        count = handle[("<head>",head)]
    except:
        count = "empty"
    return count

def find_dep( handle, dep):
    try:
        count = handle[("<dep>",dep)]
    except:
        count = "empty"
    return count

    
def main():
    conn = sqlite3.connect("en-pos.db")
    output = get_count_head_dep_deprel(conn, "NN", "JJ", "tmod")
    print(output)
    output = get_count_head_dep_deprel(conn, "FNORD", "QQQQQZM", "tmod")
    print(output)

#if __name__ == "__main__": main()
