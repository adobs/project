from flask_sqlalchemy import SQLAlchemy
from model import Profile, Essay, Adjective, db, connect_to_db
import nltk
# nltk.download()
import operator


#
def queries():
    location_list = db.session.query(Profile.location).group_by(Profile.location).all()
    print location_list


    for location in location_list:
        adjectives = {}
        self_summary_list = db.session.query(Essay.self_summary).join(Profile).filter(Profile.location == location).all()
        self_summary_string = (" ").join(self_summary_list)

        print self_summary_string

        tokens = nltk.word_tokenize(self_summary_string)
        #tag words by word type (like adjective)
        tagged = nltk.pos_tag(tokens)

        for word, speech_part in tagged:
            if speech_part == "ADJ" or speech_part == "JJ" and speech_part != "i":
                adjectives[word] = adjectives.get(word, 0)
                adjectives[word] += 1

            sorted_adjectives = sorted(adjectives.items(), key=operator.itemgetter(1))

            most_common_adjective, most_common_count = sorted_adjectives[-1]

        new_adjective = Adjective(location=location, adjective=most_common_adjective, count=most_common_count)

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
