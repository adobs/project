from __future__ import generators
from okcupyd.session import Session
from okcupyd.json_search import SearchFetchable
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import nltk
# nltk.download()
import operator


db = SQLAlchemy()

def connect_to_db(app):
    """Connect to database."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///latlong.db'
    db.app = app
    db.init_app(app)


# from zipcodes table, get lat, long >> store this in a generator

def query_results(cursor):
    while True:
        results = cursor.fetchall()
        if not results:
            break
        for result in results:
            yield result

def querying():
    # why oh why does this have to go into a function for db to work??
    QUERY = """SELECT Zip, lattitude, longitude 
            FROM Latlong
            """
    cursor = db.session.execute(QUERY)
    generator = query_results(cursor)
    return generator

def inserting(zip_code, latitude, longitude, most_common_adjective, most_common_count):
    QUERY = """INSERT INTO Adjectives VALUES
        (:zip, :latitude, :longitude, :adjective, :count)
        """
    
    db.session.execute(QUERY, {"zip": zip_code, "latitude": latitude, "longitude": longitude, "adjective": most_common_adjective, "count": most_common_count})
    db.session.commit()

#i can call my function in interactive mode.  but if i do it normally, i get an error.  Why??


# for the zipcode in generator (ideally results is output from calling the function)
def searchOKC(generator):
# log into okCupid
    session = Session.login('adobsthecat', 'meow6996')
    for entry in generator:
        zip_code, latitude, longitude = entry

        searchable_profile = ""
        for profile in SearchFetchable(session=session, location=zip_code)[:500]:
            if profile.essays.self_summary:
                print profile
                searchable_profile += profile.essays.self_summary.lower()

        tokens = nltk.word_tokenize(searchable_profile)

        #tag words by word type (like adjective)
        tagged = nltk.pos_tag(tokens)

        adjectives = {}

        for word, speech_part in tagged:
            if speech_part == "ADJ" or speech_part == "JJ":
                adjectives[word] = adjectives.get(word, 0)
                adjectives[word] += 1

        sorted_adjectives = sorted(adjectives.items(), key=operator.itemgetter(1))

        most_common_adjective, most_common_count = sorted_adjectives[-1]

    # will have zip code, lat, long, adjective, and count >> Adjectives table
    inserting(zip_code,latitude,longitude,most_common_adjective,most_common_count)


if __name__ == "__main__":
    app = Flask(__name__)
    connect_to_db(app)
    db.session.close()