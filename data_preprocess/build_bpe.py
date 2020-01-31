# -*- coding: UTF-8 -*-

from tokenizers import (ByteLevelBPETokenizer,
                            BPETokenizer,
                            SentencePieceBPETokenizer,
                            BertWordPieceTokenizer)


if __name__ == "__main__":
    tokenizer_name = "zh_example"
    tokenizer = ByteLevelBPETokenizer()
    tokenizer.train(
        [
            "datasets/examples/corpus_zh_example_subchar_0.txt"
        ],
        vocab_size=500
    )
    tokenizer.save("resources/tokenizer", tokenizer_name)

    ####################
    # tryout the trained model
    ####################
    # Initialize a tokenizer
    vocab = "./resources/tokenizer/zh_example-vocab.json"
    merges = "./resources/tokenizer/zh_example-merges.txt"
    tokenizer = ByteLevelBPETokenizer(vocab, merges)
    # tokenizer = BPETokenizer(vocab, merges)

    # And then encode:
    # encoded = tokenizer.encode("南京老城“路在何方”？")
    encoded = tokenizer.encode("立木斤 开刂土 冖二儿寸 丬犬 疒丙 母 ( 2019 - nCoV )")
    print(encoded.ids)
    print(encoded.tokens)


