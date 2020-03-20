# -*- coding: UTF-8 -*-
import os

import sentencepiece as spm
import tensorflow.compat.v1 as tf

import sys
sys.path.append("./")


if __name__ == "__main__":
    # STORAGE_BUCKET = "gs://sbt0"
    # input_dir_gs = os.path.join(
    #     STORAGE_BUCKET,
    #     "data/corpus/char_lower/zhwiki-latest-pages-articles_char_lower.txt"
    # )
    # input_dir_local = "./zhwiki-latest-pages-articles_char_lower.txt"
    # tf.gfile.Copy(input_dir_gs, input_dir_local, overwrite=True)
    #
    #
    # for vocab_size in [15000]:
    #
    #     spm.SentencePieceTrainer.train('--input=zhwiki-latest-pages-articles_char_lower.txt --model_prefix=./resources/tokenizer/char-%d-clean --vocab_size=%d --pad_id=0 --unk_id=1 --eos_id=-1 --bos_id=-1 --control_symbols=[CLS],[SEP],[MASK] --user_defined_symbols=(,),”,-,.,–,£,€ --shuffle_input_sentence=true --input_sentence_size=30000000 --character_coverage=0.99995 --model_type=bpe' % (vocab_size, vocab_size))

    vocab_sizes = [2500, 5000, 10000, 15000, 20000, 25000, 30000]
    prefixes = [
        "char_spaced_lower",
        "char_no_space_lower",
        "subchar_spaced_lower",
        "subchar_no_space_lower",
    ]

    STORAGE_BUCKET = "gs://sbt0"

    for vocab_size in vocab_sizes:
        for prefix in prefixes:

            input_dir_gs = os.path.join(
                STORAGE_BUCKET,
                "data/corpus/%s/zhwiki-latest-pages-articles_%s.txt" % (prefix, prefix)
            )
            input_dir_local = "./zhwiki-latest-pages-articles_%s.txt" % prefix
            tf.gfile.Copy(input_dir_gs, input_dir_local, overwrite=True)

            try:
                spm.SentencePieceTrainer.train(
                    '--input=zhwiki-latest-pages-articles_%s.txt --model_prefix=./resources/tokenizer/%s-%d-clean --vocab_size=%d --pad_id=0 --unk_id=1 --eos_id=-1 --bos_id=-1 --control_symbols=[CLS],[SEP],[MASK] --user_defined_symbols=(,),”,-,.,–,£,€ --shuffle_input_sentence=true --input_sentence_size=30000000 --model_type=bpe' % (
                    prefix, prefix, vocab_size, vocab_size)
                )

            except Exception as e:
                print(e)
                try:
                    spm.SentencePieceTrainer.train(
                        '--input=zhwiki-latest-pages-articles_%s.txt --model_prefix=./resources/tokenizer/%s-%d-clean --vocab_size=%d --pad_id=0 --unk_id=1 --eos_id=-1 --bos_id=-1 --control_symbols=[CLS],[SEP],[MASK] --user_defined_symbols=(,),”,-,.,–,£,€ --shuffle_input_sentence=true --input_sentence_size=30000000 --model_type=bpe --character_coverage=0.98' % (
                            prefix, prefix, vocab_size, vocab_size)
                    )

                except Exception as e:
                    print(e)

