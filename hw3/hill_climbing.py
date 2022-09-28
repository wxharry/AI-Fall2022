from math import inf

def error(state, table):
    M = 13
    T = 23
    total_weight = 0
    total_value = 0
    for obj in state:
        total_weight += table[obj]['w']
        total_value += table[obj]['v']
    return max(total_weight - M, 0) + max(T - total_value, 0), total_value, total_weight

def neighbor_of(state, table):
    for obj in table:
        if obj not in state:
            tmp = state.copy()
            tmp.add(obj)
            yield tmp
    for obj in state:
        tmp = state.copy()
        tmp.remove(obj)
        yield tmp
    for obj1 in state:
        for obj2 in table:
            if obj2 not in state:
                tmp = state.copy()
                tmp.remove(obj1)
                tmp.add(obj2)
                yield tmp
    

def hill_climbing(state, table):
    while True:
        i = 0
        next_error, next_value, next_weight = error(state, table)
        nextState = set()
        print("Visit neighbors: ")
        for neighbor in neighbor_of(state, table):
            neighbor_error, neighbor_value, neighbor_weight = error(neighbor, table)
            print(f"S{i} = { '{' + ','.join(neighbor) + '}' }\tError(S) = max({neighbor_weight}-13,0) + max(23-{neighbor_value},0) = {neighbor_error}")
            if neighbor_error < next_error \
              or (neighbor_error == next_error and neighbor_value > next_value) \
              or (neighbor_error == next_error and neighbor_value == next_value and neighbor_weight < next_weight):
                next_error, next_value, next_weight = neighbor_error, neighbor_value, neighbor_weight
                nextState = neighbor
                nextIdx = i
            i += 1
        print(f"choose S{nextIdx} = {'{' + ','.join(nextState) + '}'}\n")
        if next_error == 0:
            return nextState
        state = nextState
def main():
    table = {
        'A': {'v': 13, 'w': 11},
        'B': {'v': 8, 'w': 4},
        'C': {'v': 11, 'w': 7},
        'D': {'v': 7, 'w': 4},
        'E': {'v': 5, 'w': 2},
    }
    print("######Starting with {'A', 'D'}")
    print(hill_climbing({'A', 'D'}, table))
    print("######Starting with {'A', 'B'}")
    print(hill_climbing({'A', 'B'}, table))

if __name__ == '__main__':
    main()