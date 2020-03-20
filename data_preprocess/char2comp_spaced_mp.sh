#!/bin/bash

export STORAGE_BUCKET=gs://sbt0

### multi-processing version
NUM_PROC=70
for i in `seq 1 $((NUM_PROC))`; do
  python3 data_preprocess/char2comp_spaced_mp.py ${STORAGE_BUCKET}/data/corpus/splited/zhwiki-latest-pages-articles_${i}.txt ${STORAGE_BUCKET}/data/corpus/subchar_spaced_lower/zhwiki-latest-pages-articles_${i}_subchar_spaced_lower.txt resources/ids_dict_char2comps_joined.json 1 \
    $@ &
done