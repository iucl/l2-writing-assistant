#!/usr/bin/env python3

import sys

DPRINT=False
def dprint(*a,**aa):
    if DPRINT:
        print(file=sys.stderr, *a, **aa)

def allsplits(ls):
    """Given a list, return all of the ways to split that list into sublists.
    For example, given [1,2,3] should return in some order:
    [[1,2,3]]
    [[1],[2,3]]
    [[1,2],3]
    [[1],[2],[3]]. This is 2^(n-1) elements for an n-item list."""

    if not ls: return []
    if len(ls) == 1: return [[ls]]

    ## only two possibilities. We split off the first one, or we don't.
    rest = allsplits(ls[1:])
    splitfirst = []
    for way in rest:
        newway = [[ls[0]]] + way
        splitfirst.append(newway)

    dontsplitfirst = []
    for way in rest:
        newway = [[ls[0]] + way[0]] + way[1:]
        dontsplitfirst.append(newway)
    return splitfirst + dontsplitfirst

def printsplits(ways):
    for way in ways:
        print("/".join(" ".join(str(item) for item in part) for part in way))

def main():
    one = allsplits("one".split())
    two = allsplits("one two".split())
    three = allsplits("one two three".split())
    four = allsplits("one two three four".split())
    printsplits(one)
    printsplits(two)
    printsplits(three)
    printsplits(four)
    printsplits(allsplits("a quiet evening at home".split()))

if __name__ == "__main__": main()
