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
import os
import sys

from collections import defaultdict

import kenlm

import libsemeval2014task5.format as format
import phrasetable
import babelnet
from phrasetable import PTEntry
from util import dprint
from util import allsplits

import parser_interface
import query_cache
import pmi 

def score_candidates(candidates, weights, leftcontext, rightcontext, lm):
    """Return (score,candidate,scores) tuples, where score is the weighted
    total and scores are the individual unweighted scores.."""
    out = []
    for ptentry,listofwords in candidates:
        score = 0
        sent = " ".join(listofwords)
        lm_penalty = lm.score(sent)
        pt_direct = math.log(ptentry.pdirect, 10)
        pt_inverse = math.log(ptentry.pinverse, 10)
        scores = (lm_penalty, pt_direct, pt_inverse)

        score += (weights["LM"] * lm_penalty)
        score += (weights["DIRECT"] * pt_direct)
        score += (weights["INVERSE"] * pt_inverse)
        out.append((score, ptentry, scores))
    return out

def nonzero(num):
    """Because smoothing is for wimps."""
    return max(num, 1e-15)

def rescore_candidates(candidates, weights, leftcontext, rightcontext, sentid, args):
    pmi_cls = pmi.PMI(args.target)
    parsefn = "{0}-{1}-{2}-devel".format(args.source, args.target, sentid)
    parsecache = parser_interface.PARPATH + parsefn + ".conll"
    parser = parser_interface.Pcandidates(args.target, parsecache)
    newcandidates = []

    allsentences = []
    for (score, ptentry, scores) in candidates:
        sentence = []
        sentence.extend(leftcontext.split())
        sentence.extend(ptentry.target.split())
        sentence.extend(rightcontext.split())
        allsentences.append(sentence)

    ## XXX: make the caching work.
    if os.path.exists(parsecache):
        parser.load_new_parse(parsecache, allsentences)
    else:
        parser.do_new_parse(allsentences, sentid) 

    for (score, ptentry, scores) in candidates:
        sentence = []
        sentence.extend(leftcontext.split())
        sentence.extend(ptentry.target.split())
        sentence.extend(rightcontext.split())

        lex,pos = parser.find_rels(sentence, ptentry.target.split())
        score_lex = nonzero(pmi_cls.sim_lex(lex))
        score_pos = nonzero(pmi_cls.sim_pos(pos))

        logprob_lex = math.log(score_lex, 10)
        logprob_pos = math.log(score_pos, 10)

        dprint("PTENTRY, LEX AND POS:", ptentry.target, score_lex, score_pos)

        score += (weights["PMI_LEX"] * logprob_lex)
        score += (weights["PMI_POS"] * logprob_pos)
        scores = scores + (logprob_lex, logprob_pos)
        newcandidates.append((score, ptentry, scores))
    pmi_cls.dump_cache()

    return newcandidates


def generate_split_candidates(phrase, sl, tl):
    ptentries = []

    splits = list(reversed(allsplits(list(phrase))))
    dprint(splits)

    for split in splits:
        split_strings = [" ".join(entry) for entry in split]

        found = []
        for entry in split_strings:
            foundsomething = False
            from_pt = phrasetable.lookup(entry)
            if from_pt:
                foundsomething = True
                found.append(from_pt)
            elif " " not in entry:
                frombabelnet = babelnet_candidates(entry, sl, tl)
                if frombabelnet:
                    foundsomething = True
                    found.append(frombabelnet)
            if not foundsomething:
                found.append([])

        if all(found):
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

                ## XXX: magic number, or maybe "tunable hyperparameter".
                if len(ptentries) == 10000:
                    return ptentries
    return ptentries

@functools.lru_cache(maxsize=10000)
def babelnet_candidates(phrase_s, sl, tl):
    """Return list of PTEntry objects for the phrase."""
    ptentries = []
    key = phrase_s.replace(' ', '_')
    frombabelnet = babelnet.babelnet_translations(key, sl, tl)
    ptentries = []
    total = sum(score for (term,score) in frombabelnet)
    for (term, score) in frombabelnet:
        term = term.replace('_', ' ')
        entry = PTEntry(source=phrase_s,
                        target=term,
                        pdirect=score/total,
                        pinverse=score/total)
        ptentries.append(entry)
    return ptentries

def generate_candidates(phrase, args, oov_lookup):
    """Given a phrase and the cmdline args, return a list of appropriate
    PTEntrys"""
    assert isinstance(phrase, tuple)

    phrase_s = " ".join(phrase)
    ptentries = phrasetable.lookup(phrase_s)

    if not ptentries:
        if len(phrase) > 1:
            ptentries = generate_split_candidates(phrase,
                                                  args.source,
                                                  args.target)

    ## XXX: this seems completely correct.
    if not ptentries:
        frombabelnet = babelnet_candidates(phrase_s, args.source, args.target)
        ptentries.extend(frombabelnet)

    if not ptentries:
        nospaces = "".join(phrase)
        if nospaces in oov_lookup:
            looked_up = oov_lookup[nospaces]
            oov = PTEntry(source=phrase_s,target=looked_up,pdirect=1,pinverse=1)
            ptentries.append(oov)
        else:
            oov = PTEntry(source=phrase_s,target="OOV",pdirect=1,pinverse=1)
            ptentries.append(oov)

    return ptentries

def read_sentencepairs(reader):
    """Load up all the sentencepair objects and put them in a dictionary."""
    out = {}
    for sentencepair in reader:
        out[int(sentencepair.id)] = sentencepair
    return out

def sentences_and_candidates(sentencepairs, args, oov_lookup):
    """Generate a dictionary mapping from sentid to
     a list of (cand,candsentence) pairs
    ... where cand is a PTEntry and candsentence is the complete sentence as a
    list of words.
    """
    out = defaultdict(list)
    for sentid in sentencepairs:
        sentencepair = sentencepairs[sentid]
        inputfragments = list(sentencepair.inputfragments())
        assert len(inputfragments) == 1
        leftcontext, fragment, rightcontext = inputfragments[0]
        assert isinstance(fragment, format.Fragment)

        candidates = generate_candidates(fragment.value, args, oov_lookup)
        for cand in candidates:
            translatedvalue = cand.target.split()
            translatedfragment = format.Fragment(tuple(translatedvalue),
                                                 fragment.id)
            sentencepair.output = \
                sentencepair.replacefragment(fragment, translatedfragment,
                                             sentencepair.input)
            completesentence = []
            for item in sentencepair.output:
                if type(item) is str:
                    completesentence.append(item)
                elif type(item) is format.Fragment:
                    completesentence.extend(item.value)
                else:
                    assert False, "this should never happen"
            out[int(sentencepair.id)].append((cand, completesentence))
    return out

def load_weights(weightsfn):
    out = {}
    for line in open(weightsfn):
        line = line.strip()
        name,weight = line.split()
        name = name.strip()
        weight = float(weight.strip())
        out[name] = weight
    return out

def load_oovs(sl, tl):
    here = os.path.dirname(os.path.abspath(__file__))
    fn = here + "/{0}-{1}.tsv".format(sl,tl)
    out = {}
    with open(fn) as infile:
        for line in infile:
            line = line.strip()
            src, trg = line.split("\t")
            srcwords = src.split()
            src = "".join(srcwords)
            out[src] = trg
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
    parser.add_argument('--oof', type=bool, default=False, required=False)
    return parser

def main():
    argparser = get_argparser()
    args = argparser.parse_args()
    inputfilename = args.infn
    outputfilename = args.outfn
    weightsfn = args.weights
    targetlang = args.target

    zmert = args.zmert ## if true, output in zmert output format

    ## load weights for our different features
    weights = load_weights(weightsfn)
    dprint(weights)

    ## load things not in the phrase table.
    oov_lookup = load_oovs(args.source, args.target)

    reader = format.Reader(inputfilename)
    writer = format.Writer(outputfilename, reader.L1, reader.L2)

    lm = kenlm.LanguageModel(args.lm)
    phrasetable.set_phrase_table(args.pt)

    ## dictionary from sentid to [(cand,candsentence) ...]
    sentencepairs = read_sentencepairs(reader)
    sent_cand_pairs = sentences_and_candidates(sentencepairs, args, oov_lookup)

    sentids = sorted(list(sent_cand_pairs.keys()))

    for sentid in sentids:
        sentencepair = sentencepairs[sentid]
        ## now we have a list of (ptentry, list_of_words)
        candidates = sent_cand_pairs[sentid]

        inputfragments = list(sentencepair.inputfragments())
        assert len(inputfragments) == 1
        leftcontext, fragment, rightcontext = inputfragments[0]
        assert isinstance(fragment, format.Fragment)

        scored = score_candidates(candidates,
                                  weights,
                                  leftcontext,
                                  rightcontext,
                                  lm)
        scored.sort(reverse=True)

        tophundred = scored[:100]
        scored = rescore_candidates(tophundred, weights, leftcontext,
                                    rightcontext, sentid, args)

        if zmert:
            ## TODO: pull this out into a function
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
            print(scored[0])
            translatedvalue = scored[0][1].target.split()
            translatedfragment = format.Fragment(tuple(translatedvalue), fragment.id)

            if args.oof:
                for cand in scored[1:5]:
                    alt = format.Alternative(tuple(cand[1].target.split()))
                    translatedfragment.alternatives.append(alt)

            sentencepair.output = sentencepair.replacefragment(fragment,
                                                               translatedfragment,
                                                               sentencepair.input)

            writer.write(sentencepair)
            print("Input: " + sentencepair.inputstr(True,"blue"))
            print("Output: " + sentencepair.outputstr(True,"yellow"))

    writer.close()
    reader.close()

if __name__ == "__main__": main()
