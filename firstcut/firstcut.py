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

def score_candidates(candidates, weights, leftcontext, rightcontext, lm):
    """Return (penalty,candidate) tuples."""
    out = []
    for ptentry in candidates:
        penalty = 0
        print("SOURCE", ptentry.source)
        print("TARGET", ptentry.target)
        ## XXX: source/target is going to flip with the new phrase tables
        sent = (leftcontext + " " + ptentry.source + " " + rightcontext).lower()
        lm_penalty = -lm.score(sent)
        pt_direct = -math.log(ptentry.pdirect, 10)
        pt_inverse = -math.log(ptentry.pinverse, 10)
        print("LM penalty", lm_penalty)
        print("DIRECT penalty", pt_direct)
        print("INVERSE penalty", pt_inverse)
        penalty += (weights["LM"] * lm_penalty)
        penalty += (weights["DIRECT"] * pt_direct)
        penalty += (weights["INVERSE"] * pt_inverse)
        out.append((penalty, ptentry))
    return out

def generate_candidates(phrase, args):
    ## XXX: if we don't have a phrase table entry, look for the individual
    ## components of the fragment?
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

    if not ptentries:
        oov = PTEntry(source="OOV",target="OOV",pdirect=1,pinverse=1)
        ptentries.append(oov)

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

def get_argparser():
    """Build the argument parser for main."""
    parser = argparse.ArgumentParser(description='firstcut')
    parser.add_argument('--infn', type=str, required=True)
    parser.add_argument('--outfn', type=str, required=True)
    parser.add_argument('--lm', type=str, required=True)
    parser.add_argument('--source', type=str, required=True)
    parser.add_argument('--target', type=str, required=True)
    parser.add_argument('--weights', type=str, required=True)
    parser.add_argument('--zmert', type=bool, default=False, required=False)
    return parser

def main():
    parser = get_argparser()
    args = parser.parse_args()
    inputfilename = args.infn
    outputfilename = args.outfn
    weightsfn = args.weights

    zmert = args.zmert ## if true, output in zmert output format

    ## load weights for our different features
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

        scored = score_candidates(candidates, weights, leftcontext, rightcontext, lm)
        scored.sort()
        print(scored)
        translatedvalue = scored[0][1].source.split() ## best.source.split()

        translatedfragment = format.Fragment(tuple(translatedvalue), fragment.id)
        sentencepair.output = sentencepair.replacefragment(fragment,
                                                           translatedfragment,
                                                           sentencepair.input)
        writer.write(sentencepair)
        print("Input: " + sentencepair.inputstr(True,"blue"))
        print("Output: " + sentencepair.outputstr(True,"yellow"))

    writer.close()
    reader.close()

if __name__ == "__main__": main()
