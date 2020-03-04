#!/usr/bin/env bash
# @Author: Michael Zhu
# @Date:   2020-02-19
# @Last Modified by:   Michael Zhu
# @Last Modified time: 2020-02-19 21:08:00



CURRENT_TIME=$(date "+%Y%m%d-%H%M%S")

TASK_NAME="afqmc"
MODEL_NAME="albert_base_zh_subchar"

export PREV_TRAINED_MODEL_DIR=gs://sbt0/uncased_vocab_5000_time_0216/

export ALBERT_CONFIG_DIR=./albert_model/experiments/albert_base_v2_config_vocab_5000.json

export CLUE_DATA_DIR=./albert_model/experiments/CLUEdataset

export DATA_DIR=$CLUE_DATA_DIR/$TASK_NAME/

export OUTPUT_DIR=gs://sbt0/ experiments/${MODEL_NAME}_${TASK_NAME}_tpu_0


# download and unzip dataset
# if [ ! -d $CLUE_DATA_DIR ]; then
#   mkdir -p CLUE_DATA_DIR
#   echo "makedir $CLUE_DATA_DIR"
# fi

# if [ ! -d $CLUE_DATA_DIR/$TASK_NAME ]; then
#   mkdir $CLUE_DATA_DIR/$TASK_NAME
#   echo "makedir $CLUE_DATA_DIR/$TASK_NAME"
# fi

# cd $CLUE_DATA_DIR/$TASK_NAME
# if [ ! -f "train.json" ] || [ ! -f "dev.json" ] || [ ! -f "test.json" ]; then
#   rm *
#   wget https://storage.googleapis.com/cluebenchmark/tasks/afqmc_public.zip
#   unzip afqmc_public.zip
#   rm afqmc_public.zip
# else
#   echo "data exists"
# fi
# echo "Finish download dataset."

# cd ../../../../

# run task
echo "Start running..."
python3 albert_model/run_classifier.py \
  --task_name=TASK_NAME \
  --data_dir=... \
  --output_dir=$OUTPUT_DIR \
  --init_checkpoint=$PREV_TRAINED_MODEL_DIR/model.ckpt \
  --albert_config_file=$ALBERT_CONFIG_DIR \
  --vocab_file=./resources/tokenizer/5000-clean.vocab \
  --spm_model_file=./resources/tokenizer/5000-clean.model \
  --do_train=true \
  --do_eval=true \
  --do_predict \
  --do_lower_case \
  --max_seq_length=128 \
  --optimizer=adamw \
  --train_batch_size=16 \
  --learning_rate=3e-5 \
  --save_checkpoints_steps=100 \
  --train_step=10000 \

