#!/bin/bash

### run pretrain

python3 albert_model/run_pretraining.py --input_file=./albert_model/experiments/subchar_lower_vocab_5000/zhwiki_train_examples_*.tfrecord --output_dir=./albert_model/experiments/outputs/uncased_vocab_5000_time_0216/ --albert_config_file=./albert_model/experiments/albert_base_v2_config_vocab_5000.json --do_train --do_eval --dev_input_file=./albert_model/experiments/subchar_lower_vocab_5000/zhwiki_dev_examples_*.tfrecord --use_tpu --num_tpu_cores=8 --tpu_name=${TPU_NAME} --train_batch_size=1024 --eval_batch_size=64 --max_seq_length=512 --max_predictions_per_seq=52 --optimizer="lamb" --learning_rate=5e-5 --num_train_steps=100000 --num_warmup_steps=3000 --save_checkpoints_steps=10000