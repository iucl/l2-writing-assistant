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

def read_pic():
    names = []
    IN = open("de_small","r")
    lines = IN.readlines()
    for line in lines:
        eles = line.strip().split(" ")
        names += eles

    print names
    pickle.dump(names,open("de_small.pickle","wb"))

read_pic()
#name = sys.argv[1]
#pickle2txt(name) 
