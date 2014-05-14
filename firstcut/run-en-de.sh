python3 firstcut.py \
  --source en \
  --target de \
  --infn ../testdata/en-de.test.tokenised.xml \
  --outfn ./theoutput-en-de.xml \
  --lm /space/german-wikipedia/german.blm \
  --pt /space/phrasetables-db/en-de.db \
  --weights mert-en-de/weights.ZMERT.final \
