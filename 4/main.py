import math
from collections import defaultdict
from typing import Iterable

import pandas as pd


def get_words_list_by_id(id: int) -> dict:
    id_to_words_list = {}
    for i in range(id):
        with open(f"../2/lemmatized_tokens/{i}.txt", "r", encoding="utf-8") as file:
            id_to_words_list[i] = file.read().split()
    return id_to_words_list


def get_words_set_by_id(id: int) -> dict:
    id_to_words_set = {}
    for i in range(id):
        with open(f"../2/lemmatized_tokens/{i}.txt", "r", encoding="utf-8") as file:
            id_to_words_set[i] = set(file.read().split())
    return id_to_words_set


def get_doc_ids_by_word(id_to_words: dict[int, Iterable]):
    inverted_index = defaultdict(set)
    for doc_id, words in id_to_words.items():
        for word in words:
            inverted_index[word].add(doc_id)
    return inverted_index


def get_idfs(id_to_words, n):
    inverted_index = get_doc_ids_by_word(id_to_words)
    words = []
    idfs = []
    for word, ids in inverted_index.items():
        words.append(word)
        idfs.append(math.log2(n/len(ids)))
    return words, idfs


def main():
    n = 100
    id_to_words = get_words_list_by_id(n)
    words, idfs = get_idfs(id_to_words, n)
    idf_dict = {"Term": words, "IDF": [round(x, 6) for x in idfs]}

    tf_dict = {"Term": words}
    tfidf_dict = {"Term": words}
    for id, wordlist in id_to_words.items():
        tfs = []
        for w in words:
            tf = wordlist.count(w) / max(1, len(wordlist))
            tfs.append(tf)
        tf_dict[id] = [round(x, 6) for x in tfs]
        tfidf_dict[id] = [round(x*y, 6) for x, y in zip(tfs, idfs)]

    pd.DataFrame.from_dict(tf_dict).to_csv(f"./tfidf_tables/tf.csv", sep=",", index=False)
    pd.DataFrame.from_dict(idf_dict).to_csv(f"./tfidf_tables/idf.csv", sep=",", index=False)
    pd.DataFrame.from_dict(tfidf_dict).to_csv(f"./tfidf_tables/tfidf.csv", sep=",", index=False)


if __name__ == "__main__":
    main()
