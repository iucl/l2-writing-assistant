#!/usr/bin/env

from collections import defaultdict
import os
import subprocess
import sys

here = os.path.dirname(os.path.realpath(__file__))
BABELNETSCRIPT = here + "/../babelnet-api-2.0/run-print-translations.sh"

def babelnet_translations(lemma, sl, tl):
    text = ""
    output = subprocess.check_output([BABELNETSCRIPT, sl, lemma])
    text = output.decode('utf-8')

    out = []
    for line in text.split("\n"):
        splitted = line.strip().split("\t")
        mylang = splitted[0].lower()
        if mylang != tl: continue
        scoreds = splitted[1:]
        for scored in scoreds:
            term,score = scored.split(":")
            score = float(score)
            out.append((term, score))
    return out

def main():
    sl = sys.argv[1]
    tl = sys.argv[2]
    lemma = sys.argv[3]
    translations = babelnet_translations(lemma, sl, tl)
    print(translations)

if __name__ == "__main__": main()
