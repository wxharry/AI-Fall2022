"""
author: Xiaohan Wu
NYU ID: xw2788
email: xiaohanwu12@gmail.com
"""
from math import inf
import argparse

def parse_arguments(discount_factor=1.0, min_value=False, tolerance=0.01, max_iteration=100, verbose=False):
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-df', default=discount_factor, type=float,
                        help=f'a float discount factor [0, 1] to use on future rewards, defaults to {discount_factor} if not set')
    parser.add_argument('-min', default=min_value, action='store_true',
                        help=f'minimize values as costs, defaults to {min_value} which {"minimizes" if min_value else "maximizes"} values as rewards')
    parser.add_argument('-tol', default=tolerance, type=float,
                        help=f'a float tolerance for exiting value iteration, defaults to {tolerance}')
    parser.add_argument('-iter', default=max_iteration, type=int,
                        help=f'an integer that indicates a cutoff for value iteration, defaults to {max_iteration}')
    parser.add_argument('-v', default=verbose, action='store_true',
                        help=f'Indicates verbose mode, default to {verbose}')
    parser.add_argument('input-file', 
                        help='Specify a input file to read')

    args = parser.parse_args()
    return dict(args._get_kwargs())

def read_input(filename, **kwargs):
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
                name, val = name.strip(), val.strip()
                rewards[name] = eval(val)
            elif ':' in line:
                name, lst = line.split(':')
                name, lst = name.strip(), lst.strip()
                if not name.isalnum():
                    print("[ERROR] variables should be alpha or number")
                    exit(1)
                graph[name] = lst[1:-1].replace(' ', '').split(',')
            elif '%' in line:
                name, probs = line.split('%')
                name, probs = name.strip(), probs.strip()
                # if not decision node, check if the probabilities have a sum of 1
                probabilities[name] = list(map(eval, probs.split(' ')))
                if len(probabilities[name]) > 1 and abs(sum(probabilities[name]) - 1) > kwargs['tol']:
                    print("ERROR: probabilities of a chance node should have a sum of 1")
                    exit(1)
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
        if not visited[node]:
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
            if is_cyclic_util(graph, neighbor, visited, recStack):
                return True
        elif recStack[neighbor]:
            return True

    # The node needs to be popped from
    # recursion stack before function ends
    recStack[v] = False
    return False

def backwards_induction(graph, probabilities, rewards, entries, **kwargs):
    """
    solves acyclic graph in decision tree ways (could be DAG)
    if decision node, returns the maximum expectation from the children;
    if chance node, returns the expectation
    if terminal, return rewards
    """
    values = {}
    pi = {}
    for node in entries:
        backwards_induction_helper(graph, probabilities, rewards, node, values, pi, **kwargs)
    return pi, values


def backwards_induction_helper(graph, probabilities, rewards, node, values, pi, **kwargs):
    """
    helper function for backwards_induction
    """
    # if a terminal 
    if not graph.get(node):
        values[node] = rewards.get(node, 0)
        return rewards.get(node, 0)
    else:
        # if a decision node
        if probabilities.get(node) == None or len(probabilities[node]) == 1:
            choice_v = -inf if not kwargs['min'] else inf
            choice = None
            for child in graph[node]:
                _v = backwards_induction_helper(graph, probabilities, rewards, child, values, pi, **kwargs)
                if not kwargs['min'] and _v > choice_v:
                    choice_v = _v
                    choice = child
                if kwargs['min'] and _v < choice_v:
                    choice_v = _v
                    choice = child
            values[node] = choice_v
            pi[node] = choice
            return choice_v
        # if a chance node
        else:
            expectation = rewards.get(node, 0)
            for p, child in zip(probabilities[node], graph[node]):
                expectation += p * backwards_induction_helper(graph, probabilities, rewards, child, values, pi, **kwargs)
            values[node] = expectation
            return expectation

def markov_process_solver(graph, probabilities, rewards, **kwargs):
    """
    used for graphs with cycles
    """
    pi = initial_policy(graph, probabilities)
    values = initial_values(graph, rewards)
    while True:
        values = value_iteration(graph, probabilities, values, pi, rewards, **kwargs)
        _pi = greedy_policy_computation(graph, values, pi, **kwargs)
        if pi == _pi:
            return pi, values
        pi = _pi

def initial_policy(graph, probabilities):
    """
    initializes an arbitrary policy for each decision node in the graph
    arbitrarily pick the first one in its neighbor as the next state
    """
    policy = {}
    for current, neighbor in graph.items():
        # if current state is a decision node
        # a decision node should have only one probability
        # if a node only has one neighbor it always transits to, it is not considered as a decision node
        if len(probabilities.get(current, [1.0])) == 1 and len(neighbor) > 1:
            policy[current] = neighbor[0]
    return policy

def initial_values(graph, rewards):
    """
    initial values with rewards
    """
    values = {}
    parents = {k for k in graph.keys()}
    children = {v for lst in graph.values() for v in lst}
    V = parents | children
    for s in V:
        values[s] = rewards.get(s, 0)
    return dict(sorted(values.items(), key= lambda x: x[0]))

def value_iteration(graph, probabilities, values, pi, rewards, **kwargs):
    """
    computes a transition matrix using a fixed policy
    then iterates by recomputing values for each node using the previous values until either:
    * no value changes by more than the 'tol' flag,  
    * or -iter iterations have taken place.  
    """
    iter = 0
    new_values = {}
    while True:
        new_values = {}
        for node in values:
            exp = 0
            # if a decision node
            if pi.get(node):
                for neighbor in graph[node]:
                    # if neighbor is identical to the policy
                    if neighbor == pi[node]:
                        exp += round(probabilities.get(node, [1.0])[0] * values[neighbor], 4)
                    else:
                        exp += round((1 - probabilities.get(node, [1.0])[0])/(len(graph[node])-1) * values[neighbor], 4)
            # else if a terminal
            elif not graph.get(node):
                new_values[node] = rewards.get(node, 0)
                continue
            # else if a transition node, which has one child and has one or no probability
            else:
                for p, v in zip(probabilities.get(node, [1]), graph[node]):
                    exp += round(p * values[v], 4)
            new_values[node] = round(rewards.get(node, 0) + kwargs['df'] * exp, 4)
        # break out condition
        tolerance = max([abs(new_values[node] - values[node]) for node in values])
        if tolerance < kwargs['tol'] or iter >= kwargs['iter']:
            return new_values
        values = new_values
        iter += 1
    return new_values

def greedy_policy_computation(graph, values, pi, **kwargs):
    """
    uses the current set of values to compute a new policy. If -min is not set, the policy is chosen to maximize rewards; if -min is set, the policy is chosen to minimize costs.
    """
    new_pi = {}
    for current, next in pi.items():
        choice_v = values[current]
        choice = next
        for option in graph[current]:
            if not kwargs['min'] and values[option] > choice_v:
                choice = option
                choice_v = values[option]
            if kwargs['min'] and values[option] < choice_v:
                choice = option
                choice_v = values[option]
        new_pi[current] = choice
    return new_pi

def main():
    args = parse_arguments()
    # get input
    graph, probabilities, rewards = read_input(args['input-file'], **args)
    # if acyclic
    entries = is_cyclic(graph)
    # run Backwards induction if no
    if len(entries):
        # backwards induction
        if args['v']:
            print(f"Run backwards induction with entries {entries}")
        pi, values = backwards_induction(graph, probabilities, rewards, entries, **args)
    # run MDP solver
    else:
        if args['v']:
            print("Run MDP solver")
        pi, values = markov_process_solver(graph, probabilities, rewards, **args)
    
    # parse output
    for k, v in sorted(pi.items(), key=lambda x: x[0]):
        print(f"{k} -> {v}")
    print(' '.join([f"{k}={v:.3f}" for k, v in sorted(values.items(), key=lambda x: x[0])]))


if __name__ == "__main__":
    main()
