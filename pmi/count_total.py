import pickle
from collections import defaultdict

def count_total(lang,dict_name):
    ## Just count the total number of <POS,Label> (also with a certain role)
    counts = defaultdict(lambda: 0)

    huge = pickle.load(open(dict_name,"rb"))
    for key,value in huge.items():
         head,dep,label = key
         counts[(head,label,"head")] +=value
         counts[(dep,label,"dep")] +=value

    result = {key:value for key,value in counts.items()}
    pickle.dump(result,open(lang + ".all.pickle","wb"))

if __name__ == "__main__":

    count_total("de","de.pos.dep.pickle")

