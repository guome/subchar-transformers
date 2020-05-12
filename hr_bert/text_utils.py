import json
import re

import jieba_fast as jieba
import sys

import six
import tqdm

from src.keyword_processor import get_sememes_flashtext, KeywordProcessor
from src.tokenization_bert import BertTokenizer

sys.path.append("./")
jieba.load_userdict("resources/vocab_jieba.txt")


# def zh_tokenize_single_sent(sent):
#
#     sent = list(jieba.cut(sent))
#     sent = [w.strip() for w in sent if len(w.strip()) > 0]
#     print(sent)
#
#     sent_new = []
#     for seg in sent:
#
#         if re.search("[\u4e00-\u9fa5]", seg):
#             tmp_ = ""
#             for char in seg:
#                 # print(char)
#                 if re.search("[\u4e00-\u9fa5]", char):
#                     if tmp_:
#                         sent_new.append(tmp_)
#                         tmp_ = ""
#                     sent_new.append(char)
#                 else:
#                     tmp_ += char
#
#             if tmp_:
#                 sent_new.append(tmp_)
#
#         else:
#             sent_new.append(seg)
#
#     return sent_new


def zh_tokenize_single_sent(sent):
    sent = list(jieba.cut(sent))
    sent = [w.strip() for w in sent if len(w.strip()) > 0]
    return sent


def get_subword_tokenize_and_sememes(text, bpe_tokenizer, processor, dict_word2sememes, max_sememe_length=12):
    if re.search("[^\u4e00-\u9fa5]", text):
        # 有非中文字符
        subword = bpe_tokenizer._tokenize(text)
        subword_sememes = []
        for tok in subword:
            if tok in dict_word2sememes:
                semes = dict_word2sememes[tok]

                semes = semes[:max_sememe_length]  # limit the length

                subword_sememes.append(semes)
            else:
                subword_sememes.append([])

    else:
        subword = bpe_tokenizer._tokenize(text)
        if len(subword) != len(text):
            subword_sememes = []
            for tok in subword:
                if tok in dict_word2sememes:
                    semes = dict_word2sememes[tok]
                    semes = semes[:max_sememe_length]  # limit the length
                    subword_sememes.append(semes)
                else:
                    subword_sememes.append([])
        else:
            subword_sememes = get_sememes_flashtext(
                text,
                processor,
                dict_word2sememes,
                max_sememe_length=max_sememe_length
            )

    assert len(subword) == len(subword_sememes)
    return subword, subword_sememes


def get_subword_tokenize_and_sememes_single_sent(sent, bpe_tokenizer, processor, dict_word2sememes,
                                                 max_sememe_length=12):
    sent = zh_tokenize_single_sent(sent)
    sent_subword = []
    sent_subword_sememes = []

    for seg in sent:
        subword, subword_sememes = get_subword_tokenize_and_sememes(
            seg, bpe_tokenizer, processor, dict_word2sememes,
            max_sememe_length=max_sememe_length
        )
        sent_subword.extend(subword)
        sent_subword_sememes.extend(subword_sememes)

    assert len(sent_subword) == len(sent_subword_sememes)
    return sent_subword, sent_subword_sememes


def printable_text(text):
    """Returns text encoded in a way suitable for print or `tf.logging`."""

    # These functions want `str` for both Python2 and Python3, but in one case
    # it's a Unicode string and in the other it's a byte string.
    if six.PY3:
        if isinstance(text, str):
            return text
        elif isinstance(text, bytes):
            return six.ensure_text(text, "utf-8", "ignore")
        else:
            raise ValueError("Unsupported string type: %s" % (type(text)))
    elif six.PY2:
        if isinstance(text, str):
            return text
        elif isinstance(text, six.text_type):
            return six.ensure_binary(text, "utf-8")
        else:
            raise ValueError("Unsupported string type: %s" % (type(text)))
    else:
        raise ValueError("Not running on Python2 or Python 3?")


def sent_segmented2joined(segmented_sent):
    # non-chinese should not be joined together
    tokens = segmented_sent.split(" ")
    tokens = [w.strip() for w in tokens if len(w.strip()) > 0]

    sent_joined = ""
    for tok in tokens:
        # print(tok)
        # print(sent_joined)

        if len(sent_joined) == 0:
            sent_joined += tok

        else:
            if re.search("[\u4e00-\u9fa5]", tok[0]):
                sent_joined += tok
            else:
                if re.search("[\u4e00-\u9fa5]", sent_joined[-1]):
                    sent_joined += tok
                else:
                    sent_joined += " " + tok

    return sent_joined


def get_sememe_ids(sememes, dict_sememe2id):
    sem_ids = []
    for sem in sememes:
        sem_ids.append(dict_sememe2id[sem])

    return sem_ids



if __name__ == "__main__":
    sent = "我爱看美剧big bang, 和黄花苜蓿行尸走肉aaa. aaa"
    sent_new = zh_tokenize_single_sent(sent)
    print(sent_new)

    sent_new = " ".join(sent_new)
    print(sent_new)
    sent_new_joined = sent_segmented2joined(sent_new)
    print(sent_new_joined)



    dict_word2sememes = json.load(open("resources/dict_word2sememes.json", "r", encoding="utf-8"))
    bpe_tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
    processor = KeywordProcessor()
    processor.add_keywords_from_dict(
        json.load(open("resources/dict_hownet_flashtext.json", "r", encoding="utf-8"))
    )
    text = "捉住a"
    subword, subword_sememes = get_subword_tokenize_and_sememes(text, bpe_tokenizer, processor, dict_word2sememes)
    print(subword)
    print(subword_sememes)

    for _ in tqdm.tqdm(range(1)):
        sent = "学科建设"
        # sent = "数据库"
        sent_subword, sent_subword_sememes = get_subword_tokenize_and_sememes_single_sent(
            sent, bpe_tokenizer, processor, dict_word2sememes
        )
        print(sent_subword)
        print(sent_subword_sememes)
