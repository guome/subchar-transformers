# -*- coding: UTF-8 -*-

import sentencepiece as spm

import sys
sys.path.append("./")


if __name__ == "__main__":

    for vocab_size in [5000, 7500, 15000, 30000]:

        spm.SentencePieceTrainer.train('--input=./corpus/subchar_lower/zhwiki-latest-pages-articles_subchar_lower.txt --model_prefix=%d-clean --vocab_size=%d --pad_id=0 --unk_id=1 --eos_id=-1 --bos_id=-1 --control_symbols=[CLS],[SEP],[MASK] --user_defined_symbols=(,),”,-,.,–,£,€ --shuffle_input_sentence=true --input_sentence_size=30000000 --character_coverage=0.99995 --model_type=bpe' % (vocab_size, vocab_size))
