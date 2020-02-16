#!/bin/bash

### multi-processing version
NUM_PROC=11
for i in `seq 1 $((NUM_PROC))`; do
  python data_preprocess/char2comp_mp.py corpus/zhwiki_articles_${i}.txt corpus/subchar_lower/zhwiki_articles_${i}_subchar_lower.txt resources/char2comp.json 1 \
    $@ &
done