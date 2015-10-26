from flask_sqlalchemy import SQLAlchemy
from model import Profile, Adjective, db, connect_to_db
import nltk
# nltk.download()
import operator


#
def queries():
    location_list = db.session.query(Profile.location).group_by(Profile.location).all()
    print location_list


    for location in location_list:
        print "location is:", location
        adjectives = {}
        self_summary_list = db.session.query(Profile.self_summary).filter(Profile.location == location[0]).all()
        
        for summary in self_summary_list:
            summary = summary.encode('ascii', ignore)

        print 
        print "self self_summary_list", self_summary_list
        print
        self_summary_string = " ".join(self_summary_list)
        # self_summary_string = self_summary_list[0] + self_summary_list[1]
        self_summary_string = self_summary_string.replace('\n', ' ')
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
