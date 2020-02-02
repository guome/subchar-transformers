# -*- coding: UTF-8 -*-

from tokenizers import (ByteLevelBPETokenizer,
                            BPETokenizer,
                            SentencePieceBPETokenizer,
                            BertWordPieceTokenizer)


if __name__ == "__main__":
    tokenizer_name = "zh_example"
    # tokenizer = ByteLevelBPETokenizer()
    # tokenizer = BertWordPieceTokenizer(
    #     handle_chinese_chars=False,
    # )
    tokenizer = SentencePieceBPETokenizer()

    tokenizer.train(
        [
            "datasets/examples/corpus_zh_example_subchar_0.txt"
        ],
        vocab_size=950,
        min_frequency=1,

    )
    tokenizer.save("resources/tokenizer", tokenizer_name)

    ####################
    # tryout the trained model
    ####################
    # Initialize a tokenizer
    # vocab = "./resources/tokenizer/zh_example-vocab.txt"
    vocab = "./resources/tokenizer/zh_example-vocab.json"
    merges = "./resources/tokenizer/zh_example-merges.txt"
    # tokenizer = ByteLevelBPETokenizer(vocab, merges)
    # tokenizer = BPETokenizer(vocab, merges)
    # tokenizer = BertWordPieceTokenizer(vocab, handle_chinese_chars=False)
    tokenizer = SentencePieceBPETokenizer(
        vocab,
        merges,

    )

    # And then encode:
    # encoded = tokenizer.encode("南京老城“路在何方”？")
    # encoded = tokenizer.encode("立木斤 开刂土 冖二儿寸 丬犬 疒丙 母 ( 2019 - nCoV )")
    encoded = tokenizer.encode("丰月 勹丶勹山 乛头 戶方 月邑 占火 金戋 者邑 句多 乛头 一冂丨人人 木东 另刀 野土 乛亅 ")
    print(encoded.ids)
    print(encoded.tokens)


