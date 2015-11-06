import csv
from model import OldAdjective, db, connect_to_db

#get all adjectives, get count
def create():
    adjectives = db.session.query(OldAdjective.adjectives).all()

    list_of_source_targets =[]

    count_dictionary = {}

    select_count_dictionary = {}

    NUMBER = 300

    final_list = [["source","target","value"]]
    #need a count dictionary
    #list of tuples
    for adjective in adjectives:
        print "adjective is", adjective
        adjective_list = adjective[0] #string  comma-separated list of adjectives
    
        
        for adjective in adjective_list:
            count_dictionary[adjective]= count_dictionary.get(adjective,0)
            count_dictionary[adjective]+=1

    for key in count_dictionary:
        if count_dictionary[key] > NUMBER:
            select_count_dictionary[key] = count_dictionary[key]
    
    for adjective in adjectives:
        adjective_list = adjective[0] #
        for i in range(len(adjective_list)-1):
            for j in range(i+1, len(adjective_list)):
                if adjective_list[i] in select_count_dictionary.keys() and adjective_list[j] in select_count_dictionary.keys():
                    list_of_source_targets.append(tuple([adjective_list[i], adjective_list[j]]))
                    print "i is,",i,"j is",j

    list_of_source_targets = list(set(list_of_source_targets))

    unique_adjectives_list = select_count_dictionary.keys()


    for word in unique_adjectives_list:
        final_list.append(tuple([word, word, select_count_dictionary[word]]))

    final_list.extend(list_of_source_targets)


    # need a tuple creator

    with open('force_chart_short.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        for element in final_list:
            try:
                spamwriter.writerow(element)
            except Exception as e:
                print type(e)
                print str(e)
                continue 


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.
    from flask_app import app

    connect_to_db(app)
    print "Connected to DB."
    create()