"""
map_helper.py -- functions used in the "/map.json" route of flask_app.py
"""

from calculate_word_count import calculate_word_count


def get_compiled(logged_in, results):
    """Returns compiled dictionary of inputs for Google maps based on user selection of orientations, genders, and ages"""

    compiled = {"logged_in": logged_in, "results": {}}

    word_count = {}


    for result in results:
        username, location, adjective, latitude, longitude = result
        word_count[location] = word_count.get(location,{})
        word_count[location]["word"] = word_count[location].get("word",[])
        word_count[location]["profile_list"] = word_count[location].get("profile_list",[])
        word_count[location]["word"].append(adjective)
        word_count[location]["profile_list"].append(username)


        compiled["results"][location] = compiled["results"].get(location, {})
        compiled["results"][location]['lat'] = float(latitude)
        compiled["results"][location]['lng'] = float(longitude)
        compiled["results"][location]['location'] = location

    #broken up into a separate function 

    for location in word_count:
        unique_profiles = list(set(word_count[location]["profile_list"]))
        population = len(unique_profiles)
        word_list = word_count[location]["word"]
        most_common_adjective, most_common_count = calculate_word_count(word_list)        

        profile_index =[]

        for i, word in enumerate(word_count[location]["word"]):
            if word == most_common_adjective:
                profile_index.append(i)

        profiles = []
        for item in profile_index:
            profiles.append(word_count[location]["profile_list"][item])

        profiles = list(set(profiles))

        compiled["results"][location]['adj'] = most_common_adjective
        compiled["results"][location]['count'] = most_common_count
        compiled["results"][location]['short_profile_list']=profiles
        compiled["results"][location]['long_profile_list'] = unique_profiles
        compiled["results"][location]['population'] = population

    print "\n!!!! length of word count", len(word_count)
    return compiled



