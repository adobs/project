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

def get_words(location, n):
    """Gets word (by parsing text) out of database based on location parameter.

        Remove from list common words that appear above threshold (n) times
    """

    text_tuples = db.session.query(Profile.self_summary).filter(Profile.location == location).all()

    # returns a list of tuples
    words_and_count = {}

    features_set = set()

    for text in text_tuples:
        text_word_list = text[0].split(" ")
        # print "text word list", text_word_list

        clean = ""
        for word in text_word_list:
            word = word.replace("\n", " ").strip("\n\t1234567890!@#$%^&*()-=+{}[]/\\'\"<>?.,:;~`")
            clean += word+" "

        clean_list = clean.split(" ")
        
   
        for word in clean_list:
            words_and_count[word] = words_and_count.get(word,0)
            words_and_count[word] += 1
            # print "word is", word

    # print "words and count ", words_and_count

    for key, value in words_and_count.iteritems():
        # print key
        if value <= n:
            features_set.add(key)

    features = list(features_set)

    return [features, text_tuples]

def convert(features, text_tuples):
    """For each user, search features, and return list for each user

    1 if has feature, 0 if doesn't
    """

    print "features is", features 

    boolean_input = []

    for text in text_tuples:
        text_word_list = text[0].split(" ")
        # print "text word list", text_word_list

        clean = ""
        for word in text_word_list:
            word = word.replace("\n", " ").strip("\n\t1234567890!@#$%^&*()-=+{}[]/\\'\"<>?.,:;~`")
            clean += word+" "

        clean_list = clean.split(" ")
        user = []
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

def mean_shift(boolean_input_array, quantile):

    n_samples, n_features = boolean_input_array.shape
    seeds = boolean_input_array.shape
    X = boolean_input_array
    # for idx, line in enumerate(input):
    #    if(len(line) == ''):
    #        continue;
    #    line = line.strip()
    #    tmpNumPy = np.array([line])
    #    print tmpNumPy
    #    example = np.append(example, tmpNumPy)

    # Compute clustering with MeanShift

    # The following bandwidth can be automatically detected using
    bandwidth = estimate_bandwidth(X, quantile=quantile, n_samples=n_samples)
    
    print "bandwith is", bandwidth

    ms = MeanShift(bandwidth=12)
    ms.fit(X)
    labels = ms.labels_
    cluster_centers = ms.cluster_centers_

    # print "cluster centers", list(cluster_centers)

    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)

    # print "unique labels:", labels_unique
    # print "labels:", labels
    print "number of estimated clusters : %d" % n_clusters_

    import matplotlib.pyplot as plt
    from itertools import cycle

    plt.figure(1)
    plt.clf()

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


if __name__ == "__main__":
    connect_to_db(app)
    
    features, text_tuples = get_words("Berkeley, CA", 100)
    boolean_input_array = convert(features, text_tuples)
    mean_shift(boolean_input_array, 0.2)
