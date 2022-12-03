"""
author: Xiaohan Wu
NYU ID: xw2788
email: xw2788@nyu.edu
"""
from point import *

def KNN(train, test, k, **kwargs):
    """
    kNN (using euclidean distance-squared, weighted)
    For k-nearest neighbor, there is no training, you just parse and load the file into memory, then use it for classification.
    As discussed in class, for each each test point you compute the distance to each training point, picking the K nearest ones and they then
    "vote" on the classification using a weight of 1 over the distance.  For distance we will use euclidean squared between two points:
    For example of there are 3 predictive attributes: D(x1, y1, z1, x2,y2, z2) = (z2-z1)2 + (y2-y1)2 + (x2-x1)2
    You then compare the predicted label to the actual one and record for later metrics.
    """
    dist = []
    *test_v, test_label = test
    target = Point(test_v)
    # calculate e2 distance for each point
    for *vec, label in train:
        p = Point(vec)
        dist.append((target.e2distance(p), label))
    # sort the distances and get the k nearest points
    dist = sorted(dist, key=lambda x: x[0])[:k]

    vote = {}
    # vote with a vote function to predict
    for d, l in dist:
        vote_function = lambda d: 1 / (d+1)
        vote[l] = vote.get(l, 0) + vote_function(d)
    return max(vote.items(), key=lambda x: x[1])[0]


def naive_bayes_train(train, laplacian=0, **kwargs):
    """
    For training you should load the training file into memory,
    but then compute all of the conditional and pure probabilities in advance
    (including laplacian smoothing if applicable).
    Then when doing predictions on the test file,
    you do the argmax as per class to predict a label,
    recording versus the actual one for later metrics.
    """

    # count the frequencies of all labels and (feature, label) pair
    label_freq = {}
    feature_freq = {}
    for line in train:
        *features, label = line
        label_freq[label] = label_freq.get(label, 0) + 1
        for idx, feature in enumerate(features):
            feature_freq[((idx, feature), label)] = feature_freq.get(((idx, feature), label), 0) + 1
    
    # calculate the probabilities of labels and conditional probabilities for (feature, label) pair
    domain_number = len(label_freq)
    probabilities = {}
    for label in label_freq:
        probabilities[label] = label_freq[label] / sum(label_freq.values())
        for feature, condition in feature_freq:
            if condition == label:
                probabilities[(feature, condition)] = (feature_freq[(feature, label)] + laplacian) / (label_freq[label] + domain_number * laplacian)
    return {
        "probabilities": probabilities,
        "labels": label_freq.keys(),
        "laplacian": laplacian
    }

def naive_bayes_predict(test, model):
    *features, label = test
    probabilities = model['probabilities']
    possibility = {}
    for label in model['labels']:
        possibility[label] = probabilities[label]
        for idx, feature in enumerate(features):
            possibility[label] *= probabilities.get(((idx,feature), label), 0)
    predict = max(possibility.items(), key=lambda x: x[1])
    return predict[0]
                
    