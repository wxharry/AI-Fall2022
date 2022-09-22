import argparse
from math import inf

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
                graph[terminal] = eval(value)
    return graph

def find_root(graph):
    parents = set()
    children = set()
    for k, v in graph.items():
        if isinstance(v, list):
            for node in v:
                children.add(node)
            parents.add(k)
        elif isinstance(v, int):
            parents.add(k)
    return  parents - children

def minimax_helper(s, maxTurn, graph, alpha=None, beta=None, verbose=False):
    choice = None
    if isinstance(graph[s], int):
        return choice, graph[s]
    if maxTurn:
        v = - inf
        for c in graph[s]:
            [_choice, _v] = minimax_helper(c, not maxTurn, graph, alpha, beta, verbose)
            if verbose and _choice:
                print(f"min({c}) chooses {_choice} for {_v}")
            if _v >= v:
                v = _v
                choice = c
            if beta != None and _v > beta:
                return None, v
            if alpha != None and _v > alpha:
                alpha = _v
        return choice, v
    else:
        v = inf
        for c in graph[s]:
            [_choice, _v] = minimax_helper(c, not maxTurn, graph, alpha, beta, verbose)
            if verbose and _choice:
                print(f"max({c}) chooses {_choice} for {_v}")
            if _v <= v:
                v = _v
                choice = c
            if alpha != None and _v < alpha:
                return None, v
            if beta != None and _v < beta:
                beta = _v
        return choice, v

def minimax(s, maxTurn, graph, ab, verbose=False):
    if ab:
        [choice, v] = minimax_helper(s, maxTurn, graph, -inf, inf, verbose=verbose)
    else:
        [choice, v] = minimax_helper(s, maxTurn, graph, verbose=verbose)
    print(f"{'max' if maxTurn else 'min'}({s}) chooses {choice} for {v}")
    

def main():
    args = parse_arguments()
    graph = read_input(args['graph-file'][0])
    root = find_root(graph)
    minimax(list(root)[0], args['min/max'][0] == 'max', graph, args['ab'], verbose=args['v'])

if __name__ == "__main__":
    main()