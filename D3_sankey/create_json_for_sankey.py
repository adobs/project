import os

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

from model import MeanShiftAlgo, db, connect_to_db
import json
from sqlalchemy.sql import func, desc 

def write_json():
    # queries = db.session.query(MeanShiftAlgo.self_summary_label, MeanShiftAlgo.message_me_if_label).order_by(MeanShiftAlgo.self_summary_label).all()

    self_summary_query = db.session.query(MeanShiftAlgo.self_summary_label).group_by(MeanShiftAlgo.self_summary_label).order_by(desc(func.count(MeanShiftAlgo.self_summary_label))).limit(10).all()

    unconverted_list = []
    self_summary_unique = set()
    message_me_if_unique = set()
    
    data = {"nodes":[], "links":[]}

    # query for relevant data
    for self_summary_label in self_summary_query:
        query = db.session.query(MeanShiftAlgo.message_me_if_label, func.count(MeanShiftAlgo.message_me_if_label)).filter(MeanShiftAlgo.self_summary_label==self_summary_label[0]).group_by(MeanShiftAlgo.message_me_if_label).all()
        for message_me_if_label, count in query:
            if count >  200:
                unconverted_list.append(tuple([self_summary_label[0], message_me_if_label, count]))
                self_summary_unique.add(self_summary_label[0])
                message_me_if_unique.add(message_me_if_label)
    


    self_summary_unique_len = len(self_summary_unique)
    message_me_if_unique_len = len (message_me_if_unique)

    # iterate through the unconverted list and make ranges based on the number
    # of unique self_summary and message_me_if labels
    new_self_summary_label = range(self_summary_unique_len)
    new_message_me_if_label = range(self_summary_unique_len, self_summary_unique_len+message_me_if_unique_len)

    # make the conversion
    self_summary_unique_list = sorted(list(self_summary_unique))
    message_me_if_unique_list = sorted(list(message_me_if_unique))

    ########## add to nodes ##########
    for i in range(len(self_summary_unique_list)):
        data["nodes"].append({"node": new_self_summary_label[i],"name": new_self_summary_label[i]})

    for i in range(len(message_me_if_unique_list)):
        data["nodes"].append({"node": new_message_me_if_label[i],"name": new_message_me_if_label[i]})


    ########## add to links ##########
    for self_summary_label, message_me_if_label, count in unconverted_list: 
        self_summary_index = self_summary_unique_list.index(self_summary_label)
        message_me_if_index = message_me_if_unique_list.index(message_me_if_label)

        source = new_self_summary_label[self_summary_index]
        target = new_message_me_if_label[message_me_if_index]
        value = count

        data["links"].append({"source": source, "target": target, "value": value})

    with open('static/json/sankey.json', 'w') as outfile:
        json.dump(data, outfile)
    
    print self_summary_unique_list, new_self_summary_label, message_me_if_unique_list, new_message_me_if_label
    return self_summary_unique_list, new_self_summary_label, message_me_if_unique_list, new_message_me_if_label







    
    # for self_summary_label, message_me_if_label in queries:
    #     self_summary_unique_all.add(self_summary_label)
    #     message_me_if_unique_all.add(message_me_if_label)

    # self_summary_unique = []
    # self_summary_unique_count = []
    # for self_summary in sorted(list(self_summary_unique_all)):
    #     self_summary_unique.append(self_summary)
    #     self_summary_unique_count.append(queries.count(self_summary))

    # message_me_if_unique = []
    # message_me_if_unique_count = []
    # for message_me_if in sorted(list(message_me_if_unique_all)):
    #     message_me_if_unique.append(message_me_if)
    #     message_me_if_unique_count.append(queries.count(message_me_if))


    # # convert 
    # self_summary_new_label = range(len(self_summary_unique))
    # message_me_if_new_label = range(len(self_summary_unique),len(self_summary_unique)+len(message_me_if_unique))

    # # reduce message me ifs to numbers in order
    # self_summary_unique_list = sorted(list(self_summary_unique))
    # message_me_if_unique_list = sorted(list(message_me_if_unique))

    # for i in range(len(self_summary_unique_list)):
    #     data["nodes"].append({"node": self_summary_new_label[i],"name": self_summary_new_label[i]})

    # for i in range(len(message_me_if_unique_list)):
    #     data["nodes"].append({"node": message_me_if_new_label[i],"name": message_me_if_new_label[i]})

    # #converting time
    # for self_summary_label, message_me_if_label, count in zip:
    #     # self_summary_index = self_summary_unique_list.index(self_summary_label)
    #     # message_me_if_index = message_me_if_unique_list.index(message_me_if_label)

    #     # a = self_summary_new_label[self_summary_index]
    #     # b = message_me_if_new_label[message_me_if_index]
    #     # c = count
    #     print "self label", self_summary_label
    #     a = self_summary_unique_list.index(self_summary_label)
    #     print a
    #     source = self_summary_new_label[a]
    #     print "source is", source
    #     b = message_me_if_unique_list.index(message_me_if_label)
    #     target = message_me_if_new_label[b]
    #     value = count

    #     data["links"].append({"source": source, "target": target, "value": value})




    # # uncomment when writing to a file for a new json object
    # with open('static/json/sankey.json', 'w') as outfile:
    #     json.dump(data, outfile)
    
    # return self_summary_unique_list, self_summary_new_label, message_me_if_unique_list, message_me_if_new_label

if __name__ == "__main__":
    from flask_app import app
    connect_to_db(app)
    write_json()