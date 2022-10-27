"""
author: Xiaohan Wu
NYU ID: xw2788
email: xiaohanwu12@gmail.com
"""
import argparse

COLORS = ["Red", "Green", "Blue", "Yellow"]
VERBOSE = False

def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-v', default=False, action='store_true',
                        help='Indicates verbose mode')

    parser.add_argument('ncolor', choices=['2', '3', '4'],
                        help='Indicates the number of colors to solve for. If 2 use R, G; if 3 RGB; 4 RGBY')

    parser.add_argument('input-file', 
                        help='Specify a input file to read')

    args = parser.parse_args()
    return dict(args._get_kwargs())

def read_input(filename):
    """
    the output graph has n keys (n is the number of vertexes)
    and for each key, its value is a list containing all its adjacent vertexes.
    """
    graph = dict()
    with open(filename, "r", encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip().replace(' ', '')
            if ':' in line:
                parent, children = line.strip().split(':')
                children = children.strip("[]").split(",")
                for child in children:
                    if child == '':
                        graph[parent] = []
                        continue
                    graph[parent] = graph.get(parent, []) + [child]
                    graph[child] = graph.get(child, []) + [parent]
    return graph

class Atom:
    def __init__(self, vertex, color) -> None:
        self.vertex = vertex
        self.color = color
    def __str__(self) -> str:
        return f"{self.vertex}_{self.color}"
    def __repr__(self) -> str:
        return f'Atom({self.vertex}, {self.color})'
    def __hash__(self):
        return hash(str(self))
    def __eq__(self, __o: object) -> bool:
        return self.vertex == __o.vertex and self.color == __o.color

class Literal:
    def __init__(self, sign, atom) -> None:
        self.sign = sign
        self.atom = atom
    def __str__(self) -> str:
        return f'{"" if self.sign else "!"}{str(self.atom)}'
    def __repr__(self) -> str:
        return f'Literal({self.sign}, {repr(self.atom)})'
    def __hash__(self):
        return hash(str(self))
    def __eq__(self, __o: object) -> bool:
        return self.sign == __o.sign and self.atom == __o.atom

def graph_constraints(graph, n):
    """
    generates two parts:  
    1. a set of atoms like COLOR(assignments, R)  
    2. a set of clauses in CNF  
    """
    atoms = set()
    clauses = [] # clause is a set of literals
    for vertex, neighbors in graph.items():
        # for each vertex, it could be colored as n colors
        clauses.append([Literal(True, Atom(vertex, color)) for color in COLORS[:n]])
        for color in COLORS[:n]:
            atoms.add(Atom(vertex, color))
            for neighbor in neighbors:
                # for each vertex, either it is color, or its neighbor is color. (in CNF way)
                clauses.append([Literal(False, Atom(vertex, color)), Literal(False, Atom(neighbor, color))])
            # optional: if vertex is one color, then it cannot be any other colors
            for _color in COLORS[:n]:
                if color == _color:
                    continue
                clauses.append([Literal(False, Atom(vertex, color)), Literal(False, Atom(vertex, _color))])
    return atoms, clauses

def DPLL(atoms, clauses, assignments={}):
    """ DPLL
    is implemented based on Davis-Putnam (DPLL) procedure with a few modifications:
    1. use a dict in Python rather than a list to record assignments
    2. because of 1, no need to have a helper function
    """
    while True:
        if VERBOSE:
            output_clauses = []
            for clause in clauses:
                print_clause = ' | '.join([str(literal) for literal in clause])
                if print_clause not in output_clauses:
                    print(print_clause)
                    output_clauses.append(print_clause)
        # base of the recursion: success or failure
        if len(clauses) == 0:
            if VERBOSE:
                print("Clause is empty")
                print("Set unbounded atom to defalut(False)")
            for atom in atoms:
                if not assignments.get(atom):
                    assignments[atom] = False
            if VERBOSE:
                print(f"assignments = {assignments}")
                print("SUCCESS!")
            return assignments
        elif [] in clauses:
            if VERBOSE:
                print("found empty clause!")
            return None
        # easy cases
        # pure literal
        pure_literals = find_pure_literal(clauses)
        singletons = find_single_literal(clauses)
        if len(pure_literals):
            pure_literal = pure_literals.pop()
            assignments = obviousAssign(pure_literal, assignments)
            if VERBOSE:
                print(f"found pure literal {pure_literal}, set {pure_literal.atom} to {assignments[pure_literal.atom]}")
                print(f"assignments = {assignments}")
            for clause in list(clauses):
                if pure_literal in clause:
                    continue
                clauses.append(clause)
        # singleton
        elif len(singletons):
            singleton = singletons.pop()
            assignments = obviousAssign(singleton, assignments)
            if VERBOSE:
                print(f"found singleton {singleton}, set {singleton.atom} to {assignments[singleton.atom]}")
                print(f"assignments = {assignments}")
            clauses = propagate(singleton.atom, clauses, assignments)
        else:
            break
    # Hard case:
    # pick an unbounded atom
    guess = [atom for atom in atoms if assignments.get(atom) == None][0]
    assignments[guess] = True
    if VERBOSE:
        print(f"guess {guess} True")
        print(f"assignments = {assignments}")
    clauses_copy = clauses.copy()
    clauses_copy = propagate(guess, clauses_copy, assignments)
    assignments_copy = assignments.copy()
    assignments_new = DPLL(atoms, clauses_copy, assignments_copy)
    if assignments_new != None :
        return assignments_new
    assignments[guess] = False
    if VERBOSE:
        print(f"backtracking to {guess}")
        print(f"guess {guess} False")
        print(f"assignments = {assignments}")
    clauses_copy = propagate(guess, clauses_copy, assignments)
    return DPLL(atoms, clauses_copy, assignments)


def find_pure_literal(clauses):
    literals = {}
    for clause in clauses:
        for literal in clause:
            literals[str(literal.atom)] = literals.get(str(literal.atom)), set() | {str(literal.atom)}
    pure_literals = set()
    for literal_set in literals.values():
        if len(literal_set) == 1:
            pure_literals |= literal_set
    return pure_literals

def find_single_literal(clauses):
    singleton = set()
    for clause in clauses:
        if len(clause) == 1:
            singleton.add(clause[0])
    return singleton

def propagate(atom, clauses, assignments):
    new_clauses = []
    for clause in clauses:
        new_clause = []
        for literal in clause:
            # if literal = True, then delete clause
            if literal.atom == atom and literal.sign == assignments[atom]:
                new_clause = None
                break
            # if literal = False, then delete literal
            elif literal.atom == atom and assignments.get(atom) != None and literal.sign != assignments[atom]:
                continue
            new_clause.append(literal)
        # remove the clause with a True literal
        if new_clause == None:
            continue
        new_clauses.append(new_clause)
    return new_clauses

def obviousAssign(literal, assignments):
    if literal.sign:
        assignments[literal.atom] = True
    elif not literal.sign:
        assignments[literal.atom] = False
    return assignments

def convertBack(assignments):
    for k, v in assignments.items():
        if v:
            print(f"{k.vertex} = {k.color}")


def main():
    args = parse_arguments()
    global VERBOSE
    VERBOSE = args['v']
    graph = read_input(args['input-file'])
    atoms, clauses = graph_constraints(graph, eval(args['ncolor']))
    assignments = DPLL(atoms, clauses)
    if assignments == None:
        print(f"error: cannot fill in the map with {args['ncolor']} colors")
        return
    convertBack(assignments)

if __name__ == "__main__":
    main()
