# coding=utf-8


'''

三个来源的char2comps

1) JWE 项目爬取的新华字典的拆字结果，但是不全 resources/char2comp_httpcn.txt

2) RAN 文章的给出的汉字映射 resources/IDS_dictionary.txt

3) 来自 https://github.com/lanluoxiao/Chai 的拆字映射，但是比较杂  resources/char2comp.txt

'''
import re

from tqdm import tqdm

comp_set_httpcn = []
chars_httpcn = []

dict_char2comp_httpcn = {}
with open("resources/char2comp_httpcn.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if len(line) < 2:
            continue

        line = line.split(" ")
        line = [w.strip() for w in line]\

        char_ = line[0]
        chars_httpcn.append(char_)

        if len(line) < 3:
            continue

        comp_ = "".join(line[1: ])
        for c in comp_:
            if c not in comp_set_httpcn:
                comp_set_httpcn.append(c)

        dict_char2comp_httpcn[char_] = comp_


print("there are %d chars : ", len(chars_httpcn))
print("there are %d chars have comps: ", len(dict_char2comp_httpcn))
print("there are %d comps: ", len(comp_set_httpcn))

for comp in comp_set_httpcn:
    if comp in chars_httpcn:
        dict_char2comp_httpcn[comp] = comp

print("there are %d chars have comps: ", len(dict_char2comp_httpcn))


comp_set_ids = []
chars_ids = []

dict_char2comp_ids = {}
with open("resources/IDS_dictionary.txt", "r", encoding="utf-8") as f:
    for line in tqdm(f):
        line = line.strip()
        if len(line) < 2:
            continue

        # if re.search(r"[a-zA-Z]", line):
        #     continue

        char = line.split(":")[0]
        chars_ids.append(char)

        comps = line.split(":")[0].split(" ")
        comps = [w.strip() for w in line]

        comps = "".join(comps)
        for c in comps:
            if c not in comp_set_ids and c not in comp_set_httpcn:
                comp_set_ids.append(c)

        dict_char2comp_ids[char] = comps


print("there are %d chars : ", len(chars_ids))
print("there are %d chars have comps: ", len(dict_char2comp_ids))
print("there are %d comps: ", len(comp_set_ids))

# for comp in comp_set_ids:
#     if comp in chars_ids:
#         dict_char2comp_ids[comp] = comp
#
#
# print("there are %d chars have comps: ", len(dict_char2comp_ids))