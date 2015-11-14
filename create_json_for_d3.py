from model import OldAdjective, db, connect_to_db

#get all adjectives, get count
def create_json(adjective):
    
    NUMBER = 1
    
    count_dictionary = {}

    select_count_dictionary = {}

    links = []

    final_list = {"nodes":[], "links":[]}

    # might have to change this to get the item out of the tuple
    # users = db.session.query(OldAdjective.username).filter(Adjective.adjective==adjective).all()

    adjectives = db.session.query(OldAdjective.adjectives).filter(OldAdjective.adjectives.any(adjective)).all()

    # adjectives = db.session.query(Adjective.adjective).filter(Adjective.username.in_(users)).group_by(Adjective.username).limit(10).all()


    #adjectives is [([])]
    for adjective in adjectives:
        # print "adjective is", adjective
        adjective_list = adjective[0]
        for adjective in adjective_list:
                count_dictionary[adjective]= count_dictionary.get(adjective,0)
                count_dictionary[adjective]+=1

    for key in count_dictionary:
        if count_dictionary[key] > NUMBER:
            select_count_dictionary[key] = count_dictionary[key]
    

    for adjective in adjectives:
        adjective_list = adjective[0] #
        # print "adjective list is", adjective_list
        for i in range(len(adjective_list)-1):
            for j in range(i+1, len(adjective_list)):
                if adjective_list[i] in select_count_dictionary.keys() and adjective_list[j] in select_count_dictionary.keys():
                    links.append(tuple([adjective_list[i], adjective_list[j]]))
                    # print "i is,",i,"j is",j

    links = list(set(links))

    # print "links is", links


    unique_adjectives_list = select_count_dictionary.keys()

    for word in unique_adjectives_list:
        final_list["nodes"].append({"adjective": word, "count": select_count_dictionary[word]})

    for source, target in links:
        source_index = unique_adjectives_list.index(source)
        target_index = unique_adjectives_list.index(target)
        final_list["links"].append({"source": source_index, "target": target_index})

    # json = final_list

    return final_list



if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.
    from flask_app import app

    connect_to_db(app)
    print "Connected to DB."
