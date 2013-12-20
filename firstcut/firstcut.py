#!/usr/bin/env python

#####################################################################
# SemEval 2014 task 5 - L2 Writing Assistant
#       Example system in Python
#
#
# This example system takes two arguments, the trial/test set and the file to
# output to.
#
# Instead of translating the fragments from L2 to L1. This example
# simply converts the fragments to uppercase.
#
#####################################################################

import sys
import argparse

#Here we import the format library for this task:
import libsemeval2014task5.format as format
import phrasetable
from phrasetable import PTEntry

def get_argparser():
    """Build the argument parser for main."""
    parser = argparse.ArgumentParser(description='firstcut')
    parser.add_argument('--infn', type=str, required=True)
    parser.add_argument('--outfn', type=str, required=True)
    return parser


def best_translation(phrase):
    assert isinstance(phrase, tuple)
    phrase_s = " ".join(phrase)
    ptentries = phrasetable.lookup_phrase(phrase_s, "phrase-table.gz")
    ## XXX: if we don't have a phrase table entry, look for the individual
    ## components of the fragment?
    if not ptentries:
        return PTEntry(source=phrase_s,target=phrase_s,pdirect=1,pinverse=1)
    return max(ptentries, key=lambda e: e.pdirect)

def main():
    parser = get_argparser()
    args = parser.parse_args()
    inputfilename = args.infn
    outputfilename = args.outfn

    reader = format.Reader(inputfilename)
    writer = format.Writer(outputfilename, reader.L1, reader.L2)

    for sentencepair in reader:
        inputfragments = list(sentencepair.inputfragments())
        assert len(inputfragments) == 1
        leftcontext, fragment, rightcontent = inputfragments[0]
        assert isinstance(fragment, format.Fragment)

        best = best_translation(fragment.value)
        ## XXX(alexr): this is all going to flip if/when we use a phrase table
        ## that goes in the other direction.
        translatedvalue = best.source.split()
        # translatedvalue = [x.upper() for x in fragment.value]

        # create a new fragment for the new value, it must carry the same ID
        translatedfragment = format.Fragment(tuple(translatedvalue),
                                             fragment.id)

        #Now we can set the system output by copying the input sentence
        #(the context after all will stay the same, we only change the fragment)
        #And then replacing the old fragment with the translated one.
        sentencepair.output = sentencepair.replacefragment(fragment,
                                                           translatedfragment,
                                                           sentencepair.input)
        writer.write(sentencepair)

        print("Input: " + sentencepair.inputstr(True,"blue"))
        print("Output: " + sentencepair.outputstr(True,"yellow"))

    writer.close()
    reader.close()

if __name__ == "__main__": main()
