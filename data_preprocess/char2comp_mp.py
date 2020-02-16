# -*- coding: utf-8 -*-
import json
import sys
from pathlib import Path

import tqdm
from blingfire import text_to_sentences
import sys

sys.path.append("./")
from data_preprocess.char2comp import char2comp_file


def main():
    file_in = Path(sys.argv[1])
    file_out = Path(sys.argv[2])
    dict_char2comp_dir = Path(sys.argv[3])
    do_lower_case = int(sys.argv[4])

    print(f'Pre-processing {file_in} to {file_out}...')
    dict_char2comp = json.load(
        # open(dict_char2comp_dir, "r", encoding="utf-8")
        open(dict_char2comp_dir, "r")
    )
    char2comp_file(file_in, file_out, dict_char2comp=dict_char2comp, do_lower_case=do_lower_case)

    print(f'Successfully pre-processed {file_in} to {file_out}...')


if __name__ == '__main__':
    main()
