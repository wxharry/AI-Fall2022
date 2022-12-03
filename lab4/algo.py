"""
author: Xiaohan Wu
NYU ID: xw2788
email: xw2788@nyu.edu
"""
from copy import deepcopy
from random import choices
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
                

def kMeans(data, k, centroids=[], dist_type='e2', max_iter=100):
    """
    K is inferred from the number of centroids provides.
    """
    features = []
    labels = []
    for line in data:
        *v, l = line
        features.append(v)
        labels.append(l)
    # check distance type
    if dist_type not in ['e2', 'manh']:
        raise Exception(f"only support dist_type strings as ['e2', 'manh], given {dist_type}")

    # check dimensions
    dimension = len(features[0])
    for point in list(features + centroids):
        if len(point) != dimension:
            raise Exception(f"All the points should have the same dimension, found{point}")

    # randomly pick 3 points from the input
    if len(centroids) == 0:
        centroids = choices(features, k=3)
    # make all points to be point object
    features = {l: Point(v, l) for v, l in zip(features, labels)}
    centroids = {f'C{idx+1}': Point(c, f"C{idx+1}") for idx, c in enumerate(centroids)}
    while max_iter:
        centroids_copy = deepcopy(centroids)
        distances = {}
        for cnum, centroid in centroids.items():
            for fnum, feature in features.items():
                if dist_type == 'e2':
                    distances[fnum] = distances.get(fnum, []) + [(cnum, centroid.e2distance(feature))]
                if dist_type == 'manh':
                    distances[fnum] = distances.get(fnum, []) + [(cnum, centroid.manhdistance(feature))]
        # assign all points to the closest centroids
        assignment = {}
        for fnum, dists in distances.items():
            cnum = min(dists, key=lambda x: x[1])[0]
            assignment[cnum] = assignment.get(cnum, []) + [features[fnum]]
        
        # calculate the mean centroids
        new_centroids = {}
        for cnum in centroids:
            zero = Point([0 for _ in range(dimension)])
            points = assignment.get(cnum, [zero])
            new_centroids[cnum] = sum(points, zero) / len(points)
        if new_centroids == centroids_copy:
            break
        centroids = new_centroids

        max_iter -= 1

    for c in sorted(assignment):
        print(f"{c} = "
            + "{"
            + f"{','.join([x.name for x in assignment[c]])}"
            + "}"
            )
    for cent in sorted(centroids):
        print(f"([{' '.join([str(num) for num in centroids[cent].vector])}])")

    return (assignment, centroids)

