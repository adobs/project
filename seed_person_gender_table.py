from model import Profile, UsernameGender, Gender, db, connect_to_db



def seed_gender_table():
    
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
    # iterate through each username
    # for each username, go through their orientations, splice at comma
    # add the item to the person orientation table

    usernames = db.session.query(Profile.username, Profile.gender).all()

    for username, gender in usernames:
        gender_list = gender.split(", ")
        print "\n\ngender_list is", gender_list
        for gender_item in gender_list:
            print "gender_item is", gender_item
            new_entry = UsernameGender(username=username, gender=gender_item)
            print "username is", username
            print "gender is", gender_item
            db.session.add(new_entry)
            db.session.commit()






if __name__ == "__main__":
    #connect db to app
    from flask_app import app
    connect_to_db(app)
    print "Connected to DB."

     #create the database
    db.create_all()
    seed_gender_table()
    seed_person_gender_table()
    # test_seed_call()
