# -*- coding: utf-8 -*-
"""
@File: file_utils.py
@Copyright: 2019 Michael Zhu
@License：the Apache License, Version 2.0
@Author：Michael Zhu
@version：
@Date：
@Desc: 
"""
import os
import sys

import tqdm

import tensorflow.compat.v1 as tf

sys.path.append("./")


def txt_files2file(list_files, to_dir):
    # with open(to_dir, "w", encoding="utf-8") as out_f:
    with tf.gfile.GFile(to_dir, "w") as out_f:
        for file_ in list_files:
            # with open(file_, "r", encoding="utf-8") as in_f:
            with tf.gfile.GFile(file_, "r") as in_f:
                for line in tqdm.tqdm(in_f):
                    out_f.write(line)


if __name__ == "__main__":

    STORAGE_BUCKET = "gs://sbt0"

    list_files_ = []
    num_files = 218
    for i in range(num_files):
        file_ = os.path.join(
            STORAGE_BUCKET,
            "data/corpus/subchar_segmented_lower/zhwiki-latest-pages-articles_%d_subchar_segmented_lower.txt" % (i + 1)
        )
        list_files_.append(file_)

    to_dir_ = os.path.join(
        STORAGE_BUCKET,
        "data/corpus/subchar_segmented_lower/zhwiki-latest-pages-articles_subchar_segmented_lower.txt")
    txt_files2file(list_files_, to_dir_)

    # list_files_ = []
    # num_files = 218
    # for i in range(num_files):
    #     file_ = os.path.join(
    #         STORAGE_BUCKET,
    #         "data/corpus/char_spaced_lower/zhwiki-latest-pages-articles_%d_char_spaced_lower.txt" % (i + 1)
    #     )
    #     list_files_.append(file_)
    #
    # to_dir_ = os.path.join(
    #     STORAGE_BUCKET,
    #     "data/corpus/char_spaced_lower/zhwiki-latest-pages-articles_char_spaced_lower.txt")
    # txt_files2file(list_files_, to_dir_)

    # list_files_ = []
    # num_files = 110
    # for i in range(num_files):
    #     file_ = os.path.join(
    #         STORAGE_BUCKET,
    #         "data/corpus/subchar_lower/zhwiki-latest-pages-articles_%d_subchar_lower.txt" % (i + 1)
    #     )
    #     list_files_.append(file_)
    #
    # to_dir_ = os.path.join(
    #     STORAGE_BUCKET,
    #     "data/corpus/subchar_lower/zhwiki-latest-pages-articles_subchar_lower.txt")
    # txt_files2file(list_files_, to_dir_)

    # num_files = 110
    # for i in range(num_files):
    #     file_ = os.path.join(
    #         STORAGE_BUCKET,
    #         "data/corpus/char_lower/zhwiki-latest-pages-articles_%d_char_lower.txt" % (i + 1)
    #     )
    #     list_files_.append(file_)
    #
    # to_dir_ = os.path.join(
    #     STORAGE_BUCKET,
    #     "data/corpus/char_lower/zhwiki-latest-pages-articles_char_lower.txt")
    # txt_files2file(list_files_, to_dir_)




    
