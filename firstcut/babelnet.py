#!/usr/bin/env

from collections import defaultdict
import os
import subprocess
import sys

here = os.path.dirname(os.path.realpath(__file__))
BABELNETSCRIPT = here + "/../babelnet-api-2.0/run-print-translations.sh"

def babelnet_translations(lemma, lang):
    text = ""
    output = subprocess.check_output([BABELNETSCRIPT, lemma])
    text = output.decode('utf-8')

    out = []
    for line in text.split("\n"):
        splitted = line.strip().split("\t")
        mylang = splitted[0].lower()
        if mylang != lang: continue
        scoreds = splitted[1:]
        for scored in scoreds:
            term,score = scored.split(":")
            score = float(score)
            out.append((term, score))
    return out

def main():
    lemma = sys.argv[1]
    lang = sys.argv[2]
    translations = babelnet_translations(lemma, lang)
    print(translations)

if __name__ == "__main__": main()
