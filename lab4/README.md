# Lab4

Assignment
Write a program demonstrating two supervised learning algorithms: kNN and Naive Bayes'

The two algorithms do not need to share anything in common, but you may wish to do so for the evaluation portion.

Extra Credit: also code the kMeans clustering algorithm in the same program.

## Usage
``` bash
> python3 learn.py -h
usage: learn.py [-h] [-v] [-train TRAIN] [-test TEST] [-K K] [-C C] [-d {e2,manh}] [centroids ...]

positional arguments:
  centroids     if a list of centroids is provided those should be used for kMeans

options:
  -h, --help    show this help message and exit
  -v            Indicates verbose mode, default to False
  -train TRAIN  the training file
  -test TEST    the testing data file
  -K K          if > 0 indicates to use kNN and also the value of K (if 0, do Naive Bayes')
  -C C          if > 0 indicates the Laplacian correction to use (0 means don't use one)
  -d {e2,manh}  indicating euclidean distance squared or manhattan distance to use
```

## Examples

1. knn
``` bash
python3 learn.py -train data/knn1.train.txt -test data/knn1.test.txt -K 3
```
2. naive bayes
``` bash
python3 learn.py -train data/ex1_train.csv -test data/ex1_test.csv -C 1
```
3. k means
``` bash
python3 learn.py -train data/km1.txt -d manh 0,0 200,200 500,500
```