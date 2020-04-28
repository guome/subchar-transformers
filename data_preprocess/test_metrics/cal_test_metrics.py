import json

import numpy as np
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


def return_avg_mean_and_variance(list_metrics):
    return np.mean(list_metrics) * 100, np.std(list_metrics) * 100



if __name__ == "__main__":
    # for CHN
    # pred_tsv_dir = "data_preprocess/test_metrics/chn/picto_trans_finetune_chn_subchar_segmented_lower_subchar_segmented_lower_albert_tiny_7_submit_results.tsv"
    # truth_json_dir = "datasets/CLUE/chn/test.json"
    # accuracy, results = cal_metrics(pred_tsv_dir, truth_json_dir)
    # print(accuracy)

    # for LCQMC
    pred_tsv_dir = "data_preprocess/test_metrics/lcqmc/picto_trans_finetune_lcqmc_char_no_space_lower_char_no_space_lower_albert_tiny_10_submit_results.tsv"
    truth_json_dir = "datasets/CLUE/lcqmc/test.json"
    accuracy, results = cal_metrics(pred_tsv_dir, truth_json_dir)
    print(accuracy)
    #


    print(return_avg_mean_and_variance([0.77184,0.76504,0.76256,0.76448,0.7648,0.76784,0.77816,0.77112,0.76448, 0.77624]))



