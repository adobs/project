"""
map_helper.py -- functions used in the "/map.json" route of flask_app.py
"""

from model import Adjective, Profile, Location, UsernameOrientation, UsernameGender, db
from collections import defaultdict



def get_joined_adjectives(orientation_list, gender_list, age_list, location):
    """Takes inputs from form on map page, returns a list of tuples of adjectives.

    example: adjective_list = [("nice",)] 
    """
    # add in joined load
    # diagnose how many queries are being run, think about dynamically loading these tables.  dynamic vs lazy.
    # large JSON file of datapoints

    # adjective_object_list = db.session.query(Adjective.adjective, Profile.username).join(Profile).join(
    #                         UsernameOrientation).join(UsernameGender).filter(
    #                         UsernameOrientation.orientation.in_(orientation_list)).filter(
    #                         UsernameGender.gender.in_(gender_list)).filter(
    #                         Profile.age >= int(age_list[0])).filter(
    #                         Profile.age <= int(age_list[1])).filter(
    #                         Profile.location == location).all()
    
    #make all connections dynamic...load = dynamic to the profile table
    #create index for all of your tables
    # go into psql , create index for each table
    print "beginning of get_joined_adjectives function"
    adjective_object_list = (Adjective.query.options(db.joinedload('Profile'))).limit(10).all()
    print "\nin get joined adjectives function"
    print "adjective_object_list is", adjective_object_list
    
    adjective_list = []
    profile_list=[]
    profile_adjective_dictionary = defaultdict(list)
    print "adjective object list should be tuples of adjective, username", adjective_object_list
    for db_object in adjective_object_list:
        adjective = db_object[0]
        profile = db_object[1]
        adjective_list.append(adjective)
        profile_list.append(profile)

        # profile_adjective_dictionary[adjective]= ["NONE"]
        profile_adjective_dictionary[adjective]=profile_adjective_dictionary.get(adjective, [])
        profile_adjective_dictionary[adjective].append(profile)
        # print "profile adjective dictionary should have defualt value of empty list", profile_adjective_dictionary
        # profile_adjective_dictionary.setdefault(adjective,[])

    # for db_ofject in adjective_object_list:
    #     adjective = db_object[0]
    #     profile = db_object[1]

    profile_list = list(set(profile_list))
    population = len(profile_list)
    return [adjective_list, profile_list, profile_adjective_dictionary, population]


def get_lat_long(location):
    """For a given location, returns the latitude and longitude from the database"""

    latitude = db.session.query(Location.latitude).filter(
                                                Location.location==location).one()[0]

    longitude = db.session.query(Location.longitude).filter(
                                                Location.location==location).one()[0]

    return [latitude, longitude]


def add_adjective_to_compiled(compiled, location, latitude, longitude, population, adjective, count, profile_list, profiles):
    """Adds information to compiled dictionary that will be passed to Google Maps API when there are adjectives"""

    compiled[location]['lat']=latitude
    compiled[location]['lng']=longitude
    compiled[location]['adj']=adjective
    compiled[location]['count']=count
    compiled[location]['population']= population
    compiled[location]['location'] = location
    compiled[location]['profile_list'] = profile_list
    compiled[location]['profiles'] = profiles

    return compiled[location]


def add_nothing_to_compiled(compiled, location, latitude, longitude):
    """Adds information to compiled dictionary that will be passed to Google Maps API when there are no adjectives"""
    
    compiled[location]['lat']=latitude
    compiled[location]['lng']=longitude
    compiled[location]['adj']=""
    compiled[location]['count']=0
    compiled[location]['population']= 0
    compiled[location]['location'] = location

    return compiled[location]