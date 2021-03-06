python3 firstcut.py \
  --source fr \
  --target en \
  --infn ../testdata/fr-en.test.tokenised.xml \
  --outfn ./theoutput-fr-en.xml \
  --lm /space/english-wikipedia_old/english.blm \
  --pt /space/phrasetables-db/fr-en.db \
  --weights mert-fr-en/weights.ZMERT.final \
