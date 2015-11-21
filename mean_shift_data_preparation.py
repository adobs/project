# take text data per user, and parse on each word. list of words.
# unique set(list of words).
# remove from set any words that are in your common_words
# convert into a list of booleans:
# 
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
# from sklearn.datasets.samples_generator import make_blobs
from model import Profile, Adjective, Gender, Orientation, Location, db, connect_to_db, MeanShiftAlgo
from flask_app import app
from random import sample
import datetime
from sklearn.externals import joblib

def clean(dirty_list):
    # print "dirty list is", dirty_list
    clean_list = []
    clean_string = ""
    for word in dirty_list:
        # print "\nword is ", word
        word = unicode(word)
        word = word.strip("\n\t1234567890!@#$%^&*()-=+{}[]/\\'\"<>?.,:;~`").replace("\n", " ").replace(".", " ").replace("\t","").replace("1","").replace("2","").replace("3","").replace("4","").replace("5","").replace("6","").replace("7","").replace("8","").replace("9","").replace("0","").replace("!","").replace("@","").replace("#","").replace("$","").replace("%","").replace("^","").replace("&","").replace("*","").replace("(","").replace(")","").replace("-"," ").replace("=","").replace("+","").replace("{","").replace("}","").replace("[","").replace("]","").replace("'","").replace("\"","").replace(":","").replace(";","").replace("\\","").replace("/","").replace(">","").replace("<","").replace("`","").replace("~","").replace("_","")
        clean_string += word+" "

    # print "clean string is", clean_string

    clean_list.extend(clean_string.split(" "))

    # print "clean list is", clean_list
    return clean_list


def get_words(profile, random_profiles_to_train, n_train):
    """Gets word (by parsing text) out of database based on random samples.

        Remove from list common words that appear above threshold (n) times.
        Returns a randomly generate list of features.
    """
    low_threshold, high_threshold = n_train*0.05, n_train*.5

    text_tuples = db.session.query(profile).filter(Profile.username.in_(random_profiles_to_train)).all()
    # print "text_tuples is", text_tuples
    # returns a list of tuples
    words_and_count = {}

    features_set = set()

    text_word_list = []
    for text in text_tuples:
        # print "text is ", text
        text_word_list.extend(text[0].split(" "))
        # print "text wor list is", text_word_list
        # print "text word list", text_word_list
    
    print "pre clean in get words"
    clean_list = clean(text_word_list)
    print "post clean in get words"
    
    for word in clean_list:
        words_and_count[word] = words_and_count.get(word,0)
        words_and_count[word] += 1
            # print "word is", word

    # print "words and count ", words_and_count

    for key, value in words_and_count.iteritems():
        # print key
        if value <= high_threshold and value >= low_threshold:
            features_set.add(key)

    features = list(features_set)

    # print "for", profile, "the features are", features

    return features


def convert(features, text_list):
    """For each user, search features, and return numpy boolean array for each user

    1 if has feature, 0 if doesn't
    """

    # print "features is", features 

    boolean_input = []

    for text in text_list:
        # print "text in text list is", text
        # import pdb; pdb.set_trace()

        user = []
        clean_list = clean(text.split(" "))
        for feature in features:
            word_count = max([1 if word == feature else 0 for word in clean_list])
            user.append(word_count)

        boolean_input.append(user)

    boolean_input_array = np.array(boolean_input, dtype=int)

    # print "shape of the array is", boolean_input_array.shape
    shape = boolean_input_array.shape
        # for i in range(shape[0]):
        # print "total non-0s", sum(boolean_input_array[i])

    # X : array-like, shape=[n_samples, n_features]
    # Input points.
    # quantile : float, default 0.3
    return boolean_input_array

def mean_shift_train(boolean_input_array, bandwidth_factor):
    """Conduct mean shift analysis on training data."""

    n_samples, n_features = boolean_input_array.shape
    seeds = boolean_input_array.shape
    X = boolean_input_array

    # The following bandwidth can be automatically detected using
    bandwidth = estimate_bandwidth(X, quantile=.3, n_samples=n_samples)
    
    # print "bandwith is", bandwidth

    ms = MeanShift(bandwidth=bandwidth * bandwidth_factor, cluster_all=True)
    ms.fit(X)

    labels = ms.labels_   # all labels
    cluster_centers = ms.cluster_centers_    # all clusters

    # print "cluster centers", list(cluster_centers)

    # print "mean shift labels (training) is", list(labels)
    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)

    # print "unique labels:", labels_unique
    # print "labels:", labels
    print "number of estimated clusters (training) : %d" % n_clusters_
    # print "cluster centers:", cluster_centers[:5]

    # import matplotlib.pyplot as plt
    # from itertools import cycle

    # plt.figure(1)
    # plt.clf()

    # colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
    # colors is an iterator....never runs out, so the zip should be fine

    # print list(labels)
    # print set(labels)



    # for k in range(n_clusters_):
    #    print
    #    my_members = labels == k
    #    # print my_members
    #    print "\nk", k    # number of clusters
    #    cluster_center = cluster_centers[k]     # len of cluster_center == n_features
    #    # print "cluster_center", cluster_center   # [-0.95635942 -1.01166653]
    #    print "len is ok", len(cluster_center) == n_features
    #    # print "min of all dimensions:", min(cluster_center)
    #    # print "max of all dimensions:", max(cluster_center)
    #    # print "average of all dimensions:", float(sum(cluster_center))/n_features




    #    plt.plot(X[my_members, 0], X[my_members, 1], col + '.')
    #    plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
    #             markeredgecolor='k', markersize=14)
    # plt.title('Estimated number of clusters: %d' % n_clusters_)
    # plt.show()

    # for dimension in cluster_center:   # 2 variables, plotted as x/y.  or # n_features
    #    print "THIS DIMENSION,", dimension
    print "done with MS train"
    # import pdb; pdb.set_trace()

    return ms

def mean_shift_predict(boolean_input_array, ms):
    """Conduct mean shift analysis predictions on unlabeled data."""

    n_samples, n_features = boolean_input_array.shape
    # seeds = boolean_input_array.shape
    X = boolean_input_array

    # The following bandwidth can be automatically detected using
    # bandwidth = estimate_bandwidth(X, quantile=quantile, n_samples=n_samples)
    
    # print "bandwith is", bandwidth

    clusters_for_ea_sample = ms.predict(X)

    # print "cluster label, for ea sample:", clusters_for_ea_sample
    # print "muke sure # labels predicted == n_samples:", len(list(clusters_for_ea_sample)) == n_samples
    # print "number of unique labels, in predicted labels:", set(list(clusters_for_ea_sample))

    ##### DLW TIRED CODE -- REMOVE LATER #####
    label_counts_dict = {}
    for lab in list(clusters_for_ea_sample):
        label_counts_dict[lab] = label_counts_dict.get(lab, 0)
        label_counts_dict[lab] += 1

    # print "label counts dict is", label_counts_dict

    ###################################

    # labels = ms.labels_
    labels = ms.labels_
    cluster_centers = ms.cluster_centers_

    # print "cluster centers", list(cluster_centers)

    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)

    print "number of estimated clusters, (test should be same as training): %d" % n_clusters_

    # import pdb; pdb.set_trace()

    # import matplotlib.pyplot as plt
    # from itertools import cycle

    # # plt.figure(1)
    # # plt.clf()

    # colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
    # # colors is an iterator....never runs out, so the zip should be fine

    # # print list(labels)
    # # print set(labels)

    # for k, col in zip(range(n_clusters_), colors):
    #    print
    #    my_members = labels == k
    #    # print my_members
    #    print "\nk", k    # number of clusters
    #    cluster_center = cluster_centers[k]     # len of cluster_center == n_features
    #    # print "cluster_center", cluster_center   # [-0.95635942 -1.01166653]
    #    print "len is ok", len(cluster_center) == n_features
    #    # print "min of all dimensions:", min(cluster_center)
    #    # print "max of all dimensions:", max(cluster_center)
       # print "average of all dimensions:", float(sum(cluster_center))/n_features




    #    plt.plot(X[my_members, 0], X[my_members, 1], col + '.')
    #    plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
    #             markeredgecolor='k', markersize=14)
    # plt.title('Estimated number of clusters: %d' % n_clusters_)
    # plt.show()

    # for dimension in cluster_center:   # 2 variables, plotted as x/y.  or # n_features
    #    print "THIS DIMENSION,", dimension

    return clusters_for_ea_sample


def train_model_and_pickle(n_train):
    """SAMPLE DATA, EXTRACT FEATURES, TRAIN MODEL"""

    profile_section = db.session.query(Profile.username, Profile.self_summary, Profile.message_me_if).all()

    # random_to_train = sample([item for item in profile_section], n_train)

    # random_profiles_to_train = [item[0] for item in random_to_train]

    # Profile.usernames have ~14,000
    # all_usernames = db.session.query(Profile.username).all()
    # return a list of 14,000 tuples, each tup[0] is username

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

    # print list(boolean_input_array_self_summary_train)
    # print list(boolean_input_array_message_me_if_train)

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
    """FOR EVERYTHING IN DATABASE, FIND AND SAVE LABELS"""

    # get a list of all usernames
    all_usernames_tuple = db.session.query(Profile.username).all()
    all_usernames = [profile[0] for profile in all_usernames_tuple]
    total_num_users = len(all_usernames)
    increment = 1000
    start = 0
    count_users_both_labels = 0
    len_to_input =0
    while start < total_num_users:
        end = start + increment
        print "start:", start
        print "end:", end
        get_users = all_usernames[start:end]
        profile_section = db.session.query(Profile.username, Profile.self_summary, Profile.message_me_if).filter(Profile.username.in_(get_users)).all()

        count, input_ = run_test_and_store(profile_section)
        count_users_both_labels += count
        len_to_input += input_
        start += increment

    print "SUCCESS - ALL USERS ARE LABELED"
    print "status: {}".format(float(count_users_both_labels)/len_to_input)

def print_cluster_words():

    ms_trained_object_self_summary = joblib.load('model_pkl/self_summary_pickle.pkl')
    ms_trained_object_message_me_if = joblib.load('model_pkl/message_me_if_pickle.pkl')

    features_self_summary = open('model_pkl/features_self_summary.txt').read().rstrip("|").split("|")
    features_message_me_if = open('model_pkl/features_message_me_if.txt').read().rstrip("|").split("|")

    self_summary_cluster_centers = ms_trained_object_self_summary.cluster_centers_
    message_me_if_cluster_centers = ms_trained_object_message_me_if.cluster_centers_

    zipped_self_summary = list(zip(features_self_summary, self_summary_cluster_centers))
    zipped_message_me_if = list(zip(features_message_me_if, message_me_if_cluster_centers))

    print "SELF SUMMARY: ", zipped_self_summary
    print "MESSAGE ME IF: ", zipped_message_me_if


def run_test_and_store(profile_section):

    ms_trained_object_self_summary = joblib.load('model_pkl/self_summary_pickle.pkl')
    ms_trained_object_message_me_if = joblib.load('model_pkl/message_me_if_pickle.pkl')

    features_self_summary = open('model_pkl/features_self_summary.txt').read().rstrip("|").split("|")
    features_message_me_if = open('model_pkl/features_message_me_if.txt').read().rstrip("|").split("|")


    count_users_both_labels = 0




    sample_list = profile_section


    # sample_list = profile_section[i*n : (i+1)*n]
    # print "LEN OF SAMPLE LIST SHOULD BE 1000:", len(sample_list)
    usernames = [item[0] for item in sample_list]

    # functions to attain labels for self_summary
    sample_list_self_summary = [item[1] for item in sample_list]
    boolean_input_array_self_summary = convert(features_self_summary, sample_list_self_summary)
    labels_self_summary = mean_shift_predict(boolean_input_array_self_summary, ms_trained_object_self_summary)

    # functions to attain labels for message_me_if
    sample_list_message_me_if = [item[2] for item in sample_list]
    print "preconvert"
    boolean_input_array_message_me_if = convert(features_message_me_if, sample_list_message_me_if)
    print "postconver"
    labels_message_me_if = mean_shift_predict(boolean_input_array_message_me_if, ms_trained_object_message_me_if)

    zipped =  zip(usernames, labels_self_summary, labels_message_me_if)
    to_input = list(zipped)
    for entry in to_input:
        # print "entry is", entry
        username, self_summary_label, message_me_if_label = entry
        new_input = MeanShiftAlgo(username=username, self_summary_label=self_summary_label, message_me_if_label=message_me_if_label)

        if self_summary_label > 1 and message_me_if_label > 1:
            count_users_both_labels +=1

        # db.session.add(new_input)

    print datetime.datetime.now()
     
    print "how many users are non-zero for both labels:", count_users_both_labels
    # db.session.commit()
    return count_users_both_labels, len(to_input)



if __name__ == "__main__":
    connect_to_db(app)
    
    # x = train_model_and_pickle(500)

    # test_data()
    print_cluster_words()