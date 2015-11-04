from model import Adjective, OldAdjective, db, connect_to_db


def seed_adjective_table():
    # oldadjectives is username | adjective_list
    # iterate through each oldadjective object, create a new adjective object that is the username, then adjective

    adjectives = db.session.query(OldAdjective.username, OldAdjective.adjectives).all()

    for username, adjective_list in adjectives:
        for adjective in adjective_list:
            new_entry = Adjective(username=username, adjective=adjective)
            print "username is", username
            print "adjective is", adjective
            db.session.add(new_entry)
            db.session.commit()






if __name__ == "__main__":
    #connect db to app
    from flask_app import app
    connect_to_db(app)
    print "Connected to DB."

     #create the database
    db.create_all()
    seed_adjective_table()
    # test_seed_call()
