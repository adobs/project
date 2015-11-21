from model import UsernameGender, UsernameOrientation, Profile, Adjective, MeanShiftAlgo, db, connect_to_db
import json


def create_json():
    print "hello"

    data = {}
    data["name"] = "Typical Group Interested in Me"
    # users = db.session.query(MeanShiftAlgo.username).filter(MeanShiftAlgo.self_summary_label == 0).all()
    data["children"] = data.get("children",[])

    users = db.session.query(Profile.username).join(MeanShiftAlgo).filter(MeanShiftAlgo.self_summary_label == 3).all()
    orientations = db.session.query(UsernameOrientation.orientation).group_by(UsernameOrientation.orientation).all()

    user_list = [user[0] for user in users]
    print "user list is", user_list
    # genders = set(item[0] for item in users)
    # orientations = set(item[1] for item in users)
    # ages = set(item[2] for item in users)
    
    # for gender in genders:
    #     for orientation in orientations:
    #         for age in ages:
    #             for i in len(users):
    #                 if users[i][0] == gender and user[i][1] == orientation and user[i][2] == age:
    #                     data["children"].append

    

    genders = db.session.query(UsernameGender.gender).join(Profile).join(MeanShiftAlgo).filter(UsernameGender.username.in_(user_list)).group_by(UsernameGender.gender).all()
    for g_i, gender in enumerate(genders):
        
        current_gender_dict = {"name": gender[0], "children": []}
        data["children"].append(current_gender_dict)
        print "gender is", gender, "i is,", g_i
        for o_i, orientation in enumerate(orientations):
            current_orientation_dict = {"name": orientation[0], "children": []}
            data["children"][g_i]["children"].append(current_orientation_dict)
            print "orientation", orientation
            ages = db.session.query(Profile.age).group_by(Profile.age).all()
            for a_i, age in enumerate(ages):
                
                total = len(db.session.query(UsernameOrientation.username).join(Profile).join(UsernameGender).join(MeanShiftAlgo).filter(
                    MeanShiftAlgo.self_summary_label == 0).filter(Profile.age==age).filter(
                    UsernameOrientation.orientation==orientation).filter(
                    UsernameGender.gender == gender[0]).all())
                current_age_dict = {"name": age[0], "total": total,"children": []}
                data["children"][g_i]["children"][o_i]["children"].append(current_age_dict)

                adjectives = db.session.query(Adjective.adjective).join(Profile).join(UsernameGender).join(
                    UsernameOrientation).join(MeanShiftAlgo).filter(
                    UsernameGender.gender == gender[0]).filter(
                    Profile.age==age).filter(UsernameOrientation.orientation==orientation).filter(
                    MeanShiftAlgo.self_summary_label == 0).filter(Profile.age == age[0]).all()
                adjective_count = {}
                print "age is", age
                for adjective in adjectives:
                    adjective_count[adjective[0]] = adjective_count.get(adjective[0], 0)
                    adjective_count[adjective[0]] += 1
                    print "adjective is", adjective
                    current_adjective_dict = {"name": adjective[0], "value": adjective_count[adjective[0]]}
                    data["children"][g_i]["children"][o_i]["children"][a_i]["children"].append(current_adjective_dict)
    
    return data
    # print "BEGIN LONG ITERATION"
    # for g_i in range(len(data["children"])):
    #     if data.get("children")[g_i].get("children") == []:
    #         del data["children"][g_i]
    #     for o_i in range(len(data["children"][g_i]["children"])):
    #         if data.get("children")[g_i].get("children")[o_i].get("children") == []:
    #             del data["children"][g_i]["children"][o_i]
    #         for a_i in range(len(data["children"][g_i]["children"][o_i]["children"])):
    #             if data.get("children")[g_i].get("children")[o_i].get("children")[a_i].get("children") == []:
    #                 del data["children"][g_i]["children"][o_i]["children"][a_i]


def delete_childless(data):
    for i_g in range(len(data.get("children"))):
        for i_o in range(len(data["children"][i_g].get("children"))):
            for i_a in range(len(data["children"][i_g]["children"][i_o].get("children"))):
                for i_adj in range(len(data["children"][i_g]["children"][i_o]["children"][i_a].get("children"))):
                    for i in range(len(data["children"][i_g]["children"][i_o]["children"][i_a]["children"[i_adj]])):
                        if data["children"][i_g]["children"][i_o]["children"][i_a]["children"][i_adj].get("children") == []:
                            popped = data["children"][i_g]["children"][i_o]["children"][i_a].pop(i)
                            print "popped", popped

    for i_g in range(len(data.get("children"))):
        for i_o in range(len(data["children"][i_g].get("children"))):
            for i_a in range(len(data["children"][i_g]["children"][i_o].get("children"))):
                for i_adj in range(len(data["children"][i_g]["children"][i_o]["children"][i_a].get("children"))):
                    if data["children"][i_g]["children"][i_o]["children"][i_a].get("children") == []:
                        data["children"][i_g]["children"][i_o]["children"][i_a].pop(i_adj)


    for i_g in range(len(data.get("children"))):
        for i_o in range(len(data["children"][i_g].get("children"))):
            for i_a in range(len(data["children"][i_g]["children"][i_o].get("children"))):
                if data["children"][i_g]["children"][i_o].get("children") == []:
                    data["children"][i_g]["children"][i_o].pop(i_a)


    for i_g in range(len(data.get("children"))):
        for i_o in range(len(data["children"][i_g].get("children"))):
                if data["children"][i_g].get("children") == []:
                    data["children"][i_g].pop(i_o)


    for i_g in range(len(data.get("children"))):
        if data.get("children") == []:
            data.pop(i_g)


    # print "AT TOP OF DELETE"
    # #try to get the current dict's kids
    # kid_list = dictionary.get("children")

    # if kid_list:
    #     for kid in kid_list:
    #         if delete_childless(kid) == "delete":
    #             del kid

    # elif kid_list == None:
    #     return None

    # else:
    #     return "delete"


    # #if kid_list is None, it means we've reached the bottom of the tree, so
    # #back one level out of the recursion
    # if kid_list is None:
    #     print "if statement print"
    #     return None

    # #if kid list exists but is empty, pass a message back up one level in
    # #the recursion
    # elif kid_list == []:
    #     print "elif statement print"
    #     return "Delete me!"

    # #otherwise, there are kids, so check them one by one
    # else:
    #     for kid in kid_list:
    #         if delete_childless(kid, dictionary) == "Delete me!":
    #             del kid
    #             if kid_list == []:
    #                 print "else statement print"
    #                 return "Delete me!"
    # #we've now checked all of this dict's kids, and at least one survived,
    # #so this dict survives, too -- back out one level and go on to the next
    # #dict
    print "end of function print"
    return None

                    # data["children"].append({"name": gender, "children": })






if __name__ == "__main__":
    from flask_app import app
    connect_to_db(app)
    data = create_json()
    delete_childless(data)
    with open('static/json/sunburst.json', 'w') as outfile:
        json.dump(data, outfile)