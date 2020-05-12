


def del_all_flags(FLAGS):
    for keys in [keys for keys in FLAGS._flags()]:
        FLAGS.__delattr__(keys)

