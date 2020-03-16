#!/bin/bash

### run pretrain

export STORAGE_BUCKET=gs://sbt0
export TPU_NAME=subchar-trans-10000-128

python3 albert_model/run_pretraining.py --input_file=${STORAGE_BUCKET}/data/subchar_lower_vocab_10000_length_128/zhwiki_train_examples_*_*.tfrecord --output_dir=${STORAGE_BUCKET}/experiments/uncased_vocab_10000_length_128_steps_125k_time_0315/ --albert_config_file=./albert_model/experiments/albert_base_v2_config_vocab_10000.json --do_train --do_eval --dev_input_file=${STORAGE_BUCKET}/data/subchar_lower_vocab_10000_length_128/zhwiki_dev_examples_*_*.tfrecord --use_tpu --num_tpu_cores=8 --tpu_name=${TPU_NAME} --train_batch_size=1024 --eval_batch_size=64 --max_seq_length=128 --max_predictions_per_seq=13 --optimizer="lamb" --learning_rate=4e-4 --num_train_steps=125000 --num_warmup_steps=3125 --save_checkpoints_steps=5000