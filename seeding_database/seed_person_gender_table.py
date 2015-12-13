 """
 seed_person_gender_table.py

 Seeds two tables - the genders and the usernamegenders table - based on 
 information in the profile.
 """

 import os

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

from model import Profile, UsernameGender, Gender, db, connect_to_db



def seed_gender_table():
    """ Adds the unique genders listed in the profile to the genders table """
    
    #list of tuples
    gender_strings = db.session.query(Profile.gender).all()

    gender_list = []

    for gender_string in gender_strings:
        gender_list.extend(gender_string[0].split(", "))

    gender_list = list(set(gender_list))

    for gender in gender_list:
        new_entry = Gender(gender=gender)
        db.session.add(new_entry)
        db.session.commit()



def seed_person_gender_table():
    """ Adds all genders for a given username to usernamegenders table

    Iterates through each username.  For each username, goes through their 
    genders, spliting at the comma.  Then adds the item to the table.
    """

    usernames = db.session.query(Profile.username, Profile.gender).all()

    for username, gender in usernames:
        gender_list = gender.split(", ")
        for gender_item in gender_list:
            new_entry = UsernameGender(username=username, gender=gender_item)
            db.session.add(new_entry)
            db.session.commit()


if __name__ == "__main__":
    from flask_app import app
    connect_to_db(app)
    db.create_all()
    seed_gender_table()
    seed_person_gender_table()
