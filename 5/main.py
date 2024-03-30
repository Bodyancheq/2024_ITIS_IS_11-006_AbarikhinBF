import numpy as np
import pandas as pd
import typer


def load_tfidf(filename):
    return pd.read_csv(filename)


def get_sums_for_tokens(tfidf_table, tokens: list[str]) -> list:
    return tfidf_table.loc[tfidf_table['Term'].isin(tokens)].drop('Term', axis=1).sum().to_numpy()


def search(tfidf_table, tokens: list[str]) -> list:
    sums = get_sums_for_tokens(tfidf_table, tokens)
    indexed_sums = [(i, s) for i, s in enumerate(sums)]
    indexed_sums.sort(key=lambda x: -x[1])

    return indexed_sums


def main(args: list[str]):
    if len(args) == 0:
        print("Введите хотя бы одно ключевое слово")
        return

    tdidf_table = load_tfidf("../4/tfidf_tables/tfidf.csv")
    results = search(tdidf_table, args)

    res_msg = f"Query: {' '.join(args)}\n\n" + "Search results:\n" + "\n".join(f"Документ {doc[0]} - {doc[1]}" for doc in results[:15])
    with open("search_results.txt", "w", encoding="utf-8") as file:
        file.write(res_msg)
        print(res_msg)


if __name__ == '__main__':
    typer.run(main)
