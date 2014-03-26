#!/bin/bash

for num in `seq -w 0 98`; do
  wget "http://commondatastorage.googleapis.com/books/syntactic-ngrams/eng/arcs.$num-of-99.gz"
done
