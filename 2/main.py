import pymorphy2
from nltk.corpus import stopwords
import re
import os


morph = pymorphy2.MorphAnalyzer()


def get_lemma(word):
    return morph.parse(word)[0].normal_form


def delete_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f'Ошибка при удалении файла {file_path}. {e}')


def get_stop_words():
    with open('stop_words.txt', 'r', encoding="utf-8") as file:
        stop_words = file.read()
        stop_words = set(re.split(r'[\s\n]', stop_words))
        stop_words.union(stopwords.words('russian'))

    return stop_words


def tokenize(text):
    tokens = ['']
    idx = 0
    for j in text:
        if re.fullmatch(r'\n', j):
            idx += 2
            tokens.append('1')
            tokens.append('')
        elif re.fullmatch(r'\s', j):
            idx += 2
            tokens.append('2')
            tokens.append('')
        elif j == '-':
            if re.fullmatch(r'\s', text[text.index(j) - 1]):
                pass
            elif re.fullmatch(r'\s', text[text.index(j) + 1]):
                idx += 1
                tokens.append('')
        elif not re.fullmatch(r'[А-Яа-я]', j):
            continue
        else:
            tokens[idx] += j

    return tokens


if __name__ == '__main__':
    delete_files_in_folder('lemmatized_tokens/')

    stop_words = get_stop_words()

    for i in range(0, 100):
        with open(f'../1/pages/file_{i}', 'r', encoding="utf-8") as file:
            text = file.read()
            tokens = tokenize(text)

            with open(f'lemmatized_tokens/{i}.txt', 'w', encoding="utf-8") as page:
                for word in tokens:
                    if word:
                        word = get_lemma(word).lower()
                        if word not in stop_words and word not in ['1', '2']:
                            page.write(f'{word}')
                        if word == '1':
                            page.write('\n')
                        if word == '2':
                            page.write(' ')