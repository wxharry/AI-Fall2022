import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-v', default=False, action='store_true',
                        help='Indicates verbose mode')

    parser.add_argument('-ab', default=False, action='store_true',
                        help='Indicates to use alpha-beta pruning (by default do not do A-B)')

    parser.add_argument('min/max', nargs=1, choices=['min', 'max'],
                        help='Specify whether the root player is min or max')

    parser.add_argument('graph-file', nargs=1,
                        help='Specify a graph file to read')

    args = parser.parse_args()
    return args



def main():
    args = parse_arguments()
    print(args)
if __name__ != "main":
    main()