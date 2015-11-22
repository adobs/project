from model import MeanShiftAlgo, db, connect_to_db
from sqlalchemy.sql import func 
from flask_app import app

def query():
    queries = db.session.query(MeanShiftAlgo.self_summary_label, MeanShiftAlgo.message_me_if_label, func.count(MeanShiftAlgo.self_summary_label)).filter(MeanShiftAlgo.self_summary_label>0, MeanShiftAlgo.message_me_if_label > 0).group_by(MeanShiftAlgo.self_summary_label, MeanShiftAlgo.message_me_if_label).having(func.count(MeanShiftAlgo.self_summary_label)>=40).order_by(MeanShiftAlgo.self_summary_label).all()

    self_summary_unique = set()
    message_me_if_unique = set()

    for self_summary_label, message_me_if_label, count in queries:
        self_summary_unique.add(self_summary_label)
        message_me_if_unique.add(message_me_if_label)

    print queries

    print "self summary", self_summary_unique, "has", len(self_summary_unique), "labels"
    print "message", message_me_if_unique, "has", len(message_me_if_unique), 'self_summary_label'


if __name__=="__main__":
    connect_to_db(app)
    query()