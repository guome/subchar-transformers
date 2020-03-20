# coding=utf-8

import json

import tensorflow.compat.v1 as tf

############
# 检查 resources/char2comp_ids.json 的一致性
############

# 1) 每个comp不能再分
import os

import tqdm

char2comps_ids = json.load(
    open("resources/char2comp_ids.json", "r", encoding="utf-8")
)

for char, comps in char2comps_ids.items():
    for comp in comps:

        assert comp in char2comps_ids

        if comp in char2comps_ids:

            if len(char2comps_ids[comp]) != 1:
                print(comp)

            assert len(char2comps_ids[comp]) == 1

        else:
            print(comp)


####################
# 找一个分隔符
####################

# 看看语料是否包含这个词
sep_token = ""

STORAGE_BUCKET = "gs://sbt0"
txt_file = os.path.join(
        STORAGE_BUCKET,
        "data/corpus/char_lower/zhwiki-latest-pages-articles_char_lower.txt"
)

with tf.gfile.GFile(txt_file, "r") as in_f:
    for i, line in tqdm.tqdm(enumerate(in_f)):
        line = line.strip()
        assert sep_token not in line
