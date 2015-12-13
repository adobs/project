"""
seed_adjective_table.py

Based on entries in the oldadjectives table that has an array as a field type, 
inputs adjectives and usernames into the adjectives table.
"""

import os

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

from model import Adjective, OldAdjective, db, connect_to_db


def seed_adjective_table():
    """ Iterates through each OldAdjective object to populate adjectives table

    Input is a row from the oldadjectives table which has a username in one 
    column and an array of adjectives in another.  The adjectives table has a 
    row for each adjective, with each row containing the username and an 
    adjective.
    """

    adjectives = db.session.query(OldAdjective.username, OldAdjective.adjectives).all()

    for username, adjective_list in adjectives:
        for adjective in adjective_list:
            new_entry = Adjective(username=username, adjective=adjective)
            db.session.add(new_entry)
            db.session.commit()


if __name__ == "__main__":
    from flask_app import app
    connect_to_db(app)
    db.create_all()
    seed_adjective_table()
