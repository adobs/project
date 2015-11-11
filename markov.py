from model import db, connect_to_db
from random import choice

def get_input_text(orientation, gender, location, age, adjective_tuple):
    """Based on parameters, returns string of self summaries."""
        # (SELECT A.username FROM Adjectives AS A 
                    # WHERE A.Adjective IN :adjective_tuple
                    # AND A.username IN 
    text_string = ""

    QUERY = """SELECT P.self_summary from Profiles AS P
                WHERE P.age = :age AND P.location = :location AND P.username IN
            
                        (SELECT UO.username FROM Usernameorientations AS UO
                        WHERE UO.orientation=:orientation AND UO.username IN (
                            SELECT UG.username FROM Usernamegenders AS UG
                            WHERE UG.gender = :gender))
            """
    cursor = db.session.execute(QUERY, {"orientation": orientation, 
                                "gender": gender, "location": location, 
                                "age": age, "adjective_tuple": adjective_tuple})
    
    results = cursor.fetchall()
    print "results is", results
    for result in results:
        text =result[0].encode("utf8")
        # replace \n
        text = text.replace("\n", " ")
        print "text is", text
        text_string += text+" "

    return text_string

def make_chains(text_string, n):
    """Takes input text as string; returns dictionary of markov chains.

    Dictionary has tuple as values, lists of words as keys
    """

    chains = {}

    text_list = text_string.split()

    for i in range(len(text_list)-n+1):
        key = tuple(text_list[i:i+n])
        print type(key)
        chains[key] = chains.get(key, [])
        chains[key].extend(text_list[i+n:i+2*n])

    return chains

def make_text(chains):
    """Takes dictionary of markov chains and returns Markov-generated text.

    For a given tuple-key, one word from the value-list is added to the string of text"""

    list_of_text = []

    n_gram = choice(chains.keys())
    while n_gram[0][0].islower():
        n_gram = choice(chains.keys())
    
    list_of_text.extend(list(n_gram))


    print chains.keys()

    n = len(n_gram)

    while n_gram in chains:
        value = choice(chains[n_gram])
        list_of_text.append(value)
        print "list of text is", list_of_text
        n_gram = tuple(list_of_text[-1*n:])
        print "ngram is", n_gram

    text = (" ").join(list_of_text)

    return text

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.
    from flask_app import app
    # db.create_all()
    connect_to_db(app)
    print "Connected to DB."
    # queries()
