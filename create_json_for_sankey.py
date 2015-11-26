from model import MeanShiftAlgo, db, connect_to_db
import json
from sqlalchemy.sql import func 

def write_json():
    queries = db.session.query(MeanShiftAlgo.self_summary_label, MeanShiftAlgo.message_me_if_label).filter(MeanShiftAlgo.self_summary_label>=0, MeanShiftAlgo.message_me_if_label >= 0).order_by(MeanShiftAlgo.self_summary_label).all()

    self_summary_unique_all = set()
    message_me_if_unique_all = set()


    data = {"nodes":[], "links":[]}




    
    for self_summary_label, message_me_if_label in queries:
        self_summary_unique_all.add(self_summary_label)
        message_me_if_unique_all.add(message_me_if_label)

    self_summary_unique = []
    self_summary_unique_count = []
    for self_summary in sorted(list(self_summary_unique_all)):
        self_summary_unique.append(self_summary)
        self_summary_unique_count.append(queries.count(self_summary))

    message_me_if_unique = []
    message_me_if_unique_count = []
    for message_me_if in sorted(list(message_me_if_unique_all)):
        message_me_if_unique.append(message_me_if)
        message_me_if_unique_count.append(queries.count(message_me_if))


    # convert 
    self_summary_new_label = range(len(self_summary_unique))
    message_me_if_new_label = range(len(self_summary_unique),len(self_summary_unique)+len(message_me_if_unique))

    # reduce message me ifs to numbers in order
    self_summary_unique_list = sorted(list(self_summary_unique))
    message_me_if_unique_list = sorted(list(message_me_if_unique))

    for i in range(len(self_summary_unique_list)):
        data["nodes"].append({"node": self_summary_new_label[i],"name": self_summary_new_label[i]})

    for i in range(len(message_me_if_unique_list)):
        data["nodes"].append({"node": message_me_if_new_label[i],"name": message_me_if_new_label[i]})

    #converting time
    for self_summary_label, message_me_if_label, count in queries:
        # self_summary_index = self_summary_unique_list.index(self_summary_label)
        # message_me_if_index = message_me_if_unique_list.index(message_me_if_label)

        # a = self_summary_new_label[self_summary_index]
        # b = message_me_if_new_label[message_me_if_index]
        # c = count
        print "self label", self_summary_label
        a = self_summary_unique_list.index(self_summary_label)
        print a
        source = self_summary_new_label[a]
        print "source is", source
        b = message_me_if_unique_list.index(message_me_if_label)
        target = message_me_if_new_label[b]
        value = count

        data["links"].append({"source": source, "target": target, "value": value})




    # uncomment when writing to a file for a new json object
    with open('static/json/sankey.json', 'w') as outfile:
        json.dump(data, outfile)
    
    return self_summary_unique_list, self_summary_new_label, message_me_if_unique_list, message_me_if_new_label

if __name__ == "__main__":
    from flask_app import app
    connect_to_db(app)
    write_json()