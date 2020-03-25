#!/bin/bash

export STORAGE_BUCKET=gs://sbt0

### multi-processing version
NUM_PROC=218
for i in `seq 71 $((NUM_PROC))`; do
  python3 data_preprocess/char2char_segmented_mp.py ${STORAGE_BUCKET}/data/corpus/splited/zhwiki-latest-pages-articles_${i}.txt ${STORAGE_BUCKET}/data/corpus/char_segmented_lower/zhwiki-latest-pages-articles_${i}_char_segmented_lower.txt 1 \
    $@ &
done