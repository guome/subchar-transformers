#!/bin/bash

### run pretrain

export STORAGE_BUCKET=gs://sbt0
export TPU_NAME=subchar-trans-128

python3 albert_model/run_pretraining.py --input_file=${STORAGE_BUCKET}/data/char_lower_vocab_15000_length_256/zhwiki_train_examples_*_*.tfrecord --output_dir=${STORAGE_BUCKET}/experiments/char_uncased_vocab_15000_length_256_steps_125k_time_0319/ --albert_config_file=./albert_model/experiments/albert_base_v2_config_vocab_15000.json --do_train --do_eval --dev_input_file=${STORAGE_BUCKET}/data/char_lower_vocab_15000_length_256/zhwiki_train_examples_10_*.tfrecord --use_tpu --num_tpu_cores=8 --tpu_name=${TPU_NAME} --train_batch_size=1024 --eval_batch_size=64 --max_seq_length=256 --max_predictions_per_seq=26 --optimizer="lamb" --learning_rate=4e-4 --num_train_steps=3000 --num_warmup_steps=3125 --save_checkpoints_steps=1000