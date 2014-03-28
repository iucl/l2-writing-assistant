import parser_interface
from parser_interface import *

import pmi 
from pmi import *
##Do this once for each language
en_parse = Pcandidates("en")
#en_parse.do_new_parse(["Obviously Malaysian Airline is lying .".split(" "), "They do not have any evidence, the world will not give up the investigation .".split(" ")])

#lex,pos = en_parse.find_rels("Obviously Malaysian Airline is lying .".split(),"is lying".split(" "))
#print lex
#print pos

pmi_cls = PMI("en")
##Do this for each sentence in the training/testing data:
##suppose the candidate is "amo"

#lexTrip,posTrip = es_parse.find_rels(["me","amo","Juana"],["amo"])  ##this is a string
##Intialize PMI, and PMI calles the database file.

#pmi_lex = ...
#pmi_lex_bk =
#pmi_pos = ...
#pmi_pos_bk = ...
