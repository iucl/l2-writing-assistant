
import commands
from commands import *
import codecs, sys, re
import os
PARPATH = "../parseout/"##parser path
###!!!! The input has be a list of words
####   the input has to contain all the commas, periods..
#EN_MODE = "wiki"
    
class Pcandidates:  ##this class parses all the candidate sentences for a language
    def __init__(self, lang, fn):
        """ To initialize, input is the language """
        self.lang = lang
        self.outputname = fn
        ##self.fn = fn
        self.parse_lookup = {}
        
    def read_sents(self,filename): ##wt for "whole text"; should be the entire conll file read in as a single string.
        """ This just reads in the parsed sentences, and return a list of sentences """
        IN = codecs.open(PARPATH + filename, "r", encoding="utf-8", errors="surrogateescape")
        wholetext = IN.read()

        #print wholetext, "\n\n######"
        #raw_input()
        IN.close()
        sents = wholetext.split("\n\n")
        #for line in
        sents = [x for x in sents if x.strip() != ""]
        return sents ##sents should be a list of sentences (which are conll dependency trees)

    def do_new_parse(self,sent_list):  ##takes in a list of sentences we want to parse. Each sentence is represented by a list of words. 
        """ Calling this function will parse all the sentences. It should make the training of CONNL format first
        call the parser from command, and remember the filename"""
        ##make training format
        sentS_list = [" ".join(x) + "\n" for x in sent_list]##A list of sentence strings.
        filename = self.outputname##self.lang+"candi"

        OUT = codecs.open(PARPATH + filename, 'w', encoding='utf-8')
        #OUT = open(PARPATH + filename,"w")
        OUT.writelines(sentS_list)
        OUT.close()
        
        ##parse it
        if self.lang == "en":
            if EN_MODE == "google":
                cmd = en_cmd_google.format(PARPATH + filename,PARPATH,PARPATH + filename,PARPATH,PARPATH + filename )
            else:
                cmd = en_cmd_wiki.format(PARPATH + filename,PARPATH,PARPATH + filename,PARPATH,PARPATH + filename )

        if self.lang == "de":
            cmd = de_cmd.format(PARPATH + filename,PARPATH + filename,\
 	PARPATH + filename,PARPATH + filename, \
	PARPATH + filename,PARPATH + filename,\
	PARPATH + filename,PARPATH + filename)

        if self.lang == "es":
            cmd = es_cmd.format(PARPATH + filename,PARPATH + filename,\
        PARPATH + filename,PARPATH + filename, \
        PARPATH + filename,PARPATH + filename,\
        PARPATH + filename,PARPATH + filename)

        os.system(cmd)
        ##Now read the parse and make it into a dictionary
        parsed_sents = self.read_sents(filename + ".conll")

        #print "\n\n",len(parsed_sents), len(sent_list)
        assert len(parsed_sents) == len(sent_list)  ##the number of sentences have to match!!
        for i in range(len(sent_list)):
            sent_key = " ".join(sent_list[i])
            #print "key*****",sent_key
            self.parse_lookup[sent_key.strip()] = parsed_sents[i]
        
        ##fixed, take in the outname
        ##self.outputname = filename

        #print self.parse_lookup.keys(), "keys******\n\n"

    def load_new_parse(self, filename, sent_list): ##if we already parsed them and knew the filename.
        self.outputname = filename
        self.parse_lookup = {"foo":1}

        ##Now read the parse and make it into a dictionary
        parsed_sents = self.read_sents(filename)
        assert len(parsed_sents) == len(sent_list)  ##the number of sentences have to match!!
        for i in range(len(sent_list)):
            sent_key = " ".join(sent_list[i])
            self.parse_lookup[sent_key.strip()] = parsed_sents[i]
        
        self.outputname = filename

    def locate_parse(self,sent_rep): ##Locate the parse for a particular sentence. Input is a list of words. [w1,w2,w3...]
        #print sent_rep
        string = " ".join(sent_rep)
        result = self.parse_lookup[string.strip()]

        return result

    def find_rels(self,sent_rep,candidates):
        parse_sent = self.locate_parse(sent_rep)
        cls_sent = Psentence(parse_sent,self.lang)  ##input should be the already parsed sentence.
        indices = cls_sent.word_indices(sent_rep,candidates)
        
        posTrip = cls_sent.find_rel_pos(cls_sent.posTrip,indices)
        lexTrip = cls_sent.find_rel_pos(cls_sent.lexTrip,indices)

        return lexTrip,posTrip

"""
Usage :::
##Do this once for each language
es_parse = Pcandidates("es")
es_parse.do_new_parse(sent_list)


##Do this for each sentence in the training/testing data:

##suppose the candidate is "amo"
lexTrip,posTrip = es_parse.find_rels(["me","amo","Juana"],["amo"])  ##this is a string

##Intialize PMI, and PMI calles the database file. 

pmi_lex = ...
pmi_lex_bk =
pmi_pos = ...
pmi_pos_bk = ...

"""
        


class Psentence:  ##the class for a parsed sentence.

    def __init__(self,parse_sent,lang):
        """ Initialize a new sentence by using a list of words. The class is responsible for finding the parsed sentence in the file """
        self.lang = lang
        self.clsTrip = []
        self.lexTrip = []
        ##call this function with the parsed sentence
        if lang == "en":
            self.get_dep_en(parse_sent)
        else:
            self.get_dep_notEn(parse_sent)

    def word_indices(self,sent_s,words):
        """
        Input to this function is the sentence, represented as a list of words.
                and a list of words (that is the candidate)
        Output to this function is a list of indices for the candidate.
        """
        indices = []
        for i in range(len(sent_s)):
            if sent_s[i] in words:
                indices.append(i)
        return indices

    def find_rel_pos(self,sent_trip,word_indices):  ##give the sentence triple, and the indices of the word.
        """
        the word indices must start from 0  of the input. !!!
        """
        word_indices = [x+1 for x in word_indices]  ##convert the indices into CONNL one, start from 1.
        ##make a small dictionary of indices, faster to lookup.
        needed = {str(x):1 for x in word_indices}  ##to be consistent with the triples, these are strings.

        found_trip = [] ##the triples that are found. 
        ##Now go through the dependency triples we have and return a list of relavant ones.
        for triple in sent_trip:
            headindex,depindex,head,dep,label = triple
            if headindex in needed:
                found_trip.append((head,dep,label))
            if depindex in needed:
                if self.lang == "en" and headindex == "0":
                    pass
                else:  ##IF this word is the root of sentence, we would not have a label for it in English. But we would have one in
                        ## Spanish and German.
                    found_trip.append((head,dep,label))
        return list(set(found_trip))

    def find_rel_lex(self,sent_trip,word_indices):  ##give the sentence triple, and the indices of the word.
        """
        the word indices must start from 0  of the input. !!!
        """
        word_indices = [x+1 for x in word_indices]  ##convert the indices into CONNL one, start from 1.
        ##make a small dictionary of indices, faster to lookup.
        needed = {str(x):1 for x in word_indices}  ##to be consistent with the triples, these are strings.

        found_trip = [] ##the triples that are found. 
        ##Now go through the dependency triples we have and return a list of relavant ones.
        for triple in sent_trip:
            headindex,depindex,head,dep,label = triple
            if headindex in needed:
                found_trip.append((head,dep,label))
            if depindex in needed:
                if self.lang == "en" and headindex == "0":
                    pass
                else:  ##IF this word is the root of sentence, we would not have a label for it in English. But we would have one in
                        ## Spanish and German.
                    found_trip.append((head,dep,label))
        return list(set(found_trip))

    def get_dep_notEn(self,parsed_sent):
        """
        Given a sentence, return the dependency triples in that sentence 
        """
        sentence = parsed_sent ##the already parsed sentence. 
        ds = sentence.strip()

        dslist = ds.split('\n')
        dsdict = {}
        for line in dslist:
            dstuff = line.split()
            dkey = dstuff[0] ##the word index
            try:dval = [dstuff[1].strip(), dstuff[5].strip(), dstuff[9].strip(), dstuff[11].strip()] ##depword, depPOS, headindex, deplabel
            except: print (line)
            dsdict[dkey] = dval ##e.g., {'1': ('When', 'ADV', '4', 'TMP'), '2': ('the', 'DT', '3', 'NMOD'), ...}
        count =1
        lextriples = []
        postriples = []
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
            #lextrip = ''.join([dhead, '\t', ddep, '\t', dlabel, '\t1\n']) ##headword<TAB>dependentword<TAB>label<TAB>count		
            #postrip = ''.join([dheadpos, '\t', ddeppos, '\t', dlabel, '\t1\n'])

            lextrip = (dheadkey,k,dhead,ddep,dlabel)
            postrip = (dheadkey,k,dheadpos,ddeppos,dlabel)

            lextriples.append(lextrip)
            postriples.append(postrip)

            self.lexTrip  =lextriples
            self.posTrip = postriples

   
    def get_dep_en(self,parsed_sent):
        """
        Given a sentence, return the dependency triples in that sentence 
        """
        sentence = parsed_sent ##the already parsed sentence. 
        ds = sentence.strip()

        dslist = ds.split('\n')
        dsdict = {}
        for line in dslist:
            dstuff = line.split()
            dkey = dstuff[0] ##the word index
            try:dval = [dstuff[1].strip(), dstuff[3].strip(), dstuff[6].strip(), dstuff[7].strip()] ##depword, depPOS, headindex, deplabel
            except: print (line)
            dsdict[dkey] = dval ##e.g., {'1': ('When', 'ADV', '4', 'TMP'), '2': ('the', 'DT', '3', 'NMOD'), ...}
        count =1
        lextriples = []
        postriples = []
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
            #lextrip = ''.join([dhead, '\t', ddep, '\t', dlabel, '\t1\n']) ##headword<TAB>dependentword<TAB>label<TAB>count		
            #postrip = ''.join([dheadpos, '\t', ddeppos, '\t', dlabel, '\t1\n'])

            lextrip = (dheadkey,k,dhead,ddep,dlabel)
            postrip = (dheadkey,k,dheadpos,ddeppos,dlabel)

            lextriples.append(lextrip)
            postriples.append(postrip)

            self.lexTrip  =lextriples
            self.posTrip = postriples

testsent = """
1	The	_	DT	DT	_	2	det	_	_
2	game	_	NN	NN	_	5	nsubj	_	_
3	has	_	VBZ	VBZ	_	5	aux	_	_
4	never	_	RB	RB	_	5	neg	_	_
5	seen	_	VBN	VBN	_	0	root	_	_
6	any	_	DT	DT	_	9	det	_	_
7	official	_	JJ	JJ	_	9	amod	_	_
8	English	_	JJ	JJ	_	9	amod	_	_
9	release	_	NN	NN	_	5	dobj	_	_
10	.	_	.	.	_	5	punct	_	_
"""

#pp = Psentence(testsent,"en")
#rr = pp.find_rel_lex(pp.lexTrip,[0,1,4])
#print rr
