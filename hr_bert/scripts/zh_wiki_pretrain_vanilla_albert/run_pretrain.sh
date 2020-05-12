#!/bin/bash

### run pretrain

export STORAGE_BUCKET=gs://sbt0
export TPU_NAME=h-bert-1

python3 src/vanilla_albert/run_pretraining.py --input_file=${STORAGE_BUCKET}/data/h_bert/data_records/zhwiki_train_examples_*_*.tfrecord --output_dir=${STORAGE_BUCKET}/experiments/h_bert/pretraining/length_512_sememe_16_steps_125k_vanilla_time_0508_0/ --albert_config_file=./resources/albert_base_v2/config.json --do_train --do_eval --dev_input_file=${STORAGE_BUCKET}/data/h_bert/data_records/zhwiki_train_examples_110_*.tfrecord --use_tpu --num_tpu_cores=8 --tpu_name=${TPU_NAME} --train_batch_size=1024 --eval_batch_size=64 --max_seq_length=512 --max_sememe_length=16 --max_predictions_per_seq=51 --optimizer="lamb" --learning_rate=4e-4 --num_train_steps=125000 --num_warmup_steps=3125 --save_checkpoints_steps=5000