
import os



if __name__ == '__main__':
    print(" ======== test knn1.e2.3")
    os.system("python3 learn.py -train data/knn1.train.txt -test data/knn1.test.txt -K 3 > output")
    os.system("diff output data/knn1.e2.3.out.txt")
    os.system("rm output")

    print(" ======== test knn2.e2.3")
    os.system("python3 learn.py -train data/knn2.train.txt -test data/knn2.test.txt -K 3 > output")
    os.system("diff output data/knn2.e2.3.out.txt")
    os.system("rm output")