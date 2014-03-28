import pickle
from collections import defaultdict

import dependency_queries as dbtool ##this is the code from Alex.

DBPATH = "../dependency-dbs/"
##use python class. 
##So every language can be an instance of it. 
import sqlite3 as sql

class PMI:

    def __init__(self,lang):
        ##the constructor
        #self.pos_dep = pickle.load(open(lang+ ".pos.dep.pickle","rb"))
        #self.pos_all = pickle.load(open(lang+ ".pos.all.pickle","rb"))

        ##Now we are not using pickles, we use the database prepared by Alex.
        self.lang = lang
        self.posdb = sql.connect(DBPATH + "{0}-pos.db".format(lang))
        #self.lexdb = sqlite3.connect(DBPATH + "{0}-lex.db".format(lang))

        print("Database for {} has been loaded!".format(lang))

    def sim_lex_ea(self,head,dep,label):  ##similarity based on dependency of words
        ##handle special cases, if some counts are zero, there will be lookup error
        ##Question:::  lowercases????

        ##This is not the Backup version. 
        numerator = dbtool.get_count_head_dep_deprel(self.lexdb, head, dep, label)
        demon1 = dbtool.get_count_head_deprel(self.lexdb, head, label)
        demon2 = dbtool.get_count_dep_deprel(self.lexdb, dep, label)

        if (demon1 + demon2) ==0:
            return 0
        else:
            return 1.0* numerator/ (demon1 + demon2) 

    def sim_lex_bk(self,head,dep,label):  ##similarity based on dependency of words
        ##handle special cases, if some counts are zero, there will be lookup error
        ##Question:::  lowercases????

        ##This is not the Backup version.
        numerator = dbtool.get_count_head_dep(self.lexdb, head, dep, label)
        demon1 = dbtool.get_count_head(self.lexdb, head, label)
        demon2 = dbtool.get_count_dep(self.lexdb, dep, label)

        if (demon1 + demon2) ==0:
            return 0
        else:
            return 1.0* numerator/ (demon1 + demon2)



    def sim_pos_ea(self,head,dep,label):  ##similarity based on dependency of words
        ##handle special cases, if some counts are zero, there will be lookup error
        ##Question:::  lowercases????

        ##This is not the Backup version.
        numerator = dbtool.get_count_head_dep_deprel(self.posdb, head, dep, label)
        demon1 = dbtool.get_count_head_deprel(self.posdb, head, label)
        demon2 = dbtool.get_count_dep_deprel(self.posdb, dep, label)

        print(demon1,demon2, "####")

        if (demon1 + demon2) ==0:
            return 0
        else:
            return 1.0* numerator/ (demon1 + demon2)

    def sim_pos_ea_bk(self,head,dep,label):  ##similarity based on dependency of words
        ##handle special cases, if some counts are zero, there will be lookup error
        ##Question:::  lowercases????

        ##This is not the Backup version.
        numerator = dbtool.get_count_head_dep(self.posdb, head, dep, label)
        demon1 = dbtool.get_count_head(self.posdb, head, label)
        demon2 = dbtool.get_count_dep(self.posdb, dep, label)

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







