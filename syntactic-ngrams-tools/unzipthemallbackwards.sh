#!/bin/bash

for num in `seq -w 98 -1 60`; do
  gzip -d "arcs.$num-of-99.gz"
done
