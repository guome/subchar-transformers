#!/bin/bash

export STORAGE_BUCKET=gs://sbt0

### multi-processing version
NUM_PROC=218
for i in `seq 1 $((NUM_PROC))`; do
  python3 data_preprocess/char2comp_no_space_mp.py ${STORAGE_BUCKET}/data/corpus/splited/zhwiki-latest-pages-articles_${i}.txt ${STORAGE_BUCKET}/data/corpus/subchar_no_space_lower/zhwiki-latest-pages-articles_${i}_subchar_no_space_lower.txt resources/ids_dict_char2comps_joined.json 1 \
    $@ &
done