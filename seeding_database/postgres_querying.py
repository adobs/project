"""
postgres_querying.py

Intended for use with PostgreSQL database.  
NLTK library runs slow!  

Parses out adjectives and adds a list of adjectives used in the self-summary of
the profile to the database for a given profile.
"""


import os

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

from flask_sqlalchemy import SQLAlchemy
from model import Profile, Adjective, OldAdjective, db, connect_to_db
import nltk
nltk.download()


def queries():
    """ Adds adjectives used by different usernames to database

    Tags words in self-summary portions of profile. Adds a list of adjectives 
    that correspond with a given username to the database.
    """
    self_summary_list = db.session.query(Profile.username, Profile.self_summary).all()

    for username, self_summary in self_summary_list:
        adjectives = []
        self_summary = self_summary.replace('\n', ' ').replace('.',' ')

        tokens = nltk.word_tokenize(self_summary)
    
        # tag words by word type (like adjective)
        tagged = nltk.pos_tag(tokens)
        for word, speech_part in tagged:
            if (speech_part == "ADJ" or speech_part == "JJ") and speech_part != "i":
                adjectives.append(word.strip("\n\t1234567890!@#$%^&*()-=+{}[]/\\'\"<>?.,:;~`"))

        adjectives = list(set(adjectives))

        new_adjective = OldAdjective(username=username, adjectives=adjectives)

        db.session.add(new_adjective)
        db.session.commit()


if __name__ == "__main__":
    from flask_app import app
    connect_to_db(app)
    queries()
