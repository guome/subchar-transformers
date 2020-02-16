# -*- coding: UTF-8 -*-
import json
import re

# from blingfire import *
import jieba
import sys
import tqdm


def char2comp_single_char(zh_char, dict_char2comp):
    if zh_char in dict_char2comp:
        zh_char_comp = dict_char2comp[zh_char].strip()
        return zh_char_comp
    else:
        return None


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


def char2comp_single_sent(sent, dict_char2comp):
    sent_new_ = ""

    sent = list(jieba.cut(sent))
    sent = " ".join(sent)
    for char_ in sent:

        if re.search("[\u4e00-\u9fa5]", char_):
            tmp_ = char2comp_single_char(char_, dict_char2comp)
            if tmp_:
                sent_new_ += " " + tmp_ + " "
            else:
                sent_new_ += " " + char_ + " "
        else:
            sent_new_ += char_

    # drop redundent blank
    sent_new_ = drop_extra_blank(sent_new_)

    return sent_new_


def char2comp_file(txt_file, to_file, dict_char2comp=None, do_lower_case=1):
    with open(to_file, "w", encoding="utf-8") as out_f:
        with open(txt_file, "r", encoding="utf-8") as in_f:
            for i, line in tqdm.tqdm(enumerate(in_f)):
                line = line.strip()
                if len(line) == 0:
                    out_f.write("\n")
                    continue

                sent_new_ = char2comp_single_sent(line, dict_char2comp)
                if do_lower_case:
                    sent_new_ = sent_new_.lower()

                out_f.write(sent_new_ + "\n")


if __name__ == "__main__":
    txt_file_ = "datasets/examples/corpus_zh_example_0.txt"
    # txt_file_ = "datasets/examples/a.txt"
    to_file_ = "datasets/examples/corpus_zh_example_subchar_0.txt"

    dict_char2comp_ = json.load(open("resources/char2comp.json", "r", encoding="utf-8"))
    char2comp_file(
        txt_file_,
        to_file_,
        dict_char2comp=dict_char2comp_
    )

