import json


def load_from_json(json_dir):
    with open(json_dir, "r", encoding="utf-8") as f:
        iterable = json.load(f)
    return iterable


def dump_to_json(iterable, json_dir):
    with open(json_dir, "w", encoding="utf-8") as f:
        json.dump(iterable, f, ensure_ascii=False)


