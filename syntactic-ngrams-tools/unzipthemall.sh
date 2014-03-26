#!/bin/bash

for num in `seq -w 0 98`; do
  gzip -d "arcs.$num-of-99.gz"
done
