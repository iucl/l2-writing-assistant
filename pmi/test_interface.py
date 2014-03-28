import parser_interface
from parser_interface import *

import pmi 
from pmi import *


#en_parse = Pcandidates("en")
#en_parse.do_new_parse(["Obviously Malaysian Airline is lying .".split(" "), "They do not have any evidence, the world will not give up the investigation .".split(" ")])

"""
print "testing the German parsing commands"
es_parse = Pcandidates("es")
es_parse.do_new_parse(['La estrella de Oklahoma City puede batir una marca del maco Michael Jordan .'.split(" "), \
		'La estrella de Oklahoma City puede batir una marca del maco Michael Jordan .'.split(" ")])

#lex,pos = en_parse.find_rels("Obviously Malaysian Airline is lying .".split(),"is lying".split(" "))

#lex,pos = es_parse.find_rels('Das Wort "Arger" wird mit einem groben A geschrieben .'.split(" ")\
#, "wird mit einem".split(" "))

lex,pos = es_parse.find_rels("La estrella de Oklahoma City puede batir una marca del maco Michael Jordan .".split(" "), "La estrella".split(" "))

print lex
print pos
#print lex
#print pos

"""


pmi_cls = PMI("en")
##Do this for each sentence in the training/testing data:
##suppose the candidate is "amo"

#lexTrip,posTrip = es_parse.find_rels(["me","amo","Juana"],["amo"])  ##this is a string
##Intialize PMI, and PMI calles the database file.

