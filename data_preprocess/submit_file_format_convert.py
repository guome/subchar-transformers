import json

import sys
sys.path.append("./")


def submit_tsv2jsonl(tsv_dir, jsonl_dir):

    f_in = open(tsv_dir, "r", encoding="utf-8")
    f_out = open(jsonl_dir, "w", encoding="utf-8")

    for i, line in enumerate(f_in):
        if i == 0:
            continue

        idx, pred = line.strip().split("\t")

        samp = {
            "id": int(idx), "label": str(pred)
        }
        samp = json.dumps(samp, ensure_ascii=False)
        f_out.write(samp + "\n")

    f_out.close()


if __name__ == "__main__":
    tsv_dir = "data_preprocess/tmp/experiments_subchar_transformers_albert_base_128_iflytek_20200305-053807_submit_results.tsv"
    jsonl_dir = "data_preprocess/tmp/iflytek_predict.json"
    submit_tsv2jsonl(tsv_dir, jsonl_dir)

