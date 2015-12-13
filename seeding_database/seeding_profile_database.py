"""
seeding_profile_database.py

This is the first program that should be run in the seeding_database directory.  
This program is responsible for scraping profiles from OkCupid.  It should be 
noted that the program normally takes a long time to run.  Personally, pulling 
down 58K for me took over 3 weeks.  Valid OkCupid login credentials are needed 
in order for the program to run (to be inserted below and replace 'username' 
and 'password').  Currently, the program will search for up to 10K profiles 
per location.  Change in code (there are comments) to raise/lower this number.
"""

import os

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

from okcupyd.session import Session
from okcupyd.json_search import SearchFetchable
from okcupyd.user import User
from model import Profile, Zipcode, db, connect_to_db
import time


def search_profile(user, location, i):
    """ Searches for profiles in a given location, adds to database """

    # more than 900 profiles errors out
    for profile in user.search(location=location)[:900]:            
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

            db.session.add(new_profile)
            db.session.commit()

                
        except Exception as e:
        # e will be the exception object
            print type(e)
            print str(e)
            db.session.rollback()
            continue

def seed_profile_data():
    """ Logs user into OkCupid and keeps track of profiles being pulled """ 

    # this must be valid login credentials, NOT 'username' and 'password'
    session = Session.login('username', 'password')
    locations = db.session.query(Zipcode.zipcodes).all()
    print locations
    user = User(session=session)
    print user
    for location in locations:
        i = 0

        # this searches for up to 10,000 profiles a location
        while i < 10000:
            search_profile(user, location[0], i)

            # can query for up to 900 profiles at a time; more will error out the program
            i += 900
            

if __name__ == "__main__":
    from flask_app import app
    connect_to_db(app)
    db.create_all()
    seed_profile_data()
