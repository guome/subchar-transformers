#!/usr/bin/env bash
# @Author: Michael Zhu
# @Date:   2020-03-04
# @Last Modified by:   michael
# @Last Modified time: 2020-03-04 21:28:30

export STORAGE_BUCKET=gs://sbt0
export TPU_NAME=subchar-trans-run-iflytek

TASK_NAME="iflytek"
MODEL_NAME="subchar_transformers_albert_base_128"

# CURRENT_DIR=$(cd -P -- "$(dirname -- "$0")" && pwd -P)

export ALBERT_CONFIG_DIR=./albert_model/experiments/albert_base_v2_config_vocab_5000.json
# export ALBERT_CONFIG_DIR=./albert_model/experiments/albert_base_config_vocab_5000.json

export ALBERT_PRETRAINED_MODELS_DIR_LEN_128=${STORAGE_BUCKET}/experiments/uncased_vocab_5000_length_128_steps_125k_time_0220
export ALBERT_PRETRAINED_MODELS_DIR_LEN_256=${STORAGE_BUCKET}/experiments/uncased_vocab_5000_length_256_steps_125k_time_0221

export GLUE_DATA_DIR=./datasets/CLUE/

export OUTPUT_DIR=$STORAGE_BUCKET/experiments/${MODEL_NAME}_${TASK_NAME}_${CURRENT_TIME}

# download and unzip dataset
# if [ ! -d $GLUE_DATA_DIR ]; then
#   mkdir -p $GLUE_DATA_DIR
#   echo "makedir $GLUE_DATA_DIR"
# fi
# cd $GLUE_DATA_DIR
# if [ ! -d $TASK_NAME ]; then
#   mkdir $TASK_NAME
#   echo "makedir $GLUE_DATA_DIR/$TASK_NAME"
# fi
# cd $TASK_NAME
# if [ ! -f "train.json" ] || [ ! -f "dev.json" ] || [ ! -f "test.json" ]; then
#   rm *
#   wget https://storage.googleapis.com/cluebenchmark/tasks/iflytek_public.zip
#   unzip iflytek_public.zip
#   rm iflytek_public.zip
# else
#   echo "data exists"
# fi
# echo "Finish download dataset."


pip3 install tensorflow_hub
pip3 install sentencepiece
pip3 install jieba


# run task

echo "Start running..."
python3 albert_model/run_classifier_clue.py \
  --task_name=$TASK_NAME \
  --data_dir=$GLUE_DATA_DIR/$TASK_NAME \
  --output_dir=$OUTPUT_DIR \
  --init_checkpoint=$ALBERT_PRETRAINED_MODELS_DIR_LEN_128/model.ckpt-125000 \
  --albert_config_file=$ALBERT_CONFIG_DIR \
  --vocab_file=./resources/tokenizer/5000-clean.vocab \
  --spm_model_file=./resources/tokenizer/5000-clean.model \
  --do_train=true \
  --do_eval=true \
  --do_predict \
  --do_lower_case \
  --max_seq_length=128 \
  --optimizer=adamw \
  --train_batch_size=32 \
  --learning_rate=2e-5 \
  --warmup_step=500 \
  --save_checkpoints_steps=250 \
  --train_step=10000 \
  --use_tpu=True \
  --tpu_name=${TPU_NAME} \
  --num_tpu_cores=1


