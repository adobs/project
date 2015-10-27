from flask_sqlalchemy import SQLAlchemy
from model import Profile, Adjective, db, connect_to_db
import nltk
# nltk.download()
import operator
import geocoder

#
def queries():
    """Per a given location, add the most most common adjective to a database

    Makes a list out of all the locations listed in the database.
    For each location, turns all the self summaries into """
    location_list = db.session.query(Profile.location).group_by(Profile.location).all()

    for location in location_list:
        adjectives = {}
        self_summary_string = ""
        self_summary_list = db.session.query(Profile.self_summary).filter(Profile.location == location[0]).all()
        
        for summary in self_summary_list:
            if summary[0]:
                self_summary_string += summary[0]

        self_summary_string = self_summary_string.replace('\n', ' ').replace('.',' ')

        tokens = nltk.word_tokenize(self_summary_string)
        
        # tag words by word type (like adjective)
        tagged = nltk.pos_tag(tokens)

        for word, speech_part in tagged:
            if speech_part == "ADJ" or speech_part == "JJ" and speech_part != "i":
                adjectives[word] = adjectives.get(word, 0)
                adjectives[word] += 1

        sorted_adjectives = sorted(adjectives.items(), key=operator.itemgetter(1))
        
        if sorted_adjectives:
            most_common_adjective, most_common_count = sorted_adjectives[-1]

        lat_long = geocoder.google(location[0])
        latitude, longitude = lat_long.latlng
        
        new_adjective = Adjective(location=location[0], latitude=latitude, longitude=longitude, adjective=most_common_adjective, count=most_common_count)

        db.session.add(new_adjective)
        db.session.commit()


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.
    from flask_app import app
    # db.create_all()
    connect_to_db(app)
    print "Connected to DB."
    queries()
