# subchar-transformers
This repository holds the source codes for training and fine-tuning a Chinese pre-trained transformers with redesigned vocabulary. (C-TRANS: rethinking the vocab for pre-trained transformer models)

# Intro
Right now, from our observation, the main problem of applying BERT style transformer models is its model size, which is significantly affected by the vocab size. Even with distillation, one still face a model with 6m or more params, a half of which is the embedding. Thus, we wonder whether we can further reduce the vocab size of transformers, so that we can have a small model with 100-200 thousand params?

Now, if we deal with a word-to-sent Chinese trans model, we have the folowing ways to build the vocab: 

1) directly learn a BPE tokenizer on Chinese sents, and let the BPE to capture some common chinese words, like "拥有" (possess)

2) seperate each Chinese characters, which is what the original Bert does, then learn a BPE model to deal with other language inputs;

3) tokenize the chinese sents with a Chinese segmentation tool, like jieba, and then learn a BPE tokenizer;

One can introduce the subchar components of Chinese, which partially reflect the meaning of some chinese characters: 
  
4) on the raw sents, map each chinese char into its components, e.g. "糖" (sweet) becomes "⿰米⿸广⿱肀口", where symbols "⿰", "⿸", "⿱" indicates how the components are placed in a grid for Chinese characters, and "米", "广", "肀", "口" are components, and "" is the seperater (which should not appear in the corpus you use). A chinese sent "新型冠状病毒(2019-nCoV)" becomes "⿰⿱立朩斤⿱⿰⿱一廾刂土⿱冖⿺⿱一兀寸⿰丬犬⿸疒⿱一内⿱龶母(2019-nCoV)". Then learn BPE;

5) seperate each Chinese characters， and then map each chinese char into its components, then learn BPE;

6) tokenize the chinese sents with jieba, and then map each chinese char into its components, then learn BPE;


If we think about some of the work done with character embedding in English, one can think of a hierachical transformer architecture, where we first encode the components of Chinese into a component level transformer, get the CLS hidden state, which is hidden state for the character / word, which then will be feed into a higher-level transformer net. 

Note this idea also works for English language. This idea can significantly reduce transformer vocab to hundreds, which makes a 100-200 thousand parameter model possible. 



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

  - on Iflytek (albert-tiny):
  
| model | vocab size |  max_seq_length | lr | batch_size | warmup-steps | dev | test |
| :----:| :----: | :----: | :----: |:----: |:----: | :----: | :----: | 
| char_no_space_lower	| 5000 | 128| 2e-5 | 32 | 400 |  0.439015, 0.43362832, 0.4432474, 0.4474798, 0.4328588 |  -  |
|  char_spaced_lower | 5000 | 128| 2e-5 | 32 | 400 | 0.4263178, 0.42285493, 0.44093883, 0.43516737, 0.43401307  |  -  |
|  char_segmented_lower | 5000 | 128| 2e-5 | 32 | 400 |  , , , ,   |  -  |
|  subchar_no_space_lower | 5000 | 128| 2e-5 | 32 | 400 | 0.36898807, 0.37860715, 0.3678338, 0.37629858 |  -   |
|  subchar_spaced_lower | 5000 | 128| 2e-5 | 32 | 400 | 0.35244325, 0.35244325, 0.37437475, 0.3759138, 0.3643709 |  -   |
|  subchar_segmented_lower | 5000 | 128| 2e-5 | 32 | 400 |  , , , , |   -   |


## effects of vocab size
| model | vocab size |  max_seq_length | lr | batch_size | warmup-steps | dev | test |
| :----:| :----: | :----: | :----: |:----: |:----: | :----: | :----: | 
| Picto-Albert-mini	| 2500 | 128| 2e-5 | 32 | 400 |  - |  -  |
| Picto-Albert-mini	| 5000 | 128| 2e-5 | 32 | 400 |  - |  -  |
| Picto-Albert-mini	| 10000 | 128| 2e-5 | 32 | 400 |  - |  -  |
| Picto-Albert-mini	| 15000 | 128| 2e-5 | 32 | 400 |  - |  -  |
| Picto-Albert-mini	| 20000 | 128| 2e-5 | 32 | 400 |  - |  -  |
| Picto-Albert-mini	| 30000 | 128| 2e-5 | 32 | 400 |  - |  -  |


## effects of model size
| model | vocab size |  max_seq_length | lr | batch_size | warmup-steps | dev | test |
| :----:| :----: | :----: | :----: |:----: |:----: | :----: | :----: | 
| Picto-Albert-tiny (3-layer)	| 5000 | 128| 2e-5 | 32 | 400 |  - |  -  |
| Picto-Albert-mini (6-layer)	| 5000 | 128| 2e-5 | 32 | 400 |  - |  -  |
| Picto-Albert-Base (12-layer)	| 5000 | 128| 2e-5 | 32 | 400 |  - |  -  |
| Picto-Albert-Large (24-layer)	| 5000 | 128| 2e-5 | 32 | 400 |  - |  -  |


## contributors

 - [michael-wzhu](https://github.com/michael-wzhu)
