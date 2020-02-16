#!/bin/bash

### multi-processing version
NUM_PROC=22
for i in `seq 1 $((NUM_PROC))`; do
  python3 ALBERT/create_pretraining_data.py --input_file=./corpus/subchar_lower/zhwiki-latest-pages-articles_${i}_subchar_lower.txt --output_file=./ALBERT/experiments/subchar_lower_vocab_5000/zhwiki_train_examples_${i}.tfrecord --spm_model_file=./resources/tokenizer/5000-clean.model --do_lower_case=True --do_whole_word_mask=True --max_seq_length=256 --max_predictions_per_seq=26 --masked_lm_prob=0.15 --dupe_factor=5 \
    $@ &
done