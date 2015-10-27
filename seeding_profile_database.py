from okcupyd.session import Session
from okcupyd.json_search import SearchFetchable
from model import Profile, Zipcode, db, connect_to_db
import time

def seed_profile_data():
    session = Session.login('adobsthecat', 'woof6996')
    locations = db.session.query(Zipcode.zipcodes).all()
    for location in locations:
        i=0
        while i <10000:
        # line that iterates through fields in a diferent database
            print location[0]

            for profile in SearchFetchable(session=session, location="San Francisco")[:900]:

              
                i+=1
                try: # add to the profile table
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

                    print username, i
                    # db.session.add(new_profile)
                    # db.session.commit()

                    
                except Exception as e:
                # e will be the exception object
                    print type(e)
                    print str(e)
                    db.session.rollback()
                    continue

    

if __name__ == "__main__":
    #connect db to app
    from flask_app import app
    connect_to_db(app)
    print "Connected to DB."

     #create the database
    db.create_all()
    seed_profile_data()
    # test_seed_call()
