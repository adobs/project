from okcupyd.session import Session
from okcupyd.json_search import SearchFetchable
from model import Profile, Essay, db, connect_to_db
import time


def seed_profile_data():
    session = Session.login('adobsthecat', 'PASSWORD')
    i=0
    while i <100000:
        for profile in SearchFetchable(session=session)[:900]:
            i+=1
            try: # add to the profile table
                # inputs for the profile table
                username = str(profile.username)
                # id = int(profile.id)
                age = profile.age
                location = str(profile.location)
                gender = profile.gender
                orientation = profile.orientation
                
                print profile, i


                new_profile = Profile(username=username, 
                                      age=age,
                                      location=location,
                                      gender=gender,
                                      orientation=orientation)

                db.session.add(new_profile)

                # inputs for the essay table
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

                # print type(self_summary)
                # print type(my_life)
                # print type(good_at)
                # print type(people_first_notice)
                # print type(favorites)
                # print type(six_things)
                # print type(think_about)
                # print type(friday_night)
                # print type(private_admission)
                # print type(message_me_if)

                new_essay = Essay(username=username,
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

                db.session.add(new_essay)
                

                # gentation = profile.gentation
                # ages = profile.lookingfor.ages
                # single = profile.lookingfor.single
                # near_me = profile.lookingfor.near_me
                # kinds = profile.lookingfor.kinds

                # print type(gentation)
                # print type(ages)
                # print type(single)
                # print type(near_me)
                # print type(kinds)

                # new_looking_for = Looking_for(username=username, 
                #                              gentation=gentation,
                #                              ages=ages,
                #                              single=single,
                #                              near_me=near_me,
                #                              kinds=kinds)

                # db.session.add(new_looking_for)

                # commit changes
                db.session.commit()

              

            except Exception as e:
                # e will be the exception object
                        print type(e)
                        continue

  

if __name__ == "__main__":
    #connect db to app
    from flask_app import app
    connect_to_db(app)
    print "Connected to DB."

     #create the database
    db.create_all()
    seed_profile_data()
