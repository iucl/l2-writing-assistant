import parser_interface
from parser_interface import *
import query_cache
from query_cache import *
import pmi 
from pmi import *

print("testing the English parsing commands")
en_parse = Pcandidates("en")
en_parse.do_new_parse(["Obviously Malaysian Airline is lying .".split(),\
"Obviously Malaysian Airline ice cream .".split(),\
"The picturesque old houses by the harbor have been pulled down , and a hideous luxury hotel has been built there instead .".split(),\
"The picturesque ancient keeps by the harbor have been pulled down , and a hideous luxury hotel has been built there instead .".split(),\
"The picturesque refrigerate diode by the harbor have been pulled down , and a hideous luxury hotel has been built there instead .".split(),\
"They do not have any evidence, the world will not give up the investigation .".split(" ")])



#print "testing the English parsing commands"
#en_parse = Pcandidates("en")
#en_parse.do_new_parse(['L .'.split(" "), \
#		'La estrella de Oklahoma City puede batir una marca del maco Michael Jordan .'.split(" ")])

lex,pos = en_parse.find_rels("The picturesque old houses by the harbor have been pulled down , and a hideous luxury hotel has been built there instead .".split(),"old houses".split(" "))
lex1,pos1 = en_parse.find_rels("The picturesque ancient keeps by the harbor have been pulled down , and a hideous luxury hotel has been built there instead .".split(),"ancient keeps".split(" "))
lex2,pos2 = en_parse.find_rels("The picturesque refrigerate diode by the harbor have been pulled down , and a hideous luxury hotel has been built there instead .".split(), "refrigerate diode".split() )
#lex,pos = es_parse.find_rels('Das Wort "Arger" wird mit einem groben A geschrieben .'.split(" "#, "wird mit einem".split(" "))

#lex,pos = es_parse.find_rels("La estrella de Oklahoma City puede batir una marca del maco Michael Jordan .".split(" "), "La estrella".split(" "))

print(lex)
print(pos)
#print lex
#print pos


pmi_cls = PMI("en")
##Do this for each sentence in the training/testing data:
##suppose the candidate is "amo"

##**********************Alex, this is the additional line of code. that your program needs to call
##**********************To save the pickle
score =   pmi_cls.sim_lex(lex)
#score1 = pmi_cls.sim_lex(lex1)
#score2 = pmi_cls.sim_lex(lex2)
print("\t***PMI for this candidate is",score)
#print("\t***PMI for this candidate is", score1)
#print("\t***PMI for this candidate is ",score2)

pmi_cls.dump_cache()
##Intialize PMI, and PMI calles the database file.

