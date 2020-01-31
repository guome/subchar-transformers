# -*- coding: UTF-8 -*-

import json


def char2comp_txt2json(txt_dir, json_dir):
    dict_char2comp = {}

    with open(txt_dir, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if len(line) < 2:
                continue

            char = line[0]
            comp = line[1:].replace(" ", "", 20).strip()
            dict_char2comp[char] = comp

    with open(json_dir, "w", encoding="utf-8") as f:
        json.dump(dict_char2comp, f)


if __name__ == "__main__":
    txt_dir_ = "resources/char2comp.txt"
    json_dir_ = "resources/char2comp.json"
    char2comp_txt2json(txt_dir_, json_dir_)



