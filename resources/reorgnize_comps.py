# coding=utf-8


'''

三个来源的char2comps

1) JWE 项目爬取的新华字典的拆字结果，但是不全 resources/char2comp_httpcn.txt

2) RAN 文章的给出的汉字映射 resources/IDS_dictionary.txt

3) 来自 https://github.com/lanluoxiao/Chai 的拆字映射，但是比较杂  resources/char2comp.txt

部件集
1) http://www.guoxuedashi.com/zidian/bujian/ 的部件集
2）comps from GB13000.1 规范


'''
import copy
import json
import re

from tqdm import tqdm

###################
# comp_set from gb13000.1
###################

comp_set_gb13000 = set()
with open("resources/comps_gb13000.1.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if len(line) < 2:
            continue

        comps_ = list(line)
        comps_ = [w.strip() for w in line if len(w.strip()) > 0]

        for comp in comps_:
            comp_set_gb13000.add(comp)

print("there are %d comps from GB13000.1: ", len(comp_set_gb13000))
print(comp_set_gb13000)


###################
# comp_set from guoxuedashi
###################

comp_set_guoxue = set()
with open("resources/comps_guoxuedashi_com.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if len(line) < 2:
            continue

        comps_ = line.split("\t")[1]

        comps_ = list(comps_)
        for comp in comps_:
            comp_set_guoxue.add(comp)

print("there are %d comps from guoxuedashi: ", len(comp_set_guoxue))
# print("there are %d comps overlapping with  comp_set_gb13000: ", len(comp_set_guoxue.intersection(comp_set_gb13000)))

print(comp_set_guoxue)

with open("resources/comps_guoxuedashi.json", "w", encoding="utf-8") as f:
    json.dump(list(comp_set_guoxue), f, ensure_ascii=False)


comp_set_httpcn = set()
chars_httpcn = []

dict_char2comp_httpcn = {}
with open("resources/char2comp_httpcn.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if len(line) < 2:
            continue

        line = line.split(" ")
        line = [w.strip() for w in line if len(w.strip()) > 0]

        char_ = line[0]
        chars_httpcn.append(char_)

        if len(line) < 3:
            continue

        comp_ = line[1: ]
        if not isinstance(comp_, list):
            comp_ = [comp_]
        for c in comp_:
            if c not in comp_set_httpcn:
                comp_set_httpcn.add(c)

        dict_char2comp_httpcn[char_] = comp_


print("there are %d chars : ", len(chars_httpcn))
print("there are %d chars have comps: ", len(dict_char2comp_httpcn))
print("there are %d comps from httpcn: ", len(comp_set_httpcn))
print("there are %d comps overlapping with  comp_set_guoxue: ", len(comp_set_httpcn.intersection(comp_set_guoxue)))
# print("there are %d comps overlapping with  comp_set_gb13000: ", len(comp_set_httpcn.intersection(comp_set_gb13000)))

# for comp in comp_set_httpcn:
#     if comp in chars_httpcn:
#         dict_char2comp_httpcn[comp] = comp
#
# for comp in comp_set_guoxue:
#     if comp in chars_httpcn:
#         dict_char2comp_httpcn[comp] = comp

# print("there are %d chars have comps: ", len(dict_char2comp_httpcn))


comp_set_ids = set()
chars_ids = []
ids_comp2freq = {}

special_tokens = ['⿱', '⿰', '⿸',
                  '⿳', '⿹', '⿻',
                  '⿵', '⿺',
                  '⿴',
                  '⿶', '⿲',
                  '⿷',
                   ]

#
# # special_tokens = [('⿱', 31547), ('⿰', 27317), ('⿸', 3341),
# #                   ('⿳', 2633), ('⿹', 2420), ('⿻', 2264),
# #                   ('⿵', 1940), ('⿺', 1431), ('𠂊', 966),
# #                   ('⿴', 895), ('𠂉', 560), ('&CDP-885E;', 549),
# #                   ('㐅', 477), ('&CDP-8CBB;', 458), ('䒑', 437),
# #                   ('⿶', 400), ('⿲', 393), ('𠂇', 346), ('コ', 341),
# #                   ('&CDP-896A;', 326), ('龰', 322), ('⿷', 322),
# #                   ('⺌', 322), ('𠁣', 278), ('𠃛', 278), ('⺊', 275),
# #                   ('&CDP-8B7C;', 270), ('龷', 260), ('糸', 256), ('𠘧', 230),
# #                   ('龶', 218), ('𧘇', 194), ('乀', 172), ('㐄', 171),
# #                   ('㔾', 166), ('𠄌', 161), ('𠂒', 158), ('龴', 147),
# #                   ('&CDP-8CB5;', 140), ('㇇', 133), ('𠂆', 132),
# #                   ('&CDP-88C8;', 125), ('𠃊', 125), ('𠃌', 119),
# #                   ('⺆', 115), ('朩', 114), ('氺', 112), ('&CDP-89A9;', 104),
# #                   ('&CDP-8964;', 103), ('&CDP-8CAC;', 84), ('𡗗', 81),
# #                   ('&CDP-8A77;', 81), ('⺀', 80), ('𫝀', 79), ('谷', 79),
# #                   ('&CDP-8BCB;', 70), ('𣥂', 67), ('&CDP-8D46;', 63), ('𭕄', 63),
# #                   ('&CDP-8BBF;', 61), ('&CDP-89B0;', 60), ('𠂤', 58), ('&CDP-8BC5;', 54),
# #                   ('&CDP-89C5;', 53), ('𧰨', 52), ('𠃋', 52), ('&CDP-88EE;', 48),
# #                   ('&CDP-8BD0;', 47), ('㠯', 46), ('&CDP-89CC;', 44), ('𠃜', 43),
# #                   ('&CDP-8960;', 40), ('㡀', 39), ('冎', 39), ('&CDP-89CA;', 39),
# #                   ('朿', 37), ('&CDP-8C7A;', 35), ('&CDP-8C4E;', 33), ('東', 32),
# #                   ('&CDP-88A1;', 32), ('&CDP-884A;', 30), ('肅', 27), ('⺄', 26),
# #                   ('&CDP-8BF8;', 26), ('&CDP-89E0;', 24), ('&CDP-87C5;', 24),
# #                   ('㣺', 22), ('爲', 21), ('&CDP-8C4B;', 21), ('&CDP-8C66;', 21),
# #                   ('&CDP-8977;', 21), ('𠃓', 19), ('熏', 19), ('𡿨', 19), ('㇉', 18),
# #                   ('&CDP-89DF;', 18), ('𦣞', 18), ('&CDP-8CD4;', 18), ('&CDP-8CBD;', 17),
# #                   ('毌', 16), ('豖', 16), ('丣', 16), ('&CDP-8DDF;', 16), ('歺', 15),
# #                   ('&CDP-8CE4;', 14), ('&CDP-88F1;', 14), ('&CDP-89EE;', 13), ('艹', 13),
# #                   ('𩰋', 12), ('𩰊', 12), ('飛', 10), ('龜', 9), ('&CDP-8959;', 9), ('𠂎', 8),
# #                   ('龵', 7), ('③', 7), ('𠃍', 7), ('&CDP-895C;', 7), ('㐆', 6), ('丱', 6),
# #                   ('𣎳', 6), ('𠃑', 6), ('為', 6), ('&CDP-85F0;', 6), ('年', 5), ('&CDP-8BEA;', 5),
# #                   ('粛', 5), ('㐁', 5), ('&CDP-89DE;', 5), ('&CDP-8D6B;', 5), ('事', 4), ('㇓', 4),
# #                   ('夊', 4), ('𠁁', 4), ('𠃎', 4), ('𤴔', 4), ('円', 3), ('乁', 3), ('卝', 3), ('𫠣', 3),
# #                   ('㇣', 3), ('&CDP-8AF2;', 3), ('亜', 3),
# #                   ('𩙿', 3), ('&CDP-88E2;', 3), ('秉', 2),
# #                   ('承', 2), ('乗', 2), ('㇀', 2), ('&CDP-88D4;', 2),
# #                   ('襾', 2), ('书', 1), ('已', 1), ('孑', 1), ('⺁', 1),
# #                   ('\ue818', 1), ('⺈', 1), ('\ue81e', 1),
# #                   ('⺗', 1), ('⺧', 1), ('⺪', 1), ('凸', 1), ('飞', 1),
# #                   ('&CDP-89B9;', 1), ('&CDP-89E4;', 1), ('𠄎', 1), ('&CDP-8A4D;', 1),
# #                   ('&CDP-8846;', 1), ('卐', 1), ('孓', 1), ('㸦', 1), ('匸', 1), ('乄', 1),
# #                   ('&CDP-8A4E;', 1), ('曱', 1), ('&CDP-8665;', 1), ('䍏', 1), ('孒', 1),
# #                   ('&CDP-88B9;', 1), ('&CDP-8A49;', 1), ('㐧', 1), ('𥘅', 1), ('乜', 1),
# #                   ('釒', 1), ('卍', 1), ('&CDP-8961;', 1), ('⑮', 1), ('戼', 1), ('△', 1),
# #                   ('&CDP-8AEB;', 1), ('&CDP-876E;', 1), ('&CDP-8661;', 1), ('&CDP-88D3;', 1),
# #                   ('&CDP-88D5;', 1), ('訁', 1), ('亊', 1), ('兂', 1),
# #                   ('㱐', 1), ('𦣝', 1)]
#
#
dict_char2comp_ids = {}
count_0 = 0
count_1 = 0
with open("resources/IDS_dictionary.txt", "r", encoding="utf-8") as f:
    for line in tqdm(f):
        line = line.strip()
        if len(line) < 2:
            continue

        # if re.search(r"[a-zA-Z]", line):
        #     continue

        char = line.split(":")[0]
        chars_ids.append(char)

        comps = line.split(":")[1].split(" ")
        comps = [w.strip() for w in comps if len(w.strip()) > 0 and w.strip() not in special_tokens]
        comps = comps

        # print(char, comps)

        if char in dict_char2comp_httpcn:
            # comps = dict_char2comp_httpcn[char]

            count_1 += 1
            if set(dict_char2comp_httpcn[char]) != set(comps) and len(dict_char2comp_httpcn[char]) == len(comps):
                count_0 += 1
                # print(count_0, char, comps, "***", dict_char2comp_httpcn[char])


#
        comps_join = "".join(comps)
        if re.search("[a-zA-Z]", comps_join):

            if char in dict_char2comp_httpcn:
                comps = dict_char2comp_httpcn[char]
            else:
                continue

        if any(w in comps_join for w in unknow_tokens):
            continue

        for c in comps:

            # if c not in comp_set_httpcn and c not in special_tokens:
            if c not in special_tokens:
                comp_set_ids.add(c)

                if c not in ids_comp2freq:
                    ids_comp2freq[c] = 0
                ids_comp2freq[c] += 1

        dict_char2comp_ids[char] = comps
#
#
print("there are %d chars : ", len(chars_ids))
print("there are %d chars have comps (IDS): ", len(dict_char2comp_ids))
print("there are %d chars in httpcn: ", count_1)
print("there are %d comps (IDS): ", len(comp_set_ids))
print(sorted(list(ids_comp2freq.items()), key=lambda x: x[1], reverse=True))

print("there are %d comps overlapping with  comp_set_guoxue: ", len(comp_set_ids.intersection(comp_set_guoxue)))
#

comps_not_in_common = comp_set_guoxue.difference(comp_set_ids)
with open("resources/comps_not_in_common.json", "w", encoding="utf-8") as f:
    json.dump(list(comps_not_in_common), f, ensure_ascii=False)

# for comp in comp_set_ids:
#     print(comp)

for comp in comp_set_ids:
    dict_char2comp_ids[comp] = [comp]

    # if comp in dict_char2comp_ids:
    #     print(comp, dict_char2comp_ids[comp])
    if comp in chars_ids:
        dict_char2comp_ids[comp] = comp

for comp in comps_not_in_common:
    if comp not in chars_ids:
        print("very rare: ", comp)

for comp in comp_set_gb13000:
    if comp not in chars_ids:
        print("very rare: ", comp)



# 进一步精细化 comps
dict_char2comp_ids_copy = copy.deepcopy(dict_char2comp_ids)
for char, comps in dict_char2comp_ids_copy.items():
    comps_new = []
    for c in comps:
        if c in dict_char2comp_ids:
            comps_new.extend(dict_char2comp_ids[c])
        else:
            comps_new.append(c)

    dict_char2comp_ids[char] = comps_new

comps_set_ids = set()
for char, comps in dict_char2comp_ids.items():
    for c in comps:
        comps_set_ids.add(c)

print("there are %d comps: ", len(comps_set_ids))
print("there are %d comps: ", comps_set_ids)


with open("resources/char2comp_ids.json" , "w", encoding="utf-8") as f:
    json.dump(dict_char2comp_ids, f, ensure_ascii=False)

