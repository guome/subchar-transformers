#!/bin/bash

### run pretrain

export STORAGE_BUCKET=gs://sbt0
export TPU_NAME=michaelwzhu91

python3 albert_model/run_pretraining.py --input_file=${STORAGE_BUCKET}/subchar_lower_vocab_5000/zhwiki_train_examples_*_*.tfrecord --output_dir=${STORAGE_BUCKET}/uncased_vocab_5000_time_0216/ --albert_config_file=./albert_model/experiments/albert_base_v2_config_vocab_5000.json --do_train --do_eval --dev_input_file=${STORAGE_BUCKET}/subchar_lower_vocab_5000/zhwiki_dev_examples_*_*.tfrecord --use_tpu --num_tpu_cores=8 --tpu_name=${TPU_NAME} --train_batch_size=512 --eval_batch_size=64 --max_seq_length=512 --max_predictions_per_seq=52 --optimizer="lamb" --learning_rate=2e-4 --num_train_steps=62500 --num_warmup_steps=3125 --save_checkpoints_steps=5000