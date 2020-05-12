#!/bin/bash

export STORAGE_BUCKET=gs://sbt0

pip3 install jieba

### multi-processing version
NUM_PROC=218
for i in `seq 1 $((NUM_PROC))`; do
  python3 src/data_proc/zh_wiki_proc_mp.py ${STORAGE_BUCKET}/data/corpus/splited/zhwiki-latest-pages-articles_${i}.txt ${STORAGE_BUCKET}/data/corpus/char_no_space_lower_simplified/zhwiki-latest-pages-articles_${i}_char_no_space_lower_simplified.txt 1 \
    $@ &
done