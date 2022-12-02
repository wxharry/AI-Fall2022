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
    For example of there are 3 predictive attributes: D(1, y1, z1>, 2,y2, z2>) = (z2-z1)2 + (y2-y1)2 + (x2-x1)2
    You then compare the predicted label to the actual one and record for later metrics.
    """
    dist = []
    *test_v, test_label = test
    target = Point(test_v)
    for *vec, label in train:
        p = Point(vec)
        dist.append((target.e2distance(p), label))
    dist = sorted(dist, key=lambda x: x[0])
    # print(dist[:k])
    vote = {}
    for d, l in dist[:k]:
        vote[l] = vote.get(l, 0) + 1
    # print(vote)
    return max(vote.items(), key=lambda x: x[1])[0]

