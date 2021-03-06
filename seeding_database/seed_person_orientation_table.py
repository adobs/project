 """
 seed_person_orientation_table.py

 Seeds two tables - the orientations and the usernameorientations table - based on 
 information in the profile.
 """

 import os

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

from model import Profile, UsernameOrientation, Orientation, db, connect_to_db



def seed_orientation_table():
    """ Adds the unique orientations in the profile to orientations table """
    
    #list of tuples
    orientation_strings = db.session.query(Profile.orientation).all()

    orientation_list = []

    for orientation_string in orientation_strings:
        orientation_list.extend(orientation_string[0].split(", "))

    orientation_list = list(set(orientation_list))

    for orientation in orientation_list:
        new_entry = Orientation(orientation=orientation)
        db.session.add(new_entry)
        db.session.commit()





def seed_person_orientation_table():
    """ Adds all orientations for given username to usernameorientations table

    Iterates through each username.  For each username, goes through their 
    orientations, spliting at the comma.  Then adds the item to the table.
    """

    usernames = db.session.query(Profile.username, Profile.orientation).all()

    for username, orientation in usernames:
        orientation_list = orientation.split(", ")
        for orientation_item in orientation_list:
            new_entry = UsernameOrientation(username=username, orientation=orientation_item)
            db.session.add(new_entry)
            db.session.commit()


if __name__ == "__main__":
    from flask_app import app
    connect_to_db(app)

     #create the database
    db.create_all()
    seed_orientation_table()
    seed_person_orientation_table()
