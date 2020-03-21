# -*- coding: UTF-8 -*-
import os
import random

import sentencepiece as spm
import tensorflow.compat.v1 as tf

import sys

import tqdm

sys.path.append("./")

indices = list(range(int(1e+7)))
random.shuffle(indices)
indices = indices[: int(3e+6)]
indices = {w: 1 for w in indices}


def sample_corpus(corpus_orig_dir, to_dir):

    with open(corpus_orig_dir, "r", encoding="utf-8") as f_in:
        with open(to_dir, "w", encoding="utf-8") as f_out:
            for i, line in tqdm.tqdm(enumerate(f_in)):
                if i not in indices:
                    continue

                f_out.write(line)


if __name__ == "__main__":
    prefixes = [
        "char_spaced_lower",
        "char_no_space_lower",
        "subchar_spaced_lower",
        "subchar_no_space_lower",
    ]

    STORAGE_BUCKET = "gs://sbt0"

    for prefix in prefixes:
        input_dir_gs = os.path.join(
            STORAGE_BUCKET,
            "data/corpus/%s/zhwiki-latest-pages-articles_%s.txt" % (prefix, prefix)
        )
        input_dir_local = "./zhwiki-latest-pages-articles_%s.txt" % prefix
        tf.gfile.Copy(input_dir_gs, input_dir_local, overwrite=True)

        input_dir_local_small = "./zhwiki-latest-pages-articles_%s_small.txt" % prefix
        sample_corpus(input_dir_local, input_dir_local_small)