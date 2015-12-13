""" map_helper.py 

Function used in the "/map.json" route of flask_app.py.  The get_compiled
function creates dictionary to be JSONified and returned via AJAX.
"""

from calculate_word_count import calculate_word_count


def get_compiled(logged_in, results):
    """ Returns dictionary to be JSONified for Google Maps marker/label inputs.

    Results are based on user selection of gender, orientation, ages on the 
    Google Maps Adjective Map.  

    An example of a completed compiled dictionary (with fake data) is:

    compiled = {
                    "logged_in": True,
                    "results": {
                        "San Francisco":{
                            'lat': 100,
                            'lng': 100,
                            'adj': 'new'
                            'count': 2,
                            'short_profile_list': ['dayz12', 'SFbabe'],
                            'long_profile_list': ['dayz12, 'SFbabe', 'm_taco'],
                            'population': 3
                        }
                    }
                }

    """

    compiled = {"logged_in": logged_in, "results": {}}

    # word count is a dictionary that will hold all words/profiles per location
    word_count = {}

    # iterate through database query results
    for result in results:

        # unpack result
        username, location, adjective, latitude, longitude = result

        # for a given location, there are two subdictionaries, 
        #   "word" and "profile_list"
        word_count[location] = word_count.get(location,{})
        word_count[location]["word"] = word_count[location].get("word",[])
        word_count[location]["profile_list"] = word_count[location].get("profile_list",[])
        word_count[location]["word"].append(adjective)
        word_count[location]["profile_list"].append(username)

        # store location information
        compiled["results"][location] = compiled["results"].get(location, {})
        compiled["results"][location]['lat'] = float(latitude)
        compiled["results"][location]['lng'] = float(longitude)
        compiled["results"][location]['location'] = location

    for location in word_count:

        # unique profiles = unique list of profiles in location
        unique_profiles = list(set(word_count[location]["profile_list"]))
        # population = the number of unique profiles
        population = len(unique_profiles)

        word_list = word_count[location]["word"]

        # based on given word list, helper function calculated most common 
        #   adjective and its count
        most_common_adjective, most_common_count = calculate_word_count(word_list)        

        profile_index =[]

        # figures out the index of occurences of the most common adjective
        for i, word in enumerate(word_count[location]["word"]):
            if word == most_common_adjective:
                profile_index.append(i)

        # for a given most common adjective, figures out which profiles said 
        #   the word
        profiles = []
        for item in profile_index:
            profiles.append(word_count[location]["profile_list"][item])

        profiles = list(set(profiles))

        compiled["results"][location]['adj'] = most_common_adjective
        compiled["results"][location]['count'] = most_common_count
        compiled["results"][location]['short_profile_list']=profiles
        compiled["results"][location]['long_profile_list'] = unique_profiles
        compiled["results"][location]['population'] = population

    return compiled



