import pickle
import query_cache
from query_cache import * 
from collections import defaultdict

import dependency_queries as dbtool ##this is the code from Alex.

DBPATH = "/space/dependency-dbs/"
##use python class. 
##So every language can be an instance of it. 
import sqlite3 as sql
import commands
from commands import *

###Now, before we do any query, find the cache first. If 
### the return is 0, query the database, and update the cache.
class PMI:

    def __init__(self,lang):
        ##the constructor
        #self.pos_dep = pickle.load(open(lang+ ".pos.dep.pickle","rb"))
        #self.pos_all = pickle.load(open(lang+ ".pos.all.pickle","rb"))

        ##Now we are not using pickles, we use the database prepared by Alex.
        self.lang = lang
        exec("self.cache = load_{0}()".format(lang))  ##just load the cached pickle for this language.
        #print(self.cache, "RRRRRR")
        if EN_MODE != "wiki":
            wikipath = ""
        else:
            wikipath = "english-wikipedia"
        self.posdb = sql.connect(DBPATH + wikipath +  "{0}-pos.db".format(lang))
        self.lexdb = sql.connect(DBPATH + wikipath + "{0}-lex.db".format(lang))
        #print("Database for {} has been loaded!".format(lang))
   
    def dump_cache(self):
        eval("dump_{0}({1})".format(self.lang,self.cache))

    def sim_lex_ea(self,head,dep,label):  ##similarity based on dependency of words
        
        num_c = find_head_dep_deprel(self.cache,head,dep,label)
        if num_c =="empty":
            numerator = dbtool.get_count_head_dep_deprel(self.lexdb, head, dep, label)
            cache_head_dep_deprel(self.cache,numerator,head,dep,label)
        else:
            numerator = num_c

        demon1_c = find_head_deprel(self.cache,head,label)
        if demon1_c == "empty":
            demon1 = dbtool.get_count_head_deprel(self.lexdb, head, label)
            cache_head_deprel(self.cache,demon1,head,label)
        else:
            demon1 = demon1_c            

        demon2_c = find_dep_deprel(self.cache,dep,label)
        if demon2_c == "empty":
            demon2 = dbtool.get_count_dep_deprel(self.lexdb, dep, label)
            cache_dep_deprel(self.cache,demon2,dep,label)
        else:
            demon2 = demon2_c

        if (demon1 + demon2) ==0:
            return 0
        else:
            return 1.0* numerator/ (demon1 + demon2) 

    def sim_lex_bk(self,head,dep):  ##similarity based on dependency of words
        ##handle special cases, if some counts are zero, there will be lookup error
        ##Question:::  lowercases????

        ##This is not the Backup version.
        num_c = find_head_dep(self.cache,head,dep)
        if num_c =="empty":
            numerator = dbtool.get_count_head_dep(self.lexdb, head, dep)
            cache_head_dep(self.cache,numerator,head,dep)
        else:
            numerator = num_c

        demon1_c = find_head(self.cache,head)
        if demon1_c == "empty":
            demon1 = dbtool.get_count_head(self.lexdb, head)
            cache_head(self.cache,demon1,head)
        else:
            demon1 = demon1_c

        demon2_c = find_dep(self.cache,dep)
        if demon2_c == "empty":
            demon2 = dbtool.get_count_dep(self.lexdb, dep)
            cache_dep(self.cache,demon2,dep)
        else:
            demon2 = demon2_c

        if (demon1 + demon2) ==0:
            return 0
        else:
            return 1.0* numerator/ (demon1 + demon2)

    def sim_pos_ea(self,head,dep,label):  ##similarity based on dependency of words
        num_c = find_head_dep_deprel(self.cache,head,dep,label)
        if num_c =="empty":
            numerator = dbtool.get_count_head_dep_deprel(self.posdb, head, dep, label)
            cache_head_dep_deprel(self.cache,numerator,head,dep,label)
        else:
            numerator = num_c

        demon1_c = find_head_deprel(self.cache,head,label)
        if demon1_c == "empty":
            demon1 = dbtool.get_count_head_deprel(self.posdb, head, label)
            cache_head_deprel(self.cache,demon1,head,label)
        else:
            demon1 = demon1_c

        demon2_c = find_dep_deprel(self.cache,dep,label)
        if demon2_c == "empty":
            demon2 = dbtool.get_count_dep_deprel(self.posdb, dep, label)
            cache_dep_deprel(self.cache,demon2,dep,label)
        else:
            demon2 = demon2_c

        if (demon1 + demon2) ==0:
            return 0
        else:
            return 1.0* numerator/ (demon1 + demon2)



    def sim_pos_ea_bk(self,head,dep,label):  ##similarity based on dependency of words
        num_c = find_head_dep(self.cache,head,dep)
        if num_c =="empty":
            numerator = dbtool.get_count_head_dep(self.posdb, head, dep)
            cache_head_dep(self.cache,numerator,head,dep)
        else:
            numerator = num_c

        demon1_c = find_head(self.cache,head)
        if demon1_c == "empty":
            demon1 = dbtool.get_count_head(self.posdb, head)
            cache_head(self.cache,demon1,head)
        else:
            demon1 = demon1_c

        demon2_c = find_dep(self.cache,dep)
        if demon2_c == "empty":
            demon2 = dbtool.get_count_dep(self.posdb, dep)
            cache_dep(self.cache,demon2,dep)
        else:
            demon2 = demon2_c

        if (demon1 + demon2) ==0:
            return 0
        else:
            return 1.0* numerator/ (demon1 + demon2)


    def sim_pos(self,triples):  ## the input is a list of dependencies.
        ##should look up each label, and then average the result.
        ##if there is a root for English, then ignore it. 
        assert len(triples) > 0
        sim_sum = 0
        for triple in triples:

            head,dep,label = triple
            sim_sum += self.sim_pos_ea(head,dep,label)

        return sim_sum*1.0/len(triples)

    def sim_lex(self,triples):
        assert len(triples) > 0
        sim_sum = 0
        for triple in triples:

            head,dep,label = triple
            sim_sum += self.sim_lex_ea(head,dep,label)

        return sim_sum*1.0/len(triples)


    def sim_pos_bk(self,triples):  ## the input is a list of dependencies.
        ##should look up each label, and then average the result.
        ##if there is a root for English, then ignore it.
        assert len(triples) > 0
        sim_sum = 0
        for triple in triples:

            head,dep,label = triple
            sim_sum += self.sim_pos_ea_bk(head,dep,label)

        return sim_sum*1.0/len(triples)

    def sim_lex_bk(self,triples):
        assert len(triples) > 0
        sim_sum = 0
        for triple in triples:

            head,dep,label = triple
            sim_sum += self.sim_lex_ea_bk(head,dep,label)

        return sim_sum*1.0/len(triples)



