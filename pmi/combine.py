## This files tries to combine small pickles into large ones.
## Possibly using a hierachy.

import pickle
import sys

PATH = "/N/dc2/scratch/leviking/shared/smallpickles/"
def pickle2txt(name):
    pp = pickle.load(open(PATH + name,"rb"))
    OUT = open(name + ".txt","w")
    for key,value in pp.items():
        
        string = "{}###{}###{}:::{}\n".format(key[0],key[1],key[2],value)
        OUT.write(string)

    OUT.close()
    print("writing {} is done!", name)



name = sys.argv[1]
pickle2txt(name) 
