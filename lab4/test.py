
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

    print(" ======== test knn3.e2.3")
    os.system("python3 learn.py -train data/knn3.train.txt -test data/knn3.test.txt -K 3 > output")
    os.system("diff output data/knn3.e2.3.out.txt")
    os.system("rm output")

    print(" ======== test knn3.e2.5")
    os.system("python3 learn.py -train data/knn3.train.txt -test data/knn3.test.txt -K 5 > output")
    os.system("diff output data/knn3.e2.5.out.txt")
    os.system("rm output")

    print(" ======== test knn3.e2.7")
    os.system("python3 learn.py -train data/knn3.train.txt -test data/knn3.test.txt -K 7 > output")
    os.system("diff output data/knn3.e2.7.out.txt")
    os.system("rm output")

    print(" ======== test nb1.0")
    os.system("python3 learn.py -train data/ex1_train.csv -test data/ex1_test.csv > output")
    os.system("diff output data/nb1.0.out")
    os.system("rm output")

    print(" ======== test nb1.1")
    os.system("python3 learn.py -train data/ex1_train.csv -test data/ex1_test.csv -C 1 > output")
    os.system("diff output data/nb1.1.out")
    os.system("rm output")

    print(" ======== test nb2.0")
    os.system("python3 learn.py -train data/ex2_train.csv -test data/ex2_test.csv > output")
    os.system("diff output data/nb2.0.out")
    os.system("rm output")

    print(" ======== test nb2.1")
    os.system("python3 learn.py -train data/ex2_train.csv -test data/ex2_test.csv -C 1 > output")
    os.system("diff output data/nb2.1.out")
    os.system("rm output")

    print(" ======== test nb2.2")
    os.system("python3 learn.py -train data/ex2_train.csv -test data/ex2_test.csv -C 1 > output")
    os.system("diff output data/nb2.2.out")
    os.system("rm output")
