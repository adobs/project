from okcupyd.session import Session
from okcupyd.json_search import SearchFetchable
from okcupyd.user import User
from model import Profile, Zipcode, db, connect_to_db
import time


def search_profile(user, location,i):
    j = 0 
    for profile in user.search(location=location)[:900]:            
        try: # add to the profile table
            j+=1

              # inputs for the profile table
            username = str(profile.username)
            age = profile.age
            usr_location = str(profile.location)
            gender = profile.gender
            orientation = profile.orientation
            self_summary = profile.essays.self_summary
            my_life = profile.essays.my_life
            good_at = profile.essays.good_at
            people_first_notice = profile.essays.people_first_notice
            favorites = profile.essays.favorites
            six_things = profile.essays.six_things
            think_about = profile.essays.think_about
            friday_night = profile.essays.friday_night
            private_admission = profile.essays.private_admission
            message_me_if = profile.essays.message_me_if
            print profile.location
            new_profile = Profile(username=username, 
                                age=age,
                                location=usr_location,
                                gender=gender,
                                orientation=orientation,
                                self_summary=self_summary,
                                my_life=my_life,
                                good_at=good_at,
                                people_first_notice=people_first_notice,
                                favorites=favorites,
                                six_things=six_things,
                                think_about=think_about,
                                friday_night=friday_night,
                                private_admission=private_admission,
                                message_me_if=message_me_if)

            print username, "i is", i, 'j is', j
            db.session.add(new_profile)
            db.session.commit()

                
        except Exception as e:
        # e will be the exception object
            print type(e)
            print str(e)
            db.session.rollback()
            continue

def seed_profile_data():
    session = Session.login('username', 'password')
    locations = db.session.query(Zipcode.zipcodes).all()
    print locations
    user = User(session=session)
    print user
    for location in locations:
        i=0
        print "i is", i
        while i<10000:
            search_profile(user, location[0],i)
            i+=900
            print "i is", i
        

            

if __name__ == "__main__":
    #connect db to app
    from flask_app import app
    connect_to_db(app)
    print "Connected to DB."

     #create the database
    db.create_all()
    seed_profile_data()
    # test_seed_call()
