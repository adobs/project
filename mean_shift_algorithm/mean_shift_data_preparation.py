"""
mean_shift_data_preparation.py

Functions to be called in order that run machine learning: mean shift 
clustering algorithm.  The algorithm uses common words as feature words 
(presence of the word is converted into a boolean for the feature list).  
Bandwith can be flexed to adjust number of clusters and number of profiles 
per cluster.

Run functions that are commented out under the __name__ == "__main__" 
as appropriate.
"""

import os

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)


from model import Profile, Adjective, Gender, Orientation, Location, db, connect_to_db, MeanShiftAlgo, SelfSummaryLabel, MessageMeIfLabel
from flask_app import app
from sklearn.cluster import MeanShift, estimate_bandwidth
from random import sample
import numpy as np
import datetime
from sklearn.externals import joblib
from nltk.corpus import stopwords

def clean(dirty_list):
    """ Returns list of words with non-alpha characters stripped """

    clean_list = []
    clean_string = ""
    for word in dirty_list:
        word = unicode(word)
        word = word.strip("\n\t1234567890!@#$%^&*()-=+{}[]/\\'\"<>?.,:;~`").replace("\n", " ").replace(".", " ").replace("\t","").replace("1","").replace("2","").replace("3","").replace("4","").replace("5","").replace("6","").replace("7","").replace("8","").replace("9","").replace("0","").replace("!","").replace("@","").replace("#","").replace("$","").replace("%","").replace("^","").replace("&","").replace("*","").replace("(","").replace(")","").replace("-"," ").replace("=","").replace("+","").replace("{","").replace("}","").replace("[","").replace("]","").replace("'","").replace("\"","").replace(":","").replace(";","").replace("\\","").replace("/","").replace(">","").replace("<","").replace("`","").replace("~","").replace("_","")
        clean_string += word+" "

    clean_list.extend(clean_string.split(" "))


    return clean_list


def get_words(profile, random_profiles_to_train, n_train):
    """Gets word (by parsing text) out of database based on random samples.

    Remove from list common words that appear above threshold (n) times.
    Returns a randomly generated list of features.
    """
    low_threshold, high_threshold = n_train*0.05, n_train*.5

    text_tuples = db.session.query(profile).filter(Profile.username.in_(random_profiles_to_train)).all()

    words_and_count = {}

    features_set = set()

    text_word_list = []
    for text in text_tuples:
        text_word_list.extend(text[0].split(" "))

    clean_list = clean(text_word_list)
    
    filtered_words = [word for word in clean_list if word not in stopwords.words('english')]
    
    for word in filtered_words:

        words_and_count[word] = words_and_count.get(word,0)
        words_and_count[word] += 1

    for key, value in words_and_count.iteritems():
        if value <= high_threshold and value >= low_threshold:
            features_set.add(key)

    features = list(features_set)

    return features


def convert(features, text_list):
    """For each user, search features, and return numpy boolean array for each user

    1 if has feature, 0 if doesn't
    """

    boolean_input = []

    for text in text_list:

        user = []
        clean_list = clean(text.split(" "))
        for feature in features:
            word_count = max([1 if word == feature else 0 for word in clean_list])
            user.append(word_count)

        boolean_input.append(user)

    boolean_input_array = np.array(boolean_input, dtype=int)

    shape = boolean_input_array.shape

    return boolean_input_array


def mean_shift_train(boolean_input_array, bandwidth_factor):
    """Conduct mean shift analysis on training data."""

    n_samples, n_features = boolean_input_array.shape
    seeds = boolean_input_array.shape
    X = boolean_input_array

    # The following bandwidth can be automatically detected using
    bandwidth = estimate_bandwidth(X, quantile=.3, n_samples=n_samples)
    

    ms = MeanShift(bandwidth=bandwidth * bandwidth_factor, cluster_all=True)
    ms.fit(X)

    labels = ms.labels_   # all labels
    cluster_centers = ms.cluster_centers_    # all clusters

    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)

    return ms


def mean_shift_predict(boolean_input_array, ms):
    """ Conduct mean shift analysis predictions on unlabeled data."""

    n_samples, n_features = boolean_input_array.shape
    X = boolean_input_array

    clusters_for_ea_sample = ms.predict(X)

    label_counts_dict = {}
    for lab in list(clusters_for_ea_sample):
        label_counts_dict[lab] = label_counts_dict.get(lab, 0)
        label_counts_dict[lab] += 1

    labels = ms.labels_
    cluster_centers = ms.cluster_centers_

    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)

    return clusters_for_ea_sample, cluster_centers


def train_model_and_pickle(n_train):
    """ Sample the data, extract features, train the model """

    profile_section = db.session.query(Profile.username, Profile.self_summary, Profile.message_me_if).all()

    random_to_train = sample(profile_section, n_train)

    # result is a much shorter list of tups. now extract only the usernames
    random_profiles_to_train = [item[0] for item in random_to_train]

    # which features to use, for cluster dimensions
    features_self_summary = get_words(Profile.self_summary, random_profiles_to_train,n_train)
    features_message_me_if = get_words(Profile.message_me_if, random_profiles_to_train, n_train)

    print "\nfeatures",features_self_summary
    print "\nfEADTRUES",features_message_me_if

    # must be the profiles that are trained
    text_list_self_summary_train = [item[1] for item in random_to_train]
    text_list_message_me_if_train = [item[2] for item in random_to_train]

    boolean_input_array_self_summary_train = convert(features_self_summary, text_list_self_summary_train)
    boolean_input_array_message_me_if_train = convert(features_message_me_if, text_list_message_me_if_train)

    # bandwidth is set here at 0.2
    ms_trained_object_self_summary = mean_shift_train(boolean_input_array_self_summary_train, 0.2)
    ms_trained_object_message_me_if = mean_shift_train(boolean_input_array_message_me_if_train, 0.2)

    joblib.dump(ms_trained_object_self_summary, 'model_pkl/self_summary_pickle.pkl')
    joblib.dump(ms_trained_object_message_me_if, 'model_pkl/message_me_if_pickle.pkl')

    file_features_self_summary = open('model_pkl/features_self_summary.txt', 'w')
    [file_features_self_summary.write(feature+"|") for feature in features_self_summary]
    file_features_self_summary.close()

    file_features_message_me_if = open('model_pkl/features_message_me_if.txt', 'w')
    [file_features_message_me_if.write(feature+"|") for feature in features_message_me_if]
    file_features_message_me_if.close()

    print "MODELS TRAINED AND SAVED!"
    return profile_section


def test_data():
    """ Finds and saves labels for users in databse """

    # get a list of all usernames
    all_usernames_tuple = db.session.query(Profile.username).all()
    all_usernames = [profile[0] for profile in all_usernames_tuple]
    total_num_users = len(all_usernames)
    increment = 1000
    start = 0
    count_users_both_labels = 0
    len_to_input = 0

    while start < total_num_users:
        end = start + increment

        get_users = all_usernames[start:end]
        profile_section = db.session.query(Profile.username, Profile.self_summary, Profile.message_me_if).filter(Profile.username.in_(get_users)).all()

        count, input_ = run_test_and_store(profile_section)
        count_users_both_labels += count
        len_to_input += input_
        start += increment


def run_test_and_store(profile_section):

    ms_trained_object_self_summary = joblib.load('model_pkl/self_summary_pickle.pkl')
    ms_trained_object_message_me_if = joblib.load('model_pkl/message_me_if_pickle.pkl')

    features_self_summary = open('model_pkl/features_self_summary.txt').read().rstrip("|").split("|")
    features_message_me_if = open('model_pkl/features_message_me_if.txt').read().rstrip("|").split("|")

    count_users_both_labels = 0

    sample_list = profile_section

    usernames = [item[0] for item in sample_list]

    # functions to attain labels for self_summary
    sample_list_self_summary = [item[1] for item in sample_list]
    boolean_input_array_self_summary = convert(features_self_summary, sample_list_self_summary)
    labels_self_summary, cluster_centers_self_summary = mean_shift_predict(boolean_input_array_self_summary, ms_trained_object_self_summary)

    # functions to attain labels for message_me_if
    sample_list_message_me_if = [item[2] for item in sample_list]
    boolean_input_array_message_me_if = convert(features_message_me_if, sample_list_message_me_if)
    labels_message_me_if, cluster_centers_message_me_if = mean_shift_predict(boolean_input_array_message_me_if, ms_trained_object_message_me_if)

    self_summary_dict = {}
    message_me_if_dict = {}    


    for i in range(len(cluster_centers_self_summary)):
        self_summary_dict[labels_self_summary[i]] = zip(features_self_summary, cluster_centers_self_summary[i])

    for key, value in self_summary_dict.iteritems():
        for feature, center in value:
            if center == 1:
                new_self_summary = SelfSummaryLabel(self_summary_label=key, feature=feature)
                db.session.add(new_self_summary)

    for i in range(len(cluster_centers_message_me_if)):
        message_me_if_dict[labels_message_me_if[i]] = zip(features_message_me_if, cluster_centers_message_me_if[i])
    
    for key, value in message_me_if_dict.iteritems():
        for feature, center in value:
            if center == 1:
                new_message_me_if = MessageMeIfLabel(message_me_if_label=key, feature=feature)
                db.session.add(new_message_me_if)


    zipped =  zip(usernames, labels_self_summary, labels_message_me_if)
    to_input = list(zipped)
    for entry in to_input:
        username, self_summary_label, message_me_if_label = entry
        new_input = MeanShiftAlgo(username=username, self_summary_label=self_summary_label, message_me_if_label=message_me_if_label)

        if self_summary_label > 1 and message_me_if_label > 1:
            count_users_both_labels +=1

        db.session.add(new_input)

    db.session.commit()

    return count_users_both_labels, len(to_input)



if __name__ == "__main__":
    connect_to_db(app)
    
    # train_model_and_pickle(500)
    test_data()
    # print_cluster_words()
    # run_test_and_store()
