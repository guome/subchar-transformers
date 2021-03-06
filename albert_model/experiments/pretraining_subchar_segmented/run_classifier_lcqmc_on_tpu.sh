#!/usr/bin/env bash
# @Author: Michael Zhu
# @Date:   2020-03-04
# @Last Modified by:   michael
# @Last Modified time: 2020-03-04 21:28:30

CURRENT_TIME=$(date "+%Y%m%d-%H%M%S")

export STORAGE_BUCKET=gs://sbt0
export TPU_NAME=grpc://10.154.114.146:8470

TASK_NAME="lcqmc"
PREFIX=subchar_segmented_lower

MODEL_NAME="${PREFIX}_albert_tiny"

# CURRENT_DIR=$(cd -P -- "$(dirname -- "$0")" && pwd -P)

export ALBERT_CONFIG_DIR=./albert_model/experiments/albert_tiny_v2_config_vocab_5000.json

export ALBERT_PRETRAINED_MODELS_DIR_LEN_256=${STORAGE_BUCKET}/data/picto_trans/pretraining/${PREFIX}_vocab_5000_length_256_steps_125k_time_0326

export GLUE_DATA_DIR=./datasets/CLUE/


pip3 install tensorflow_hub
pip3 install sentencepiece
pip3 install jieba

# run task

echo "Start running..."
RUN_TIMES=10
for run_idx in `seq 1 $((RUN_TIMES))`; do

    OUTPUT_DIR=${STORAGE_BUCKET}/data/picto_trans/finetune/${TASK_NAME}/${PREFIX}_${MODEL_NAME}_${run_idx}/

    python3 albert_model/run_classifier_clue_subchar_segmented.py \
      --task_name=$TASK_NAME \
      --data_dir=$GLUE_DATA_DIR/$TASK_NAME \
      --output_dir=$OUTPUT_DIR \
      --init_checkpoint=$ALBERT_PRETRAINED_MODELS_DIR_LEN_256/model.ckpt-125000 \
      --albert_config_file=$ALBERT_CONFIG_DIR \
      --vocab_file=./resources/tokenizer/${PREFIX}-5000-clean.vocab \
      --spm_model_file=./resources/tokenizer/${PREFIX}-5000-clean.model \
      --do_train=true \
      --do_eval=true \
      --do_predict \
      --do_lower_case \
      --max_sent_length=64 \
      --max_seq_length=256 \
      --optimizer=adamw \
      --learning_rate=5e-5 \
      --warmup_step=1500 \
      --save_checkpoints_steps=1000 \
      --train_step=50000 \
      --use_tpu=True \
      --tpu_name=${TPU_NAME} \
      --num_tpu_cores=1 \

done