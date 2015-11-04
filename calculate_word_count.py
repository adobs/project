import operator
def calculate_word_count(word_list):

    counting_dictionary = {}

    for adjective in word_list:
        counting_dictionary[adjective] = counting_dictionary.get(adjective, 0)
        counting_dictionary[adjective] += 1

    sorted_adjectives = sorted(counting_dictionary.items(), key=operator.itemgetter(1))

    most_common_adjective, most_common_count = sorted_adjectives[-1]

    return [most_common_adjective, most_common_count]