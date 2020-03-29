import json


def csc_txt2json(from_dir, to_dir, mode="test"):

    f_in = open(from_dir, "r", encoding="utf-8")
    f_out = open(to_dir, "w", encoding="utf-8")

    for i, line in enumerate(f_in):
        # if i == 0:
        #     continue

        line = line.strip()
        if not line:
            continue

        line = line.split("\t")
        sentence1 = line[0].strip()
        sentence2 = line[1].strip()
        label = line[2].strip()

        json_ = {
            "label": label,
            "sentence1": sentence1,
            "sentence2": sentence2,
        }
        f_out.write(json.dumps(json_, ensure_ascii=False) + "\n")

    f_out.close()



if __name__ == "__main__":
    from_dir = "datasets/LCQMC/train.txt"
    to_dir = "datasets/LCQMC/train.json"
    csc_txt2json(from_dir, to_dir)

    from_dir = "datasets/LCQMC/dev.txt"
    to_dir = "datasets/LCQMC/dev.json"
    csc_txt2json(from_dir, to_dir)

    from_dir = "datasets/LCQMC/test.txt"
    to_dir = "datasets/LCQMC/test.json"
    csc_txt2json(from_dir, to_dir)
