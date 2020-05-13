#!/usr/bin/env bash
# @Author: Michael Zhu
# @Date:   2020-03-04
# @Last Modified by:   michael
# @Last Modified time: 2020-03-04 21:28:30


export STORAGE_BUCKET=gs://sbt0
export TPU_NAME=h-bert-0


pip3 install tensorflow_hub
pip3 install sentencepiece
pip3 install jieba

# run task

echo "Start running..."
RUN_TIMES=10
for run_idx in `seq 1 $((RUN_TIMES))`; do

    python3 src/vanilla_albert/run_classifier.py \
      --task_name=chn \
      --data_dir=datasets/ChnSentiCorp \
      --output_dir=${STORAGE_BUCKET}/experiments/h_bert/finetune/chn_length_512_sememe_16_steps_125k_time_0512_0_vanilla/ \
      --init_checkpoint=${STORAGE_BUCKET}/experiments/h_bert/pretraining/length_512_sememe_16_steps_125k_vanilla_time_0508_0/model.ckpt-125000 \
      --albert_config_file=./resources/albert_base_v2/config.json \
      --do_train=true \
      --do_eval=true \
      --do_predict \
      --do_lower_case \
      --max_seq_length=128 \
      --max_sememe_length=16 \
      --optimizer=adamw \
      --train_batch_size=32 \
      --learning_rate=2e-5 \
      --warmup_step=400 \
      --save_checkpoints_steps=400 \
      --train_step=10000 \
      --use_tpu=True \
      --tpu_name=${TPU_NAME} \
      --num_tpu_cores=1 \
      --bert-base-chinese \
      --dict_word2sememes_dir resources/dict_word2sememes.json \
      --dict_sememe2id_dir resources/dict_sememe2id.json \
      --flashtext_dict_dir resources/dict_hownet_flashtext.json


done


# python src/vanilla_albert/run_classifier.py --task_name=chn --data_dir=datasets/ChnSentiCorp --output_dir=./experiments/h_bert/finetune/chn_length_512_sememe_16_steps_125k_time_0512_0/ --init_checkpoint=experiments/zh_sample/model.ckpt-12 --albert_config_file=./resources/albert_base_v2/config.json --do_train=true --do_eval=true --do_predict=true --do_lower_case --max_seq_length=128 --max_sememe_length=16 --optimizer=adamw --train_batch_size=2 --learning_rate=2e-5 --warmup_step=20 --save_checkpoints_steps=30 --train_step=100 --bert_tokenizer_name bert-base-chinese --dict_word2sememes_dir resources/dict_word2sememes.json --dict_sememe2id_dir resources/dict_sememe2id.json --flashtext_dict_dir resources/dict_hownet_flashtext.json