#!/bin/bash

### multi-processing version
NUM_PROC=11
for i in `seq 1 $((NUM_PROC))`; do
  python data_preprocess/char2comp_mp.py datasets/examples/corpus_zh_example_0_${i}.txt datasets/examples/corpus_zh_example_${i}_subchar_lower.txt resources/char2comp.json 1 \
    $@ &
done