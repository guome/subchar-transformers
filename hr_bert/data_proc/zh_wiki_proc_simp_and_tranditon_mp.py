# -*- coding: utf-8 -*-
import json
# import sys
# from pathlib import Path
#
# import tqdm
# from blingfire import text_to_sentences
import re

import sys

import jieba
import tqdm

import tensorflow.compat.v1 as tf

sys.path.append("./")
from hr_bert.chinese_utils.chinese_tranditional2simplified import traditional2simplified, simplified2traditional


def drop_extra_blank(sent):

    sent_new = ""
    sent = sent.strip()
    prev_is_blank = False

    for i, char_ in enumerate(sent):
        if char_ == " " and prev_is_blank:
            continue
        elif char_ == " " and not prev_is_blank:
            sent_new += char_
            prev_is_blank = True
            continue
        else:
            sent_new += char_
            prev_is_blank = False
            continue

    return sent_new


def split_sent(text_, spliter="。？?"):
    list_sents = []
    tmp_sent = ""
    for char_ in text_:
        if char_ in spliter:
            if len(tmp_sent) == 0:
                continue
            else:
                tmp_sent += char_
                list_sents.append(tmp_sent)
                tmp_sent = ""

        else:
            tmp_sent += char_

    if len(tmp_sent) > 0:
        list_sents.append(tmp_sent)

    return list_sents


def proc_file(txt_file, to_file, do_lower_case=1):
    # with open(to_file, "w", encoding="utf-8") as out_f:
    with tf.gfile.GFile(to_file, "w") as out_f:
        # with open(txt_file, "r", encoding="utf-8") as in_f:
        with tf.gfile.GFile(txt_file, "r") as in_f:
            passage = []

            for i, line in tqdm.tqdm(enumerate(in_f)):
                line = line.strip()
                if len(line) > 0:
                    passage.append(line)

                else:
                    if len(passage) > 0:
                        passage_new_0 = []
                        for sent in passage:
                            if do_lower_case:
                                sent_new_ = sent.lower()
                            else:
                                sent_new_ = sent

                            # 繁体转简体
                            sent_new_ = traditional2simplified(sent_new_)
                            passage_new_0.append(sent_new_)

                        passage_new_1 = []
                        for sent in passage:
                            if do_lower_case:
                                sent_new_ = sent.lower()
                            else:
                                sent_new_ = sent

                            # 繁体转简体
                            sent_new_ = simplified2traditional(sent_new_)
                            passage_new_1.append(sent_new_)

                        for sent in passage_new_0:
                            out_f.write(sent + "\n")
                        out_f.write("\n")

                        if passage_new_1 != passage_new_0:
                            for sent in passage_new_1:
                                out_f.write(sent + "\n")
                            out_f.write("\n")


def main():
    file_in = str(sys.argv[1])
    file_out = str(sys.argv[2])
    do_lower_case = int(sys.argv[3])

    print('Pre-processing {} to {}...'.format(file_in, file_out))
    proc_file(file_in, file_out, do_lower_case=do_lower_case)

    print('Successfully pre-processed {} to {}...'.format(file_in, file_out))


if __name__ == '__main__':
    main()
