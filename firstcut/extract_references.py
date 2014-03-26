#!/usr/bin/env python

"""
Print all the reference sentences to stdout in the format ZMERT expects.
"""

import sys
import libsemeval2014task5.format as format

reader = format.Reader(sys.argv[1])
for sentencepair in reader:
    strings = [" ".join(item.value) if type(item) is format.Fragment
                                    else item
               for item in sentencepair.ref]
    text = " ".join(strings)
    print(text)
