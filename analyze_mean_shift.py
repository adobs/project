from model import MeanShiftAlgo, connect_to_db, db
from sqlalchemy import distinct
from sqlalchemy import func
def calculate():
    distinct_self_summary = db.session.query(distinct(MeanShiftAlgo.self_summary_label),func.count(MeanShiftAlgo.self_summary_label)*float(100)/5000).order_by(MeanShiftAlgo.self_summary_label).group_by(MeanShiftAlgo.self_summary_label).all()
    print "distinct self sum is", distinct_self_summary
    distinct_message_me_if = db.session.query(distinct(MeanShiftAlgo.message_me_if_label),func.count(MeanShiftAlgo.message_me_if_label)*float(100)/5000).order_by(MeanShiftAlgo.message_me_if_label).group_by(MeanShiftAlgo.message_me_if_label).all()
    print "distinc message me if is", distinct_message_me_if
    answer = []
    for self_summary_label, count in distinct_self_summary:
        for message in distinct_message_me_if:
            message_me_if_stat = db.session.query(func.count(MeanShiftAlgo.message_me_if_label)*float(100)/5000).filter(MeanShiftAlgo.message_me_if_label==message[0]).one()

            answer.append([self_summary_label, "{0:.2f}".format(count), message[0], "{0:.2f}".format(message_me_if_stat[0])])


    print answer




if __name__=="__main__":
    from flask_app import app
    connect_to_db(app)
    calculate()