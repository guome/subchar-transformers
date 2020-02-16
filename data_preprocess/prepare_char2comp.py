# -*- coding: UTF-8 -*-

import json


def char2comp_txt2json(txt_dir, json_dir):
    dict_char2comp = {}

    comp_set = set()

    with open(txt_dir, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if len(line) < 2:
                continue

            line = line.split("\t")
            line = [w.strip() for w in line if len(w.strip()) > 0]
            if len(line) < 2:
                raise ValueError

            char = line[0]
            if len(char) != 1:
                raise ValueError

            comp = line[1].replace(" ", "", 20).strip()

            if char == "□":
                continue

            if char in dict_char2comp:
                if dict_char2comp[char] != comp:
                    print("**********")
                    print("char: ", char)
                    print(dict_char2comp[char])
                    print(comp)
                    print("**********")
                # assert dict_char2comp[char] == comp

            else:
                dict_char2comp[char] = comp

                comp_set = comp_set.union(set(comp))

    print("there are %d comps: " % len(comp_set))
    print("there are %d chars: " % len(dict_char2comp))

    with open(json_dir, "w", encoding="utf-8") as f:
        json.dump(dict_char2comp, f)


if __name__ == "__main__":
    txt_dir_ = "resources/char2comp.txt"
    json_dir_ = "resources/char2comp.json"
    char2comp_txt2json(txt_dir_, json_dir_)

    import torch
    torch.nn.ReLU()



