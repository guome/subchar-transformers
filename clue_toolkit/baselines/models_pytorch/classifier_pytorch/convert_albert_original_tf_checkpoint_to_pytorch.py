"""Convert ALBERT checkpoint."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import torch

from transformers.modeling_albert import BertConfig, AlbertForPreTraining, load_tf_weights_in_albert

import logging
logging.basicConfig(level=logging.INFO)

def convert_tf_checkpoint_to_pytorch(tf_checkpoint_path, bert_config_file, pytorch_dump_path):
    # Initialise PyTorch model
    config = BertConfig.from_json_file(bert_config_file)
    print("Building PyTorch model from configuration: {}".format(str(config)))
    model = AlbertForPreTraining(config)

    # Load weights from tf checkpoint
    load_tf_weights_in_albert(model, config, tf_checkpoint_path)

    # Save pytorch-model
    print("Save PyTorch model to {}".format(pytorch_dump_path))
    torch.save(model.state_dict(), pytorch_dump_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    ## Required parameters
    parser.add_argument("--tf_checkpoint_path",
                        default = None,
                        type = str,
                        required = True,
                        help = "Path to the TensorFlow checkpoint path.")
    parser.add_argument("--bert_config_file",
                        default = None,
                        type = str,
                        required = True,
                        help = "The config json file corresponding to the pre-trained ALBERT model. \n"
                            "This specifies the model architecture.")
    parser.add_argument("--pytorch_dump_path",
                        default = None,
                        type = str,
                        required = True,
                        help = "Path to the output PyTorch model.")
    args = parser.parse_args()
    convert_tf_checkpoint_to_pytorch(args.tf_checkpoint_path,
                                     args.bert_config_file,
                                     args.pytorch_dump_path)

'''
python convert_albert_original_tf_checkpoint_to_pytorch.py \
    --tf_checkpoint_path=/home/lwt/NewDisk/chineseGLUE_pytorch/prev_trained_model/albert_tiny_tf \
    --bert_config_file=/home/lwt/NewDisk/chineseGLUE_pytorch/prev_trained_model/albert_tiny_tf/config.json \
    --pytorch_dump_path=/home/lwt/NewDisk/chineseGLUE_pytorch/prev_trained_model/albert_tiny/pytorch_model.bin
'''