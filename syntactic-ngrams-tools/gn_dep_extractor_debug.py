#!/usr/bin/env python

###2014/03/13. LK: This script (modified from "dep_extractor.py") takes a file from my "clean_google/" folder (these files derived from the Google ngrams "arcs" dataset; see note "*A" below to see the form of the clean_google files) and produces two pickled dictionaries, of this form:
##1: pospickle = {(headPOS1, depPOS1, label1): count, (headPOS2, depPOS2, label2): count, ...}
##2: lexpickle = {(head1, dep1, label1): count, (head2, dep2, label2): count, ...}
##
##usage (you'll probably run this something like this): for gn in $(ls *.txt) ; do python gn_dep_extractor.py $gn ; done



import cPickle as pickle ##python2
import sys

def get_deps(curr_line): 
	lextrips = []
	postrips = []
	curr_line = curr_line.strip()
	curr_words = curr_line.split()
	curr_count = int(curr_words.pop()) #now curr_words = e.g. ['jimmy/NNP/nsubj/2', 'eating/VBG/ROOT/0'] or ['market/NN/dobj/0', 'for/IN/prep/1 as/RB/mwe/4', 'well/RB/cc/2 as/IN/mwe/4', 'for/IN/conj/2'] (most will have two words, but there may be more); curr_count = '43';
	curr_wdict = {} #current word dict
	indexer = 1
	for winfostring in curr_words:
		curr_wdict[str(indexer)] = winfostring.split('/') ##{indexer: [word, pos, deplabel, headindex], ...}
		indexer +=1
	for key in curr_wdict: ##key is indexer
		if curr_wdict[key][3] == '0':
			pass
		else:
			print "line: ", curr_line
			print "headwd: ", curr_wdict[curr_wdict[key][3]][0]
			print "depwd: ", curr_wdict[key][0]
			print "deplabel: ", curr_wdict[key][2]
			print "headpos: ", curr_wdict[curr_wdict[key][3]][1]
			print "deppos: ", curr_wdict[key][1]
			lextrip = (curr_wdict[curr_wdict[key][3]][0], curr_wdict[key][0], curr_wdict[key][2]) ##(headword, depword, deplabel) ##this line seems to be causing problems...
			postrip = (curr_wdict[curr_wdict[key][3]][1], curr_wdict[key][1], curr_wdict[key][2]) ##(headpos, deppos, deplabel)
			if lextrip in ltrip_tallies:
				ltrip_tallies[lextrip]+=curr_count
			else:
				ltrip_tallies[lextrip]=curr_count
			if postrip in ptrip_tallies:
				ptrip_tallies[postrip]+=curr_count
			else:
				ptrip_tallies[postrip]=curr_count

ltrip_tallies = {}
ptrip_tallies = {}
filename = sys.argv[1]
fileprefix = filename.split(".")[0]
input = open(filename, "r")
alllines = input.readlines()
input.close()
for line in alllines:
	get_deps(line)

lexpicklename = ''.join(["../lexpickles/", fileprefix, ".lexpickle"])
pospicklename = ''.join(["../pospickles/", fileprefix, ".pospickle"])

lexpickle = open(lexpicklename, "wb")
pickle.dump(ltrip_tallies, lexpickle)
lexpickle.close()
pospickle = open(pospicklename, "wb")
pickle.dump(ptrip_tallies, pospickle)
pospickle.close()
