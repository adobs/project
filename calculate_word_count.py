import operator
def calculate_word_count(adjective_list):
    #list is a list of tuples
    word_list = []
    for adjectives in adjective_list:
        word_list.extend(adjectives[0])

    counting_dictionary = {}

    for word in word_list:
        counting_dictionary[word] = counting_dictionary.get(word, 0)
        counting_dictionary[word] += 1

    sorted_adjectives = sorted(counting_dictionary.items(), key=operator.itemgetter(1))

    most_common_adjective, most_common_count = sorted_adjectives[-1]

    return [most_common_adjective, most_common_count]