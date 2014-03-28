#!/usr/bin/env python

##2014/03/19. LK: This script takes a parsed file (Spanish in CoNLL09 format, but this could easily be adjusted) and produces a list of all dependencies (tokens); there is a list for words, and a list for POS tags. A later script will iterate through the list of tokens and produce a list of types and counts. So this script will write to a text file, where each line is simply:
##headword<TAB>dependentword<TAB>label<TAB>count
##And the other file will be:
##headPOS<TAB>dependentPOS<TAB>label<TAB>count
##Note that because we are not adding anything in this script, all counts will be "1"!
##usage:
##this uses sys to get the filename as a command line argument, so it can be run on a batch of files like so:
##for pf in $(ls *.parsed) ; do python get_dep_list.py $pf ; done

import codecs, sys, re
#

filename = sys.argv[1]
fileprefix = filename.split(".")[0] ##filenames are "something.parsed", so we just want "something"
input = codecs.open(filename, "r", encoding="utf-8", errors="surrogateescape")
wholetext = input.read()
input.close()

def split_sents(wt): ##wt for "whole text"; should be the entire conll file read in as a single string.
	sents = wt.split('\n\n')
	return sents ##sents should be a list of sentences (which are conll dependency trees)

def get_deps(ds): ##ds should be a single conll dependency tree for one sentence (it's a string)
	ds = ds.strip()
	dslist = ds.split('\n')
	dsdict = {}
	for line in dslist:
		dstuff = line.split()
		dkey = dstuff[0] ##the word index
		dval = [dstuff[1].strip(), dstuff[5].strip(), dstuff[9].strip(), dstuff[11].strip()] ##depword, depPOS, headindex, deplabel
		dsdict[dkey] = dval ##e.g., {'1': ('When', 'ADV', '4', 'TMP'), '2': ('the', 'DT', '3', 'NMOD'), ...}
	for k in dsdict:
		ddep = dsdict[k][0] ##depword
		ddeppos = dsdict[k][1]
		dheadkey = dsdict[k][2]
		dlabel = dsdict[k][3]
		if dheadkey == '0':
			dhead = '0' ##we give it a '0' because we can't look up the head of the root (bc there is no word at index '0')
			dheadpos = '0' ##likewise, the root has no POS, so let's call it '0'
		else:
			dhead = dsdict[dheadkey][0] ##headword
			dheadpos = dsdict[dheadkey][1]
		lextrip = ''.join([dhead, '\t', ddep, '\t', dlabel, '\t1\n']) ##headword<TAB>dependentword<TAB>label<TAB>count		
		postrip = ''.join([dheadpos, '\t', ddeppos, '\t', dlabel, '\t1\n'])
		lexout.write(lextrip)
		posout.write(postrip)

##main program
sentlist = split_sents(wholetext)
with codecs.open(''.join([fileprefix, '.posdeplist']), 'a', encoding='utf-8') as posout, codecs.open(''.join([fileprefix, '.lexdeplist']), 'a', encoding='utf-8') as lexout:
	for s in sentlist:
		get_deps(s)
