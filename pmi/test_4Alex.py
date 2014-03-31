import parser_interface
from parser_interface import *
import query_cache
from query_cache import *
import pmi 
from pmi import *

print("testing the English parsing commands")

### *********  step 1 *******
##  new a class for a language
en_parse = Pcandidates("en")

### ********  step 2 *******
## parse the candidate sentences. The input should be a LIST of sentences,
## each sentence is a LIST of WORDS.
en_parse.do_new_parse(["Obviously Malaysian Airline is lying .".split(),\
"Obviously Malaysian Airline ice cream .".split(),\
"The picturesque old houses by the harbor have been pulled down , and a hideous luxury hotel has been built there instead .".split(),\
"The picturesque ancient keeps by the harbor have been pulled down , and a hideous luxury hotel has been built there instead .".split(),\
"The picturesque refrigerate diode by the harbor have been pulled down , and a hideous luxury hotel has been built there instead .".split(),\
"They do not have any evidence, the world will not give up the investigation .".split(" ")])


### ****** step 3 ******
##  find the dependency triples for a candidate, given the context
## input1:  a sentence. as a LIST of WORDS
## input2:  a candiate, as a LIST of WORDS (evne there;s just one word!)
lex,pos = en_parse.find_rels("The picturesque old houses by the harbor have been pulled down , and a hideous luxury hotel has been built there instead .".split(),"there instead".split(" "))

### **** step 4 ******
##new a PMI class for this language.
pmi_cls = PMI("en")
## get the lexical score.
score =   pmi_cls.sim_lex(lex)
print("\t***PMI for this candidate is",score)

### **** step 5 ******   IMPORTANT!!! saves the cache!!!
##  saves the query results during the lifetime of the class instance of PMI
pmi_cls.dump_cache()
##Intialize PMI, and PMI calles the database file.

