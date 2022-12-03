
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
    
    print(" ======== test km1.e2")
    os.system("python3 learn.py -train data/km1.txt 0,0 200,200 500,500 > output")
    os.system("diff output data/km1.e2.out.txt")
    os.system("rm output")

    print(" ======== test km1.manh")
    os.system("python3 learn.py -train data/km1.txt -d manh 0,0 200,200 500,500 > output")
    os.system("diff output data/km1.manh.out.txt")
    os.system("rm output")

    print(" ======== test km2.e2")
    os.system("python3 learn.py -train data/km2.txt 0,0,0 200,200,200 500,500,500 > output")
    os.system("diff output data/km2.e2.out.txt")
    os.system("rm output")

    print(" ======== test km2.manh")
    os.system("python3 learn.py -train data/km2.txt -d manh 0,0,0 200,200,200 500,500,500 > output")
    os.system("diff output data/km2.manh.out.txt")
    os.system("rm output")
