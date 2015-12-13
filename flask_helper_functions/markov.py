"""
markov.py

Runs functions to operate the markov.html page.  Based on input parameters, 
functions called in succession will result in a corpus for a self-summary 
generated with Markov Chains.
"""

from model import db, connect_to_db
from random import choice


def get_input_text(orientation, gender, location, age_min, age_max, adjective_list, n):
    """ Based on parameters, returns string of self summaries."""
  
    text_string = ""


    QUERY = """SELECT P.self_summary from Profiles AS P
                WHERE P.age BETWEEN :age_min AND :age_max AND P.location = 
                    :location AND P.username IN
                        (SELECT UO.username FROM Usernameorientations AS UO
                         WHERE UO.orientation=:orientation AND UO.username IN 
                            (SELECT UG.username FROM Usernamegenders AS UG
                             WHERE UG.gender = :gender and UG.username IN
                                (SELECT A.username FROM Adjectives AS A 
                                 WHERE :adjective_one = A.adjective OR 
                                 :adjective_two = A.adjective OR 
                                 :adjective_three = A.adjective)))
            """
    
    cursor = db.session.execute(QUERY, {"orientation": orientation, 
                                "gender": gender, "location": location, 
                                "age_min": age_min, "age_max": age_max, 
                                "adjective_one": adjective_list[0], 
                                "adjective_two": adjective_list[1], 
                                "adjective_three": adjective_list[2]})
    
    results = cursor.fetchall()

    for result in results:
        text =result[0].encode("utf8")
        if text:
            text = text.replace("\n", " ")
            text_string += text+" "

    # checks to make sure there will be enough words available for the given n 
    if len(text_string.split(" ")) <= n + 1:
        return "invalid search results"
    else:
        return text_string


def make_chains(text_string, n):
    """ Takes input text as string; returns dictionary of markov chains.

    Dictionary has tuple as values, lists of words as keys
    """

    chains = {}

    text_list = text_string.split()

    for i in range(len(text_list)-n):
        key = tuple(text_list[i:i+n])
        chains[key] = chains.get(key, [])

        # slice text_list according to appropriate length as dictated by n
        chains[key].extend(text_list[i+n:i+2*n])

    return chains


def make_text(chains):
    """ Takes dictionary of markov chains and returns Markov-generated text.

    For a given tuple-key, one word from the value-list is added to the string of text
    """

    list_of_text = []

    n_gram = choice(chains.keys())

    # ensures that the first sentence starts with an Uppercase word
    while n_gram[0][0].islower():
        n_gram = choice(chains.keys())
    
    list_of_text.extend(list(n_gram))

    n = len(n_gram)

    while len(list_of_text)<200:
        if n_gram in chains:
            value = choice(chains[n_gram])
            list_of_text.append(value)

            # slices text_list corpus to create next n-gram key to search on
            n_gram = tuple(list_of_text[-1*n:])
        else:
            n_gram = choice(chains.keys())
            while n_gram[0][0].islower():
                n_gram = choice(chains.keys())

    # ensures that the markov text corpus finishes with punctuation
    while list_of_text[-1][-1] != ".":
        if n_gram in chains:
            value = choice(chains[n_gram])
            list_of_text.append(value)
            print "list of text is", list_of_text
            n_gram = tuple(list_of_text[-1*n:])
        else:
            n_gram = choice(chains.keys())
            while n_gram[0][0].islower():
                n_gram = choice(chains.keys())

    text = (" ").join(list_of_text)

    return text


if __name__ == "__main__":

    from flask_app import app
    connect_to_db(app)
    print "Connected to DB."
