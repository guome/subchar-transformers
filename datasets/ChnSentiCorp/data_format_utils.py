import json


def csc_tsv2json(from_dir, to_dir, mode="test"):

    f_in = open(from_dir, "r", encoding="utf-8")
    f_out = open(to_dir, "w", encoding="utf-8")

    for i, line in enumerate(f_in):
        if i == 0:
            continue

        line = line.strip()
        if not line:
            continue

        line = line.split("\t")
        label = line[0].strip()
        sentence = line[1].strip()

        json_ = {
            "label": label,
            "sentence": sentence
        }
        f_out.write(json.dumps(json_, ensure_ascii=False) + "\n")

    f_out.close()



if __name__ == "__main__":
    from_dir = "datasets/ChnSentiCorp/train.tsv"
    to_dir = "datasets/ChnSentiCorp/train.json"
    csc_tsv2json(from_dir, to_dir)

    from_dir = "datasets/ChnSentiCorp/dev.tsv"
    to_dir = "datasets/ChnSentiCorp/dev.json"
    csc_tsv2json(from_dir, to_dir)

    from_dir = "datasets/ChnSentiCorp/test.tsv"
    to_dir = "datasets/ChnSentiCorp/test.json"
    csc_tsv2json(from_dir, to_dir)
