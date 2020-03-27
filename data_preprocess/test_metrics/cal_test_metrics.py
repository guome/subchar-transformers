import json

from sklearn.metrics import classification_report


def get_truth_labels(from_json_dir):

    truth_labels = []
    with open(from_json_dir, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):

            line = line.strip()
            line = json.loads(line)
            truth_labels.append(int(line["label"]))

    return truth_labels


def get_pred_labels(from_tsv_dir):
    pred_labels = []
    with open(from_tsv_dir, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):

            if i == 0:
                continue

            line = line.strip()
            line = line.split("\t")
            label_ = line[-1]
            pred_labels.append(int(label_))

    return pred_labels


def cal_acc(truth_labels, pred_labels):
    count = 0
    assert len(truth_labels) == len(pred_labels)
    for true, pred in zip(truth_labels, pred_labels):
        if true == pred:
            count += 1

    return count / len(truth_labels)


def cal_metrics(pred_tsv_dir, truth_json_dir):
    truth_labels = get_truth_labels(truth_json_dir)
    pred_labels = get_pred_labels(pred_tsv_dir)

    results = classification_report(truth_labels, pred_labels, output_dict=True)
    accuracy = cal_acc(truth_labels, pred_labels)

    print(results)

    return accuracy, results


if __name__ == "__main__":
    pred_tsv_dir = "data_preprocess/test_metrics/chn/data_picto_trans_finetune_chn_subchar_spaced_lower_subchar_spaced_lower_albert_tiny_5_submit_results.tsv"
    truth_json_dir = "datasets/CLUE/chn/test.json"
    accuracy, results = cal_metrics(pred_tsv_dir, truth_json_dir)
    print(accuracy)


