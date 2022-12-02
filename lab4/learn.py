"""
author: Xiaohan Wu
NYU ID: xw2788
email: xw2788@nyu.edu
"""
import argparse
import csv
from knn import *

def parse_arguments(default_verbose=False, default_distance='e2'):
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-v', default=default_verbose, action='store_true',
                        help=f'Indicates verbose mode, default to {default_verbose}')
    parser.add_argument('-train', 
                        help="the training file")
    parser.add_argument('-test', 
                        help="the testing data file")
    parser.add_argument('-K', default=0, type=int,
                        help="if > 0 indicates to use kNN and also the value of K (if 0, do Naive Bayes')")
    parser.add_argument('-C', default=0,
                        help="if > 0 indicates the Laplacian correction to use (0 means don't use one)")
    parser.add_argument('-d', choices={'e2', 'manh'}, default=default_distance,
                        help="indicating euclidean distance squared or manhattan distance to use")
    parser.add_argument("-c", default=[],
                        help="if a list of centroids is provided those should be used for kMeans")

    args = parser.parse_args()
    if args.K > 0 and args.C > 0:
        print("ERROR: K and C cannot both be greater than zero")
        exit(1)
    return dict(args._get_kwargs())

def read_input(filename):
    """
    read csv file as an input
    """
    data = []
    with open(filename, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            data.append([int(ele) for ele in row[:-1]] + [row[-1]])
    return data

def evaluation(answer, system):
    domain = set(answer) | set(system)
    for x, y in zip(answer, system):
        print(f"want={x} got={y}")

    for label in sorted(list(domain)):
        true_positive = 0
        false_positive = 0
        false_negative = 0
        for x, y in zip(answer, system):
            if y == label and x == y:
                true_positive += 1
            elif y == label and x != y:
                false_positive += 1
            elif x == label and x != y:
                false_negative += 1
        print(f"Label={label} "
                f"Precision={true_positive}/{(true_positive + false_positive)} "
                f"Recall={true_positive}/{(true_positive + false_negative)}")

def main():
    args = parse_arguments()
    train_data = read_input(args['train'])
    test_data = read_input(args['test'])
    prediction = []
    for test in test_data:
        r = KNN(train_data, test, args['K'])
        prediction.append(r)
    
    evaluation([row[-1] for row in test_data], prediction)


if __name__ == "__main__":
    main()

