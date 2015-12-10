import os

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

from model import Profile, UsernameOrientation, Orientation, db, connect_to_db



def seed_orientation_table():
    
    #list of tuples
    orientation_strings = db.session.query(Profile.orientation).all()

    orientation_list = []

    for orientation_string in orientation_strings:
        orientation_list.extend(orientation_string[0].split(", "))

    orientation_list = list(set(orientation_list))

    for orientation in orientation_list:
        # orientation= orientation.strip()
        new_entry = Orientation(orientation=orientation)
        db.session.add(new_entry)
        db.session.commit()





def seed_person_orientation_table():
    # iterate through each username
    # for each username, go through their orientations, splice at comma
    # add the item to the person orientation table

    usernames = db.session.query(Profile.username, Profile.orientation).all()

    for username, orientation in usernames:
        orientation_list = orientation.split(", ")
        print "\n\norientation_list is", orientation_list
        for orientation_item in orientation_list:
            print "orientation_item is", orientation_item
            new_entry = UsernameOrientation(username=username, orientation=orientation_item)
            print "username is", username
            print "orientation is", orientation_item
            db.session.add(new_entry)
            db.session.commit()






if __name__ == "__main__":
    #connect db to app
    from flask_app import app
    connect_to_db(app)
    print "Connected to DB."

     #create the database
    db.create_all()
    seed_orientation_table()
    seed_person_orientation_table()
    # test_seed_call()
