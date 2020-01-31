# subchar-transformers
This repository holds the source codes for training and fine-tuning a Chinese pre-trained transformers with sub-character features.


## data preparation

这里假设预训练预料已经按照bert的格式准备好

 - 汉字拆开
    - [汉字与偏旁部首的映射表](https://github.com/HKUST-KnowComp/JWE/blob/master/subcharacter/char2comp.txt)
    - 将汉字拆为偏旁部首
        - e.g., "糖" 会变为 "米广肀口";
    - 现在每个汉字相当于英文中的一个词，其左右也用空格隔开
       - e.g., "新型冠状病毒(2019-nCoV)" 拆为 " 立木斤  开刂土  冖二儿寸  丬犬  疒丙  母 (2019-nCoV)"
    - 将non-chinese部分，用标注tokenizer拆分处理(e.g., blingfire), 且去除多余空格
       - e.g. "立木斤 开刂土 冖二儿寸 丬犬 疒丙 母 ( 2019 - nCoV )"

    - 训练byte-level BPE tokenizer, 作为预训练模型的tokenizer
        - python data_preprocess/build_bpe.py
     
    - 将语料做bpe tokenize

## pretraining

## downstream task