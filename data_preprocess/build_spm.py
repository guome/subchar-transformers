# -*- coding: UTF-8 -*-
import os

import sentencepiece as spm

import sys
sys.path.append("./")


if __name__ == "__main__":
    STORAGE_BUCKET = "gs://sbt0"
    input_dir = os.path.join(
        STORAGE_BUCKET,
        "data/corpus/char_lower/zhwiki-latest-pages-articles_char_lower.txt"
    )

    for vocab_size in [5000, 10000]:

        spm.SentencePieceTrainer.train('--input=%s --model_prefix=./resources/tokenizer/char-%d-clean --vocab_size=%d --pad_id=0 --unk_id=1 --eos_id=-1 --bos_id=-1 --control_symbols=[CLS],[SEP],[MASK] --user_defined_symbols=(,),”,-,.,–,£,€ --shuffle_input_sentence=true --input_sentence_size=30000000 --character_coverage=0.99995 --model_type=bpe' % (input_dir, vocab_size, vocab_size))

        # spm.SentencePieceTrainer.train('--input=./corpus/subchar_lower/zhwiki-latest-pages-articles_100_subchar_lower.txt --model_prefix=./resources/tokenizer/%d-clean --vocab_size=%d --pad_id=0 --unk_id=1 --eos_id=-1 --bos_id=-1 --control_symbols=[CLS],[SEP],[MASK] --user_defined_symbols=(,),”,-,.,–,£,€ --shuffle_input_sentence=true --input_sentence_size=30000000 --character_coverage=0.99995 --model_type=bpe' % (vocab_size, vocab_size))

