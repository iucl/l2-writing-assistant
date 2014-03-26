#!/usr/bin/env python

"""
So far, just using scores from a phrase table and a language model. But let's
add more stuff!
"""

import argparse
import math
import sys

import kenlm

import libsemeval2014task5.format as format
import phrasetable
import babelnet
from phrasetable import PTEntry

def best_translation(candidates, weights, leftcontext, rightcontext, lm):
    ## XXX: if we don't have a phrase table entry, look for the individual
    ## components of the fragment?
    if not candidates:
        return PTEntry(source="OOV",target="OOV",pdirect=1,pinverse=1)
    lowpenalty = float("inf")
    best = None
    for ptentry in candidates:
        sent = (leftcontext + " " + ptentry.source + " " + rightcontext).lower()
        lm_penalty = -lm.score(sent)
        pt_penalty = -math.log(ptentry.pdirect, 10)
        penalty = 0
        penalty += (weights["LM"] * lm_penalty)
        penalty += (weights["PT"] * pt_penalty)
        if penalty < lowpenalty:
            lowpenalty = penalty
            best = ptentry
    assert best
    return best

def get_argparser():
    """Build the argument parser for main."""
    parser = argparse.ArgumentParser(description='firstcut')
    parser.add_argument('--infn', type=str, required=True)
    parser.add_argument('--outfn', type=str, required=True)
    parser.add_argument('--lm', type=str, required=True)
    parser.add_argument('--source', type=str, required=True)
    parser.add_argument('--target', type=str, required=True)
    parser.add_argument('--weights', type=str, required=True)
    return parser

def generate_candidates(phrase, args):
    assert isinstance(phrase, tuple)
    phrase_s = " ".join(phrase)

    pt_filename = "phrase-table-{0}-{1}.gz".format(args.source, args.target)
    ptentries = phrasetable.lookup_phrase(phrase_s, pt_filename)

    if not ptentries:
        key = phrase_s.replace(' ', '_')
        frombabelnet = babelnet.babelnet_translations(key, args.target)
        ptentries = []
        for (term, score) in frombabelnet:
            entry = PTEntry(source=phrase_s,target=term,pdirect=score,pinverse=score)
            ptentries.append(entry)

    return ptentries

def load_weights(weightsfn):
    out = {}
    for line in open(weightsfn):
        line = line.strip()
        name,weight = line.split()
        name = name.strip()
        weight = float(weight.strip())
        out[name] = weight
    return out

def main():
    parser = get_argparser()
    args = parser.parse_args()
    inputfilename = args.infn
    outputfilename = args.outfn
    weightsfn = args.weights

    weights = load_weights(weightsfn)

    reader = format.Reader(inputfilename)
    writer = format.Writer(outputfilename, reader.L1, reader.L2)

    lm = kenlm.LanguageModel(args.lm)

    for sentencepair in reader:
        inputfragments = list(sentencepair.inputfragments())
        assert len(inputfragments) == 1
        leftcontext, fragment, rightcontext = inputfragments[0]
        assert isinstance(fragment, format.Fragment)

        candidates = generate_candidates(fragment.value, args)

        best = best_translation(candidates, weights, leftcontext, rightcontext, lm)
        ## XXX(alexr): this is all going to flip if/when we use a phrase table
        ## that goes in the other direction.
        translatedvalue = best.source.split()

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
