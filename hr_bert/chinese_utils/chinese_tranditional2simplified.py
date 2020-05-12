
from hr_bert.chinese_utils.langconv import *


def traditional2simplified(sentence):
    '''
    将sentence中的繁体字转为简体字
    :param sentence: 待转换的句子
    :return: 将句子中繁体字转换为简体字之后的句子
    '''
    sentence = Converter('zh-hans').convert(sentence)
    return sentence


def simplified2traditional(sentence):
    sentence = Converter('zh-hant').convert(sentence)
    return sentence


if __name__=="__main__":
    # traditional_sentence = '憂郁的臺灣烏龜'
    traditional_sentence = '忧郁的台湾乌龟'
    simplified_sentence = traditional2simplified(traditional_sentence)
    print(simplified_sentence)

    '''
    输出结果：
        忧郁的台湾乌龟
    '''

    sentence = '忧郁的台湾乌龟'
    sentence = simplified2traditional(sentence)
    print(sentence)