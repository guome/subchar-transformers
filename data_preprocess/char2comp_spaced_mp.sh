#!/bin/bash

export STORAGE_BUCKET=gs://sbt0

### multi-processing version
NUM_PROC=110
for i in `seq 1 $((NUM_PROC))`; do
  python3 data_preprocess/char2comp_mp.py ${STORAGE_BUCKET}/data/corpus/splited/zhwiki-latest-pages-articles_${i}.txt ${STORAGE_BUCKET}/data/corpus/subchar_lower/zhwiki-latest-pages-articles_${i}_subchar_lower.txt resources/char2comp.json 1 \
    $@ &
done