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
    return dict(args._get_kwargs())

def read_input(filename):
    graph = dict()
    with open(filename, "r", encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip().replace(' ', '')
            if ':' in line:
                parent, children = line.split(':')
                graph[parent] = eval(children.replace('[', '["').replace(',', '","').replace(']', '"]'))
            elif '=' in line:
                terminal, value = line.split("=")
                graph[terminal] = value
    return graph

def main():
    args = parse_arguments()
    graph = read_input(args['graph-file'][0])
    print(graph)

if __name__ != "main":
    main()