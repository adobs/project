from create_json_for_sankey import write_json
from model import SelfSummaryLabel, MessageMeIfLabel, db, connect_to_db, MeanShiftAlgo, Profile
from itertools import cycle


def provide_label_sets():


    self_summary_unique_list = [0, 1, 4, 6, 126, 162, 177, 190, 396] 
    self_summary_new_label = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    message_me_if_unique_list = [0, 1, 2, 3, 4, 6, 9, 17]
    message_me_if_new_label = [9, 10, 11, 12, 13, 14, 15, 16]

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
        if count < 3:
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

def _colors():

    colors = ["#37465D", "#143726", "#000000","#bd1f2e","#051A37"]

    color_cycle = cycle(colors)

    return color_cycle

def _highlights():
    
    colors = ["#4E535D", "#04371C", "#000000", "#bd1f2e", '#1A2537']

    highlight_cycle = cycle(colors)

    return highlight_cycle


def prepare_data(label, identifier, section):

    self_summary_unique_list, self_summary_new_label, message_me_if_unique_list, message_me_if_new_label = provide_label_sets()
    
    color = _colors()
    highlight = _highlights()


    data = []
    if section == "source":
        converted_label = self_summary_unique_list[self_summary_new_label.index(int(label.encode('utf8')))]
        
        

        subquery = db.session.query(MeanShiftAlgo.username).filter(
                MeanShiftAlgo.self_summary_label==converted_label).filter(MeanShiftAlgo.message_me_if_label.in_(message_me_if_unique_list)).group_by(MeanShiftAlgo.username)
        
        query = db.session.query(identifier).filter(Profile.username.in_(subquery)).all()
    
    else:
        converted_label = message_me_if_unique_list[message_me_if_new_label.index(int(label.encode('utf8')))]

        subquery = db.session.query(MeanShiftAlgo.username).filter(
                MeanShiftAlgo.message_me_if_label==converted_label).filter(MeanShiftAlgo.self_summary_label.in_(self_summary_unique_list)).group_by(MeanShiftAlgo.username)
        
        query = db.session.query(identifier).filter(Profile.username.in_(subquery)).all()


    unique_identifier = set(query)

    entry = zip(unique_identifier, color, highlight)

    comment_info = []

    for item, color, highlight in entry:
        #get data into a percent
        count = query.count(item)*100/float(len(query))
        count = "{0:.1f}".format(count)
        data.append({"value": count, "label": item[0], "color": color, "highlight": highlight})
        print "label is", label
        if identifier == Profile.gender:
            comment_info.append({"value": count, "label": item[0]})

        if identifier == Profile.orientation:
            comment_info.append({"value": count, 'label': item[0]})



    return data, comment_info



if __name__ == "__main__":
    from flask_app import app
    connect_to_db(app)
