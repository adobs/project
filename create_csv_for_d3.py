import csv
from model import OldAdjective, db, connect_to_db

#get all adjectives, get count
def create():
    adjectives = db.session.query(OldAdjective.adjectives).all()

    list_of_source_targets =[]

    count_dictionary = {}

    final_list = [["source","target","value"]]
    #need a count dictionary
    #list of tuples
    for adjective in adjectives:
        print "adjective is", adjective
        adjective_list = adjective[0] #string  comma-separated list of adjectives
       
        
        for adjective in adjective_list:
            count_dictionary[adjective]= count_dictionary.get(adjective,0)
            count_dictionary[adjective]+=1

        for i in range(len(adjective_list)):
            for j in range(len(adjective_list)):
                list_of_source_targets.append(tuple([adjective_list[i], adjective_list[j]]))
                print "i is,",i,"j is",j



    unique_adjectives_list = count_dictionary.keys()


    for word in unique_adjectives_list:
        final_list.append(tuple([word, word, count_dictionary[word]]))

    final_list.extend(list_of_source_targets)


    # need a tuple creator

    with open('force_chart_csv.csv', 'wb') as csvfile:
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