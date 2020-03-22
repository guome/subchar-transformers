#!/bin/bash

### multi-processing version

export STORAGE_BUCKET=gs://sbt0

PREFIX=subchar_no_space_lower

# NUM_PROC=218
NUM_PROC=10

for i in `seq 10 $((NUM_PROC))`; do
  python3 albert_model/create_pretraining_data.py --input_file=$STORAGE_BUCKET/data/corpus/${PREFIX}/zhwiki-latest-pages-articles_${i}_${PREFIX}.txt --output_file=${STORAGE_BUCKET}/data/picto_trans/${PREFIX}_vocab_5000_length_256/zhwiki_train_examples_${i}_%s.tfrecord --vocab_file=./resources/tokenizer/${PREFIX}-5000-clean.vocab --spm_model_file=./resources/tokenizer/${PREFIX}-5000-clean.model --do_lower_case=True --do_whole_word_mask=True --max_seq_length=256 --max_predictions_per_seq=26 --masked_lm_prob=0.1 --dupe_factor=10 \
  $@ &
done