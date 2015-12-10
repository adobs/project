import os

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

from flask_sqlalchemy import SQLAlchemy
from model import Profile, Adjective, OldAdjective, db, connect_to_db
import nltk
nltk.download()
# import operator
# import geocoder
#
def queries():
    """Per a given location, add the most most common adjective to a database

    Makes a list out of all the locations listed in the database.
    For each location, turns all the self summaries into """
    self_summary_list = db.session.query(Profile.username, Profile.self_summary).all()

    for username, self_summary in self_summary_list:
        adjectives = []
        self_summary = self_summary.replace('\n', ' ').replace('.',' ')

        tokens = nltk.word_tokenize(self_summary)
    
    ############CONSIDER ADDING IN NOUNS

        
        # tag words by word type (like adjective)
        tagged = nltk.pos_tag(tokens)
        print tagged
        for word, speech_part in tagged:
            if (speech_part == "ADJ" or speech_part == "JJ") and speech_part != "i":
                adjectives.append(word.strip("\n\t1234567890!@#$%^&*()-=+{}[]/\\'\"<>?.,:;~`"))
                print "#########WORD IS", word

        adjectives = list(set(adjectives))

        new_adjective = OldAdjective(username=username, adjectives=adjectives)

        db.session.add(new_adjective)
        db.session.commit()

# def convert_into_unique():

#     words = db.session.query(Adjective).all()

#     for word in words:
#         word.adjectives = list(set(word.adjectives)) 
#         db.session.commit()


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.
    from flask_app import app
    # db.create_all()
    connect_to_db(app)
    print "Connected to DB."
    queries()
