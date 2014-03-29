#!/usr/bin/env python

"""
So far, just using scores from a phrase table and a language model. But let's
add more stuff!
"""

import argparse
import functools
import itertools
import math
import operator
import sys

import kenlm

import libsemeval2014task5.format as format
import phrasetable
import babelnet
from phrasetable import PTEntry
from util import dprint
from util import allsplits

def score_candidates(candidates, weights, leftcontext, rightcontext, lm):
    """Return (score,candidate,scores) tuples, where score is the weighted
    total and scores are the individual unweighted scores.."""
    out = []
    for ptentry in candidates:
        score = 0
        sent = (leftcontext + " " + ptentry.target + " " + rightcontext).lower()
        lm_penalty = lm.score(sent)
        pt_direct = math.log(ptentry.pdirect, 10)
        pt_inverse = math.log(ptentry.pinverse, 10)

        scores = (lm_penalty, pt_direct, pt_inverse)

        score += (weights["LM"] * lm_penalty)
        score += (weights["DIRECT"] * pt_direct)
        score += (weights["INVERSE"] * pt_inverse)
        out.append((score, ptentry, scores))
    return out

def generate_split_candidates(phrase):
    ptentries = []

    splits = list(reversed(allsplits(list(phrase))))
    dprint(splits)

    for split in splits:
        split_strings = [" ".join(entry) for entry in split]
        if all(phrasetable.lookup(entry) for entry in split_strings):
            found = [phrasetable.lookup(entry) for entry in split_strings]

            for assignment in itertools.product(*found):
                target = " ".join(pte.target for pte in assignment)
                pdirects = [pte.pdirect for pte in assignment]
                pinverses = [pte.pinverse for pte in assignment]

                product_pdirect = functools.reduce(operator.mul, pdirects, 1)
                product_pinverse = functools.reduce(operator.mul, pinverses, 1)

                entry = PTEntry(source=" ".join(phrase),
                                target=target,
                                pdirect=product_pdirect,
                                pinverse=product_pinverse)
                ptentries.append(entry)
    ## XXX: this can generate way too many possibilities; consider filtering at
    ## this point.
    return ptentries

def generate_candidates(phrase, args):
    """Given a phrase and the cmdline args, """
    assert isinstance(phrase, tuple)

    phrase_s = " ".join(phrase)
    ptentries = phrasetable.lookup(phrase_s)

    if not ptentries:
        if len(phrase) > 1:
            ptentries = generate_split_candidates(phrase)

    ## XXX: consider folding this into generate_split_candidates too.
    ## XXX: this seems wrong.
    ##if not ptentries:
    ##    key = phrase_s.replace(' ', '_')
    ##    frombabelnet = babelnet.babelnet_translations(key, args.target)
    ##    ptentries = []
    ##    for (term, score) in frombabelnet:
    ##        entry = PTEntry(source=phrase_s,target=term,pdirect=score,pinverse=score)
    ##        ptentries.append(entry)

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
    parser.add_argument('--pt', type=str, required=True)
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
    dprint(weights)

    reader = format.Reader(inputfilename)
    writer = format.Writer(outputfilename, reader.L1, reader.L2)

    lm = kenlm.LanguageModel(args.lm)
    phrasetable.set_phrase_table(args.pt)

    for sentencepair in reader:
        inputfragments = list(sentencepair.inputfragments())
        assert len(inputfragments) == 1
        leftcontext, fragment, rightcontext = inputfragments[0]
        assert isinstance(fragment, format.Fragment)

        candidates = generate_candidates(fragment.value, args)

        scored = score_candidates(candidates, weights, leftcontext, rightcontext, lm)
        scored.sort(reverse=True)

        translatedvalue = scored[0][1].target.split()
        translatedfragment = format.Fragment(tuple(translatedvalue), fragment.id)
        sentencepair.output = sentencepair.replacefragment(fragment,
                                                           translatedfragment,
                                                           sentencepair.input)

        if zmert:
            ### output the n-best translations in ZMERT format
            for cand in scored[:10]:
                translatedvalue = cand[1].target.split()
                translatedfragment = format.Fragment(tuple(translatedvalue),
                                                     fragment.id)
                sentencepair.output = \
                    sentencepair.replacefragment(fragment, translatedfragment,
                                                 sentencepair.input)
                strings = [" ".join(item.value) if type(item) is format.Fragment
                                                else item
                           for item in sentencepair.output]
                text = " ".join(strings)
                scores = " ".join([str(score) for score in cand[2]])
                out = "{0} ||| {1} ||| {2}".format(int(sentencepair.id) - 1,
                                                   text,
                                                   scores)
                print(out)
        else:
            writer.write(sentencepair)
            print("Input: " + sentencepair.inputstr(True,"blue"))
            print("Output: " + sentencepair.outputstr(True,"yellow"))

    writer.close()
    reader.close()

if __name__ == "__main__": main()
