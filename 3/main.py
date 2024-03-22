import re
from collections import defaultdict

dictionary = defaultdict(list)


def intersection(list1, list2):
    temp = set(list2)
    list3 = [value for value in list1 if value in temp]
    return list3


def diff(list2):
    list1 = list(range(0, 100))
    temp = set(list2)
    list3 = [value for value in list1 if value not in temp]
    return list3


def form_dictionary():
    unique_tokens = []

    for i in range(100):
        with open(f'../2/lemmatized_tokens/{i}.txt', 'r',  encoding="utf-8") as file:
            words = file.read()
            words = re.split(r'[\s\n]', words)
            words.remove('')
            unique_tokens.append(set(words))
            for word in list(unique_tokens[i]):
                dictionary[word].append(i)

    for key in dict(sorted(dictionary.items())):
        with open('dictionary.txt', 'w',  encoding="utf-8") as file:
            file.write(f"{key}: {dictionary[key]}\n")

    return dictionary


def run(search, dictionary):
    search_conditions = search.split(' ')
    answer = search_conditions

    for i, element in enumerate(answer):
        if element not in ['|', '&', '!']:
            answer[i] = dictionary[answer[i]]

    while '!' in answer:
        index = answer.index('!') + 1
        answer[index] = diff(answer[index])
        answer.remove('!')

    while '&' in answer:
        index = answer.index('&') + 1
        answer[index] = intersection(answer[index - 2], answer[index])
        answer.remove('&')
        answer.pop(index-2)

    while '|' in answer:
        index = answer.index('|') + 1
        answer[index] = list(set(answer[index - 2] + answer[index]))
        answer.remove('|')
        answer.pop(index-2)

    return answer


if __name__ == '__main__':
    dictionary = form_dictionary()
    conditions = ['собрание & стругацкий | интервью', 'собрание | стругацкий | интервью',
                  'собрание & стругацкий & интервью', 'собрание & ! стругацкий | ! интервью',
                  'собрание | ! стругацкий | ! интервью']
    for cond in conditions:
        print(run(cond, dictionary))
