#!/bin/bash

### multi-processing version

pip3 install tensorflow_hub
pip3 install sentencepiece


export STORAGE_BUCKET=gs://sbt0

# NUM_PROC=109
# NUM_PROC=20

#for i in `seq 1 $((NUM_PROC))`; do
#  python3 albert_model/create_pretraining_data.py --input_file=$STORAGE_BUCKET/data/corpus/subchar_lower/zhwiki-latest-pages-articles_${i}_subchar_lower.txt --output_file=${STORAGE_BUCKET}/data/subchar_lower_vocab_10000_length_128/zhwiki_train_examples_${i}_%s.tfrecord --vocab_file=./resources/tokenizer/subchar-10000-clean.vocab --spm_model_file=./resources/tokenizer/subchar-10000-clean.model --do_lower_case=True --do_whole_word_mask=True --max_seq_length=128 --max_predictions_per_seq=13 --masked_lm_prob=0.1 --dupe_factor=10 \
#  $@ &
#done

NUM_PROC=31

for i in `seq 31 $((NUM_PROC))`; do
  python3 albert_model/create_pretraining_data.py --input_file=$STORAGE_BUCKET/data/corpus/subchar_lower/zhwiki-latest-pages-articles_${i}_subchar_lower.txt --output_file=${STORAGE_BUCKET}/data/subchar_lower_vocab_10000_length_128/zhwiki_train_examples_${i}_%s.tfrecord --vocab_file=./resources/tokenizer/subchar-10000-clean.vocab --spm_model_file=./resources/tokenizer/subchar-10000-clean.model --do_lower_case=True --do_whole_word_mask=True --max_seq_length=128 --max_predictions_per_seq=13 --masked_lm_prob=0.1 --dupe_factor=10 \
  $@ &
done

NUM_PROC=36

for i in `seq 36 $((NUM_PROC))`; do
  python3 albert_model/create_pretraining_data.py --input_file=$STORAGE_BUCKET/data/corpus/subchar_lower/zhwiki-latest-pages-articles_${i}_subchar_lower.txt --output_file=${STORAGE_BUCKET}/data/subchar_lower_vocab_10000_length_128/zhwiki_train_examples_${i}_%s.tfrecord --vocab_file=./resources/tokenizer/subchar-10000-clean.vocab --spm_model_file=./resources/tokenizer/subchar-10000-clean.model --do_lower_case=True --do_whole_word_mask=True --max_seq_length=128 --max_predictions_per_seq=13 --masked_lm_prob=0.1 --dupe_factor=10 \
  $@ &
done