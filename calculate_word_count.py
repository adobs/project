import operator
def calculate_word_count(word_list):

    counting_dictionary = {}

    for word in word_list:
        counting_dictionary[word] = counting_dictionary.get(word, 0)
        counting_dictionary[word] += 1

    sorted_adjectives = sorted(counting_dictionary.items(), key=operator.itemgetter(1))

    most_common_adjective, most_common_count = sorted_adjectives[-1]

    return [most_common_adjective, most_common_count]