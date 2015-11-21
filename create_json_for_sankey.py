from model import MeanShiftAlgo, db, connect_to_db
import json
from sqlalchemy.sql import func 

def write_json():
    queries = db.session.query(MeanShiftAlgo.self_summary_label, MeanShiftAlgo.message_me_if_label, func.count(MeanShiftAlgo.self_summary_label)).filter(MeanShiftAlgo.self_summary_label>0, MeanShiftAlgo.message_me_if_label > 0).group_by(MeanShiftAlgo.self_summary_label, MeanShiftAlgo.message_me_if_label).having(func.count(MeanShiftAlgo.self_summary_label)>=20).order_by(MeanShiftAlgo.self_summary_label).all()

    self_summary_unique = set()
    message_me_if_unique = set()

    data = {"nodes":[], "links":[]}

    for self_summary_label, message_me_if_label, count in queries:
        self_summary_unique.add(self_summary_label)
        message_me_if_unique.add(message_me_if_label)

    #add to nodes
    for self in self_summary_unique:
        for i in range(len(self_summary_unique)):
            data["nodes"].append({"node": self+1000, "name": i})
    for me in message_me_if_unique:
        data["nodes"].append({"node": me})

    for self_summary_label, message_me_if_label, count in queries:
        data["links"].append({"source":self+1000, "target":message_me_if_label, "value": count})

    with open('static/json/sankey.json_data', 'w') as outfile:
        json.dump(data, outfile)
    
if __name__ == "__main__":
    from flask_app import app
    connect_to_db(app)
    write_json()