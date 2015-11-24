from create_json_for_sankey import write_json
from model import SelfSummaryLabel, MessageMeIfLabel, db, connect_to_db

def create_self_summary_chart(label):
    self_summary_unique_list, self_summary_new_label, message_me_if_unique_list, message_me_if_new_label = [1, 4, 6, 116, 162, 177, 190], [0, 1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6, 9, 10, 15, 17] ,[7, 8, 9, 10, 11, 12, 13, 14, 15, 16]


    converted_label = self_summary_unique_list[self_summary_new_label.index(int(label.encode('utf8')))]

    label_feature = db.session.query(SelfSummaryLabel.feature).filter(SelfSummaryLabel.self_summary_label==converted_label).all()

    final_list = []

    
    for label in set(label_feature):

        final_list.append(label[0])
        # else:
        #     final_list.append([label[0], 1])

    final_list.sort()

    return final_list

def create_message_me_if_chart(label):
    self_summary_unique_list, self_summary_new_label, message_me_if_unique_list, message_me_if_new_label = [1, 4, 6, 116, 162, 177, 190], [0, 1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6, 9, 10, 15, 17] ,[7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

    converted_label = message_me_if_unique_list[message_me_if_new_label.index(int(label.encode('utf8')))]

    label_feature = db.session.query(MessageMeIfLabel.feature).filter(MessageMeIfLabel.message_me_if_label==converted_label).all()
    all_features = db.session.query(MessageMeIfLabel.feature).all()

    final_list = []

    for label in set(all_features):
        if label in set(label_feature):
            final_list.append(label[0])
        # else:
        #     final_list.append([label[0], 1])

    final_list.sort()
    return final_list

if __name__ == "__main__":
    from flask_app import app
    connect_to_db(app)
