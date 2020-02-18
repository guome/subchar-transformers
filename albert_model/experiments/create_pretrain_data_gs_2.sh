#!/bin/bash

### multi-processing version

export STORAGE_BUCKET=gs://sbt0

NUM_PROC=20
for i in `seq 13 $((NUM_PROC))`; do
  python3 albert_model/create_pretraining_data.py --input_file=./corpus/subchar_lower/zhwiki-latest-pages-articles_${i}_subchar_lower.txt --output_file=${STORAGE_BUCKET}/subchar_lower_vocab_5000/zhwiki_train_examples_${i}_%s.tfrecord --vocab_file=./resources/tokenizer/5000-clean.vocab --spm_model_file=./resources/tokenizer/5000-clean.model --do_lower_case=True --do_whole_word_mask=True --max_seq_length=512 --max_predictions_per_seq=52 --masked_lm_prob=0.15 --dupe_factor=5
done