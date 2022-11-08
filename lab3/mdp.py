"""
author: Xiaohan Wu
NYU ID: xw2788
email: xiaohanwu12@gmail.com
"""
from math import inf
import argparse

VERBOSE = False

def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-df', default=1.0,
                        help='a float discount factor [0, 1] to use on future rewards, defaults to 1.0 if not set')
    parser.add_argument('-min', default=False, action='store_true',
                        help='minimize values as costs, defaults to false which maximizes values as rewards')
    parser.add_argument('-tol', default=0.01, 
                        help='a float tolerance for exiting value iteration, defaults to 0.01')
    parser.add_argument('-iter', default=100, 
                        help='an integer that indicates a cutoff for value iteration, defaults to 100')
    parser.add_argument('-v', default=False, action='store_true',
                        help='Indicates verbose mode')
    parser.add_argument('input-file', 
                        help='Specify a input file to read')

    args = parser.parse_args()
    return dict(args._get_kwargs())

def read_input(filename):
    """
    Node/state names should be alphanumeric

    The input file consists of 4 types of input lines:

    * Comment lines that start with # and are ignored (as are blanklines)
    * Rewards/costs lines of the form 'name = value' where value is an integer
    * Edges of the form 'name : [e1, e2, e2]' where each e# is the name of an out edge from name
    * Probabilities of the form 'name % p1 p2 p3' (more below)
    """
    graph = {}
    probabilities = {}
    rewards = {}
    with open(filename, "r", encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#') or line == '\n':
                continue
            elif '=' in line:
                name, val = line.split('=')
                rewards[name] = eval(val)
            elif ':' in line:
                name, lst = line.split(' : ')
                if not name.isalnum():
                    print("[ERROR] variables should be alpha or number")
                    exit(1)
                graph[name] = lst[1:-1].replace(' ', '').split(',')
            elif '%' in line:
                name, probs = line.split(' % ')
                # TBD: if not decision node, check if the probabilities have a sum of 1
                probabilities[name] = list(map(eval, probs.split(' ')))
    return graph, probabilities, rewards

def is_cyclic(graph):
    """
    determines if given graph is acyclic.
    returns entries if it acyclic; empty set if it contains a cycle.
    """
    parents = {k for k in graph.keys()}
    children = {v for lst in graph.values() for v in lst}
    entries = parents - children
    if not len(entries):
        return entries
    
    # if there is some entries
    # applied from GeeksforGeeks https://www.geeksforgeeks.org/detect-cycle-in-a-graph/
    V = parents | children
    visited = {v: False for v in V}
    recStack = {v: False for v in V}
    for node in V:
        if visited[node] == False:
            if is_cyclic_util(graph, node, visited, recStack):
                return set()
    return entries

def is_cyclic_util(graph, v, visited, recStack):
    """
    helper function for is_cyclic
    """
    # Mark current node as visited and
    # adds to recursion stack
    visited[v] = True
    recStack[v] = True

    # Recur for all neighbors
    # if any neighbor is visited and in
    # recStack then graph is cyclic
    for neighbor in graph.get(v, []):
        if visited[neighbor] == False:
            if is_cyclic_util(graph, neighbor, visited, recStack) == True:
                return True
        elif recStack[neighbor] == True:
            return True

    # The node needs to be popped from
    # recursion stack before function ends
    recStack[v] = False
    return False

def backwards_induction(graph, probabilities, rewards, entries):
    """
    solves acyclic graph in decision tree ways (could be DAG)
    if decision node, returns the maximum expectation from the children;
    if chance node, returns the expectation
    if terminal, return rewards
    """
    for node in entries:
        rewards[node] = backwards_induction_helper(graph, probabilities, rewards, node)
    


def backwards_induction_helper(graph, probabilities, rewards, node):
    """
    helper function for backwards_induction
    """
    # if a terminal 
    if not graph.get(node):
        return rewards.get(node, 0)
    else:
        # if a decision node
        if probabilities.get(node) == None or len(probabilities[node]) == 1:
            max_v = -inf
            choice = None
            for child in graph[node]:
                _v = backwards_induction_helper(graph, probabilities, rewards, child)
                if _v > max_v:
                    max_v = _v
                    choice = child
            print(f"{node}->{choice}")
            rewards[node] = max_v
            return max_v
        # if a chance node
        else:
            expectation = rewards.get(node, 0)
            for p, child in zip(probabilities[node], graph[node]):
                expectation += p * backwards_induction_helper(graph, probabilities, rewards, child)
            rewards[node] = expectation
            return expectation

def markov_process_solver():
    """
    used for graphs with cycles
    """
    pi = initial_policy()
    v = initial_values()
    while True:
        v = value_iteration(pi)
        _pi = greedy_policy_computation(v)
        if pi == _pi:
            return pi, v
        pi = _pi

def initial_policy():
    pass

def initial_values():
    pass

def value_iteration(pi):
    """
    computes a transition matrix using a fixed policy
    then iterates by recomputing values for each node using the previous values until either:
    * no value changes by more than the 'tol' flag,  
    * or -iter iterations have taken place.  
    """
    pass

def greedy_policy_computation(v):
    """
    uses the current set of values to compute a new policy. If -min is not set, the policy is chosen to maximize rewards; if -min is set, the policy is chosen to minimize costs.
    """
    pass

def main():
    args = parse_arguments()
    global VERBOSE
    VERBOSE = args['v']
    # get input
    graph, probabilities, rewards = read_input(args['input-file'])
    print(graph)
    print(probabilities)
    print(rewards)
    # if acyclic
    entries = is_cyclic(graph)
    # run Backwards induction if no
    if len(entries):
        # backwards induction
        backwards_induction(graph, probabilities, rewards, entries)
        print(sorted(rewards.items(), key=lambda x: x[0]))
    # run MDP solver
    else:
        markov_process_solver()


if __name__ == "__main__":
    main()
