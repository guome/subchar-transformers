# coding=utf-8
import copy
import json
import os
import re

import tqdm

import tensorflow.compat.v1 as tf


#################
# 使用 RAN 的映射表，并保留田字格
#################
ids_dict_char2comps = {}
with open("resources/IDS_dictionary.txt", "r", encoding="utf-8") as f:
    for line in tqdm.tqdm(f):
        line = line.strip()
        if len(line) < 2:
            continue

        # if re.search(r"[a-zA-Z]", line):
        #     continue

        char = line.split(":")[0]

        comps = line.split(":")[1].split(" ")
        assert isinstance(comps, list)
        comps = [w.strip() for w in comps if len(w.strip()) > 0]

        # comps_clean = []
        # for comp in comps:
        #     if re.search("[a-zA-Z]", comp):
        #         assert "&CDP-" in comp
        #         assert ";" in comp
        #
        #         comp = comp.replace("&", "").replace("-", "").replace(";", "")
        #
        #     comps_clean.append(comp)

        ids_dict_char2comps[char] = comps

# 计数一下comp的频率
ids_dict_char2comps_copy = copy.deepcopy(ids_dict_char2comps)
dict_comp2freq = {}
for char, comps in ids_dict_char2comps_copy.items():
    for c in comps:
        if c not in dict_comp2freq:
            dict_comp2freq[c] = 0

        dict_comp2freq[c] += 1

list_comp2freq = list(dict_comp2freq.items())
list_comp2freq = sorted(list_comp2freq, key=lambda x: x[1], reverse=True)
list_comps = [w[0] for w in list_comp2freq]

print(len(list_comp2freq))
for item in list_comp2freq:
    print(item)

with open("resources/ids_list_comps.json", "w", encoding="utf-8") as f:
    json.dump(
        list_comps,
        f,
        ensure_ascii=False
    )


ids_dict_char2comps_joined = {}
for char, comps in ids_dict_char2comps.items():
    comps_join = "".join(comps)
    ids_dict_char2comps_joined[char] = comps_join

with open("resources/ids_dict_char2comps.json", "w", encoding="utf-8") as f:
    json.dump(
        ids_dict_char2comps,
        f,
        ensure_ascii=False
    )

with open("resources/ids_dict_char2comps_joined.json", "w", encoding="utf-8") as f:
    json.dump(
        ids_dict_char2comps_joined,
        f,
        ensure_ascii=False
    )