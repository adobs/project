# take text data per user, and parse on each word. list of words.
# unique set(list of words).
# remove from set any words that are in your common_words
# convert into a list of booleans:
# 
#WHAT IS QUANTILE
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
# from sklearn.datasets.samples_generator import make_blobs
from model import Profile, Adjective, Gender, Orientation, Location, db, connect_to_db
from flask_app import app
from random import sample

def clean(dirty_list):
    print "dirty list is", dirty_list
    clean_list = []
    clean_string = ""
    for word in dirty_list:
        print "\nword is ", word
        word = word.strip("\n\t1234567890!@#$%^&*()-=+{}[]/\\'\"<>?.,:;~`").replace("\n", " ")
        clean_string += word+" "

    # print "clean string is", clean_string

    clean_list.extend(clean_string.split(" "))

    print "clean list is", clean_list
    return clean_list


def get_words(profile, threshold):
    """Gets word (by parsing text) out of database based on random samples.

        Remove from list common words that appear above threshold (n) times.
        Returns a randomly generate list of features.
    """
   
    text_tuples = db.session.query(profile).limit(30).all()
    print "text_tuples is", text_tuples
    # returns a list of tuples
    words_and_count = {}

    features_set = set()

    text_word_list = []
    for text in text_tuples:
        print "text is ", text
        text_word_list.extend(text[0].split(" "))
        print "text wor list is", text_word_list
        # print "text word list", text_word_list
    
    clean_list = clean(text_word_list)

    for word in clean_list:
        words_and_count[word] = words_and_count.get(word,0)
        words_and_count[word] += 1
            # print "word is", word

    # print "words and count ", words_and_count

    for key, value in words_and_count.iteritems():
        # print key
        if value <= threshold:
            features_set.add(key)

    features = list(features_set)

    print "for", profile, "the features are", features

    return features


def convert(features, text_list):
    """For each user, search features, and return numpy boolean array for each user

    1 if has feature, 0 if doesn't
    """

    print "features is", features 

    boolean_input = []

    for text in text_list:
        print "text in text list is", text
        # import pdb; pdb.set_trace()

        user = []
        clean_list = clean(text.split(" "))
        for feature in features:
            if feature in clean_list:
                user.append(1)
            else:
                user.append(0)

        boolean_input.append(user)

    boolean_input_array = np.array(boolean_input, dtype=int)

    print "shape of the array is", boolean_input_array.shape
    shape = boolean_input_array.shape
        # for i in range(shape[0]):
        # print "total non-0s", sum(boolean_input_array[i])

    # X : array-like, shape=[n_samples, n_features]
    # Input points.
    # quantile : float, default 0.3
    return boolean_input_array

def mean_shift_train(boolean_input_array, bandwidth):
    """Conduct mean shift analysis on training data."""

    n_samples, n_features = boolean_input_array.shape
    seeds = boolean_input_array.shape
    X = boolean_input_array

    # The following bandwidth can be automatically detected using
    # bandwidth = estimate_bandwidth(X, quantile=quantile, n_samples=n_samples)
    
    # print "bandwith is", bandwidth

    ms = MeanShift(bandwidth=bandwidth)
    ms.fit(X)
    labels = ms.labels_
    cluster_centers = ms.cluster_centers_

    # print "cluster centers", list(cluster_centers)

    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)

    # print "unique labels:", labels_unique
    # print "labels:", labels
    print "number of estimated clusters : %d" % n_clusters_

    # import matplotlib.pyplot as plt
    from itertools import cycle

    # plt.figure(1)
    # plt.clf()

    colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
    # colors is an iterator....never runs out, so the zip should be fine

    # print list(labels)
    # print set(labels)

    for k, col in zip(range(n_clusters_), colors):
       print
       my_members = labels == k
       # print my_members
       print "\nk", k    # number of clusters
       cluster_center = cluster_centers[k]     # len of cluster_center == n_features
       print "cluster_center", cluster_center   # [-0.95635942 -1.01166653]
       print "len is ok", len(cluster_center) == n_features
       print "min of all dimensions:", min(cluster_center)
       print "max of all dimensions:", max(cluster_center)
       print "average of all dimensions:", float(sum(cluster_center))/n_features




    #    plt.plot(X[my_members, 0], X[my_members, 1], col + '.')
    #    plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
    #             markeredgecolor='k', markersize=14)
    # plt.title('Estimated number of clusters: %d' % n_clusters_)
    # plt.show()

    # for dimension in cluster_center:   # 2 variables, plotted as x/y.  or # n_features
    #    print "THIS DIMENSION,", dimension
    print "done with MS train"
    return ms

def mean_shift_predict(boolean_input_array, ms):
    """Conduct mean shift analysis predictions on unlabeled data."""

    n_samples, n_features = boolean_input_array.shape
    seeds = boolean_input_array.shape
    X = boolean_input_array

    # The following bandwidth can be automatically detected using
    # bandwidth = estimate_bandwidth(X, quantile=quantile, n_samples=n_samples)
    
    # print "bandwith is", bandwidth

    labels = ms.fit_predict(X)
    # labels = ms.labels_
    cluster_centers = ms.cluster_centers_

    # print "cluster centers", list(cluster_centers)

    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)

    print "unique labels:", labels_unique
    print "labels:", labels
    print "number of estimated clusters : %d" % n_clusters_

    # import matplotlib.pyplot as plt
    from itertools import cycle

    # plt.figure(1)
    # plt.clf()

    colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
    # colors is an iterator....never runs out, so the zip should be fine

    # print list(labels)
    # print set(labels)

    for k, col in zip(range(n_clusters_), colors):
       print
       my_members = labels == k
       # print my_members
       print "\nk", k    # number of clusters
       cluster_center = cluster_centers[k]     # len of cluster_center == n_features
       print "cluster_center", cluster_center   # [-0.95635942 -1.01166653]
       print "len is ok", len(cluster_center) == n_features
       print "min of all dimensions:", min(cluster_center)
       print "max of all dimensions:", max(cluster_center)
       print "average of all dimensions:", float(sum(cluster_center))/n_features




    #    plt.plot(X[my_members, 0], X[my_members, 1], col + '.')
    #    plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
    #             markeredgecolor='k', markersize=14)
    # plt.title('Estimated number of clusters: %d' % n_clusters_)
    # plt.show()

    # for dimension in cluster_center:   # 2 variables, plotted as x/y.  or # n_features
    #    print "THIS DIMENSION,", dimension

    return labels


def parse_all_data(n):

    profile_section = db.session.query(Profile.username, Profile.self_summary, Profile.message_me_if).all()

    print "1"
    features_self_summary = get_words(Profile.self_summary, 1000)
    features_message_me_if = get_words(Profile.message_me_if, 1000)


    print "2"
    text_list_self_summary_train = sample([item[1] for item in profile_section], n)
    # import pdb; pdb.set_trace()

    print "text_list_self_summary_train", text_list_self_summary_train
    text_list_message_me_if_train = sample([item[2] for item in profile_section], n)
    print "3"
    boolean_input_array_self_summary_train = convert(features_self_summary, text_list_self_summary_train)
    boolean_input_array_message_me_if_train = convert(features_message_me_if, text_list_message_me_if_train)
    print "4"
    ms_trained_object_self_summary = mean_shift_train(boolean_input_array_self_summary_train, 12)
    ms_trained_object_message_me_if = mean_shift_train(boolean_input_array_message_me_if_train, 12)

    i = 0

    # go through all my data, iterate slices in chunks of size n
    while (len(profile_section) > i*n):
        print "i is", i
        sample_list = profile_section[i*n : (i+1)*n]
        usernames = [item[0] for item in sample_list]

        # functions to attain labels for self_summary
        sample_list_self_summary = [item[1] for item in sample_list]
        print "sample list ", sample_list_self_summary
        boolean_input_array_self_summary = convert(features_self_summary, sample_list_self_summary)
        labels_self_summary = mean_shift_predict(boolean_input_array_self_summary, ms_trained_object_self_summary)


        # functions to attain labels for message_me_if
        sample_list_message_me_if = [item[2] for item in sample_list]
        print "sample message is", sample_list_message_me_if
        #
        boolean_input_array_message_me_if = convert(features_message_me_if, sample_list_message_me_if)
        labels_message_me_if = mean_shift_predict(boolean_input_array_message_me_if, ms_trained_object_message_me_if)

        zipped =  zip(usernames, labels_self_summary, labels_message_me_if)
        to_input = list(zipped)
        print "to input :", to_input
        for entry in to_input:
            for username, self_summary_label, message_me_if_label in entry:
                new_input = MeanShift(username=username, self_summary_label=self_summary_label, message_me_if_label=message_me_if_label)

                db.session.add(new_input)

        i+=1

    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)
    
    parse_all_data(3000)
