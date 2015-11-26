from create_json_for_sankey import write_json
from model import SelfSummaryLabel, MessageMeIfLabel, db, connect_to_db, MeanShiftAlgo, Profile
import itertools

def provide_label_sets():
    self_summary_unique_list = [1, 4, 6, 116, 162, 177, 190]
    self_summary_new_label = [0, 1, 2, 3, 4, 5, 6] 
    message_me_if_unique_list = [1, 2, 3, 4, 5, 6, 9, 10, 15, 17] 
    message_me_if_new_label = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

    return self_summary_unique_list, self_summary_new_label, message_me_if_unique_list, message_me_if_new_label

def create_self_summary_words(label):

    self_summary_unique_list, self_summary_new_label, message_me_if_unique_list, message_me_if_new_label = provide_label_sets()

    converted_label = self_summary_unique_list[self_summary_new_label.index(int(label.encode('utf8')))]

    label_features = db.session.query(SelfSummaryLabel.feature).filter(SelfSummaryLabel.self_summary_label==converted_label).all()

    feature_count = {}
    final = {}
    
    label_features_list = [item[0] for item in label_features]

    for item in label_features_list:
        count = label_features_list.count(item)
        feature_count[item] = count

    print "feature count", feature_count
    
    unique_labels_list = []
    nonunique_labels_list = []
    for word, count in feature_count.iteritems():
        if count < 2:
            unique_labels_list.append(word) 
        else:
            nonunique_labels_list.append(word)

    unique_labels_list.sort()
    nonunique_labels_list.sort()

    final = {"unique": unique_labels_list, "nonunique": nonunique_labels_list}

    return final

def create_message_me_if_words(label):

    self_summary_unique_list, self_summary_new_label, message_me_if_unique_list, message_me_if_new_label = provide_label_sets()

    converted_label = message_me_if_unique_list[message_me_if_new_label.index(int(label.encode('utf8')))]

    label_features = db.session.query(MessageMeIfLabel.feature).filter(MessageMeIfLabel.message_me_if_label==converted_label).all()

    # all_other_labels_and_features = set(db.session.query(MessageMeIfLabel.message_me_if_label, MessageMeIfLabel.feature).filter(MessageMeIfLabel.message_me_if_label.in_(message_me_if_unique_list)).filter(MessageMeIfLabel.message_me_if_label!=converted_label).all())

    # all_other_features = [item[1] for item in all_other_labels_and_features]

    feature_count = {}
    final = {}
    
    label_features_list = [item[0] for item in label_features]

    for item in label_features_list:
        count = label_features_list.count(item)
        feature_count[item] = count

    # print "feature count", feature_count
    
    unique_labels_list = []
    nonunique_labels_list = []
    for word, count in feature_count.iteritems():
        if count < 4:
            unique_labels_list.append(word) 
        else:
            nonunique_labels_list.append(word)

    unique_labels_list.sort()
    nonunique_labels_list.sort()
    
    final = {"unique": unique_labels_list, "nonunique": nonunique_labels_list}

    return final

def _color_generator():

    colors = ["#37465D", "#F2F2F2", "#000000","#BF1E2D","#051A37"]

    for color in colors*5:
        yield color


def _highlight_generator():
    
    colors = ["#4E535D", "#F1F1F1", "#000000", "#BF4043", '#1A2537']

    for color in colors*5:
        yield color


def prepare_data(label, identifier, section):

    self_summary_unique_list, self_summary_new_label, message_me_if_unique_list, message_me_if_new_label = provide_label_sets()
    
    color = _color_generator()
    highlight = _highlight_generator()

    data = []
    if section == "source":
        converted_label = self_summary_unique_list[self_summary_new_label.index(int(label.encode('utf8')))]
        
        # QUERY = """SELECT :identifier
        #         FROM Profiles as P JOIN MeanShiftAlgos AS M 
        #         ON P.username=M.username 
        #         WHERE M.self_summary_label=:converted_label"""

        # cursor = db.session.execute(QUERY, {"identifier": identifier, "converted_label": converted_label})

        # results = cursor.fetchall()
        query = db.session.query(identifier).join(MeanShiftAlgo, 
                Profile.username==MeanShiftAlgo.username).filter(
                MeanShiftAlgo.self_summary_label==converted_label).all()
    
    else:
        converted_label = message_me_if_unique_list[message_me_if_new_label.index(int(label.encode('utf8')))]

        query = db.session.query(identifier).join(MeanShiftAlgo, 
                Profile.username==MeanShiftAlgo.username).filter(
                MeanShiftAlgo.message_me_if_label==converted_label).all()


    unique_identifier = set(query)

    for item in unique_identifier:
        count = query.count(item)
        data.append({"value": count, "label": item[0], "color": color.next(), "highlight": highlight.next()})

    return data



if __name__ == "__main__":
    from flask_app import app
    connect_to_db(app)
