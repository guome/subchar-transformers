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
import tensorflow.compat.v1 as tf

import tqdm


sys.path.append("./")


def text_file2files(from_file, to_file_regex, num_docs_per_file=1e+3):
    # with open(from_file, 'r', encoding='utf-8') as in_f:
    with tf.gfile.GFile(from_file, 'r') as in_f:
        list_docs = []
        count_docs = 0
        file_idx = 0
        for line in tqdm.tqdm(in_f):

            # line = line.strip()
            # if line == "</doc>\n":
            if line == "\n":
                count_docs += 1
                list_docs.append("\n")
            else:
                list_docs.append(line)

            if count_docs > 0 and count_docs % num_docs_per_file == 0 and list_docs[-1] == "\n":
                file_idx += 1
                to_file = to_file_regex % str(file_idx)
                print("to_file: ", to_file)
                print("count_docs: ", count_docs)
                print("file_idx: ", file_idx)

                # with open(to_file, 'w', encoding='utf-8') as out_f:
                # writer = tf.gfile.GFile(output_eval_file, "w")
                with tf.gfile.GFile(to_file, 'w') as out_f:
                    for line in list_docs:
                        out_f.write(line)

                list_docs = []

        if len(list_docs) > 0:
            file_idx += 1
            to_file = to_file_regex % str(file_idx)
            # with open(to_file, 'w', encoding='utf-8') as out_f:
            with tf.gfile.GFile(to_file, 'w') as out_f:
                for line in list_docs:
                    out_f.write(line)


if __name__ == "__main__":
    STORAGE_BUCKET = "gs://sbt0"

    from_file = os.path.join(
        STORAGE_BUCKET,
        "data/corpus/char_lower/zhwiki-latest-pages-articles_char_lower.txt"
    )
    # tf.gfile.Copy(from_file, "./zhwiki-latest-pages-articles.txt")
    #
    # from_file = "./zhwiki-latest-pages-articles.txt"

    to_file_regex = os.path.join(
        STORAGE_BUCKET,
        "data/corpus/splited/zhwiki-latest-pages-articles_%s.txt"
    )
    text_file2files(
        from_file,
        to_file_regex,
        num_docs_per_file=5e+3
    )



    
