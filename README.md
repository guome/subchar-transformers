# subchar-transformers
This repository holds the source codes for training and fine-tuning a Chinese pre-trained transformers with sub-character features.

# Acknowledgement
Research supported with Cloud TPUs from Google's TensorFlow Research Cloud ([TFRC](https://www.tensorflow.org/tfrc))

## data preparation

这里假设预训练预料已经按照bert的格式准备好

 - 汉字拆开
    - [拆字表](https://github.com/kfcd/chaizi/blob/master/chaizi-jt.txt)
    
    - split chinese characters into their components (将汉字拆为偏旁部首) 
        - e.g., "糖" 会变为 "米广肀口";
        - python data_preprocess/char2comp.py
    - now every chinese characters are similar to a word in English, and are seperated by blank spaces (现在每个汉字相当于英文中的一个词，其左右也用空格隔开)
       - e.g., "新型冠状病毒(2019-nCoV)" are splitted into " 立木斤  开刂土  冖二儿寸  丬犬  疒丙  母 (2019-nCoV)"
    - non-chinese parts are tokenized by, for example, jieba, etc; (将non-chinese部分，用tokenizer拆分处理(e.g., jieba, blingfire), 且去除多余空格)
       - e.g. "立木斤 开刂土 冖二儿寸 丬犬 疒丙 母 ( 2019 - nCoV )"

    - train a bpe tokenizer, which will be the tokenizer for pretrained models(训练byte-level BPE tokenizer, 作为预训练模型的tokenizer)
        - python data_preprocess/build_bpe.py
     
    - tokenize the corpus
 
 - 多进程版
    - 将预料文件拆为多份
        - e.g., "datasets/examples/corpus_zh_example_0.txt" 拆为 "datasets/examples/corpus_zh_example_0_${i}.txt", 拆分时设置每个文件包含 NUM=6 个documents： 
        - python data_preprocess/split_file_utils.py
    
    - 对每个拆分的文件同时进行拆字预处理
        - data_preprocess/char2comp_mp.sh
        - 设置脚本中的进程数，文件路径等
        - e.g., 处理完后的文件路径格式为 ./datasets/examples/corpus_zh_example_0_${i}_subchar.txt
    
    - 将预处理完的文件合并(optional)
        - python data_preprocess/merge_file_utils.py 

## pretraining

  - Phase 1. Train on ZH-WIKI corpus (1.2G)
    - preprocess of zh-wiki: (a) extract; (b) split sentence based punctuations; (c) split char into compositions;
    - vocab size for subchar-transformers: 5000;
    - pretrained model: albert-base
    - comparison: for strict and fair comparison, we also train a normal model based on chinese chars, whose vocab size is 15000.
    
    - sent_length: all the models are trained with length 512;
    
## downstream tasks

  - on Iflytek:
  
| model | vocab size |  max_seq_length | lr | batch_size | warmup-steps | dev | test |
| :----:| :----: | :----: | :----: |:----: |:----: | :----: | :----: | 
| Picto-Albert-mini	| 5000 | 128| 2e-5 | 32 | 400 |  - |  -  |
|  - w/o word tokenization | 5000 | 128| 2e-5 | 32 | 400 | - |  -  |
|  - w/o subchar | 5000 | 128| 2e-5 | 32 | 400 | - |  -   |
|  - w/o both | 5000 | 128| 2e-5 | 32 | 400 | - |  -   |


## effects of vocab size
| model | vocab size |  max_seq_length | lr | batch_size | warmup-steps | dev | test |
| :----:| :----: | :----: | :----: |:----: |:----: | :----: | :----: | 
| Picto-Albert-Base	| 2500 | 128| 2e-5 | 32 | 400 |  - |  -  |
| Picto-Albert-Base	| 5000 | 128| 2e-5 | 32 | 400 |  - |  -  |
| Picto-Albert-Base	| 10000 | 128| 2e-5 | 32 | 400 |  - |  -  |
| Picto-Albert-Base	| 15000 | 128| 2e-5 | 32 | 400 |  - |  -  |
| Picto-Albert-Base	| 20000 | 128| 2e-5 | 32 | 400 |  - |  -  |
| Picto-Albert-Base	| 30000 | 128| 2e-5 | 32 | 400 |  - |  -  |


## effects of model size
| model | vocab size |  max_seq_length | lr | batch_size | warmup-steps | dev | test |
| :----:| :----: | :----: | :----: |:----: |:----: | :----: | :----: | 
| Picto-Albert-tiny	| 5000 | 128| 2e-5 | 32 | 400 |  - |  -  |
| Picto-Albert-mini	| 5000 | 128| 2e-5 | 32 | 400 |  - |  -  |
| Picto-Albert-Base	| 5000 | 128| 2e-5 | 32 | 400 |  - |  -  |
| Picto-Albert-Large	| 5000 | 128| 2e-5 | 32 | 400 |  - |  -  |


## contributors

 - [michael-wzhu](https://github.com/michael-wzhu)
