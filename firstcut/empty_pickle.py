#!/usr/bin/env python3

import pickle
import sys

out = {}
with open(sys.argv[1], "wb") as outfile:
    pickle.dump(out, outfile)
