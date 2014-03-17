import pickle
from collections import defaultdict

##use python class. 
##So every language can be an instance of it. 

class PMI:

    def __init__(self,lang):
        ##the constructor
        self.pos_dep = pickle.load(open(lang+ ".pos.dep.pickle","rb"))
        self.pos_all = pickle.load(open(lang+ ".pos.all.pickle","rb"))

        ##these two are not ready yet.
        #wrd_dep = pickle.load(open(lang+ ".wrd.dep.pickle","rb"))
        #wrd_all = pickle.load(open(lang+ ".wrd.all.pickle","rb"))

        print("Pickles for {} has been loaded!".format(lang))

    def sim_wrd_ea(self):  ##similarity based on dependency of words
        pass

    def sim_pos_ea(self,head,dep,label):

        ##handle special cases, if some counts are zero, there will be lookup error
        ##Question:::  lowercases????

        try:
            num = self.pos_dep[(head,dep,label)]
        except:
            num = 0
        try:
            demon1 = self.pos_all[(head,label,"head")]
        except:
            demon1 = 0
        try:
            demon2 = self.pos_all(dep,label,"dep")
        except:
            demon2 = 0
        if (demon1 + demon2) == 0: return 0
        else: return num/ (demon1 + demon2)

    def sim_pos(self,deplist,lang):  ## the input is a list of dependencies.
        ##should look up each label, and then average the result.
        length = 0  ##if there is a root for English, then ignore it. 
        sim_sum = 0
        for triple in deplist:
            head,dep,label = triple
            if lang == "en" and label == "root":  ### XXX Question, what should this be??
                continue
            else:
                sim_sum += sim_pos_ea(head,dep,label)
                length +=1

        return sim_sum/length










