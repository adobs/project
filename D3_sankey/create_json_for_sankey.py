"""
create_json_for_sankey.py 

The function write_json converts the labels from what's stored in the database 
to what's acceptable for D3.  It adds information for the nodes and the links 
in order to be made into an appropriate dictionary that will be able to be 
JSONified and used to create the D3 Sankey chart.
"""

import os

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)

from model import MeanShiftAlgo, db, connect_to_db
import json
from sqlalchemy.sql import func, desc 

def write_json():
    """ Creates JSON file with information needed for D3 Sankey chart """

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

    # add to nodes
    for i in range(len(self_summary_unique_list)):
        data["nodes"].append({"node": new_self_summary_label[i],"name": new_self_summary_label[i]})

    for i in range(len(message_me_if_unique_list)):
        data["nodes"].append({"node": new_message_me_if_label[i],"name": new_message_me_if_label[i]})


    # add to links
    for self_summary_label, message_me_if_label, count in unconverted_list: 
        self_summary_index = self_summary_unique_list.index(self_summary_label)
        message_me_if_index = message_me_if_unique_list.index(message_me_if_label)

        source = new_self_summary_label[self_summary_index]
        target = new_message_me_if_label[message_me_if_index]
        value = count

        data["links"].append({"source": source, "target": target, "value": value})

    with open('static/json/sankey.json', 'w') as outfile:
        json.dump(data, outfile)
    
    return self_summary_unique_list, new_self_summary_label, message_me_if_unique_list, new_message_me_if_label


if __name__ == "__main__":
    from flask_app import app
    connect_to_db(app)
    write_json()