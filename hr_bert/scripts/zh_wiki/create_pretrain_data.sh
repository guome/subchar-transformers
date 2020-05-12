#!/bin/bash

### multi-processing version

pip3 install jieba_fast
pip3 install tokenizers
pip3 install boto3

export STORAGE_BUCKET=gs://sbt0

# NUM_PROC=218
NUM_PROC=100

for i in `seq 100 $((NUM_PROC))`; do
  python3 src/create_pretraining_data.py --input_file=$STORAGE_BUCKET/data/corpus/char_no_space_lower/zhwiki-latest-pages-articles_${i}_char_no_space_lower.txt --output_file=${STORAGE_BUCKET}/data/h_bert/data_records/zhwiki_train_examples_${i}_%s.tfrecord --do_lower_case=True --do_whole_word_mask=True --max_seq_length=512 --max_sememe_length=16 --max_predictions_per_seq=51 --masked_lm_prob=0.1 --dupe_factor=10 --flashtext_dict_dir resources/dict_hownet_flashtext.json --bert_tokenizer_name bert-base-chinese --dict_word2sememes_dir resources/dict_word2sememes.json --dict_sememe2id_dir resources/dict_sememe2id.json \
  $@ &
done

# python src/create_pretraining_data.py --input_file=datasets/zh_sample/wiki.valid.raw --output_file=experiments/zh_sample/wiki.valid.raw.%s.tfrecord --do_lower_case=True --do_whole_word_mask=True --max_seq_length=512 --max_sememe_length=16 --max_predictions_per_seq=51 --masked_lm_prob=0.1 --dupe_factor=10 --flashtext_dict_dir resources/dict_hownet_flashtext.json --bert_tokenizer_name bert-base-chinese --dict_word2sememes_dir resources/dict_word2sememes.json --dict_sememe2id_dir resources/dict_sememe2id.json