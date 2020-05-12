#!/bin/bash

### multi-processing version

pip3 install jieba_fast
pip3 install tokenizers
pip3 install boto3

export STORAGE_BUCKET=gs://sbt0

# NUM_PROC=218
NUM_PROC=218

for i in `seq 181 $((NUM_PROC))`; do
  python3 src/create_pretraining_data.py --input_file=$STORAGE_BUCKET/data/corpus/char_no_space_lower_simplified/zhwiki-latest-pages-articles_${i}_char_no_space_lower_simplified.txt --output_file=${STORAGE_BUCKET}/data/h_bert/data_records_char_no_space_lower_simplified/zhwiki_train_examples_${i}_%s.tfrecord --do_lower_case=True --do_whole_word_mask=True --max_seq_length=512 --max_sememe_length=16 --max_predictions_per_seq=51 --masked_lm_prob=0.1 --dupe_factor=10 --flashtext_dict_dir resources/dict_hownet_flashtext.json --bert_tokenizer_name bert-base-chinese --dict_word2sememes_dir resources/dict_word2sememes.json --dict_sememe2id_dir resources/dict_sememe2id.json \
  $@ &
done