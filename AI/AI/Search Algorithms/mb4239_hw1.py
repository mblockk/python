"""
COMS W4701 Artificial Intelligence - Programming Homework 1

In this assignment you will implement and compare different search strategies
for solving the n-Puzzle, which is a generalization of the 8 and 15 puzzle to
squares of arbitrary size (we will only test it with 8-puzzles for now). 
See Courseworks for detailed instructions.

@author: Michael Block (mb4239)
"""

import time
import math

def state_to_string(state):
    row_strings = [" ".join([str(cell) for cell in row]) for row in state]
    return "\n".join(row_strings)


def swap_cells(state, i1, j1, i2, j2):
    """
    Returns a new state with the cells (i1,j1) and (i2,j2) swapped. 
    """
    value1 = state[i1][j1]
    value2 = state[i2][j2]
    
    new_state = []
    for row in range(len(state)): 
        new_row = []
        for column in range(len(state[row])): 
            if row == i1 and column == j1: 
                new_row.append(value2)
            elif row == i2 and column == j2:
                new_row.append(value1)
            else: 
                new_row.append(state[row][column])
        new_state.append(tuple(new_row))
    return tuple(new_state)


def get_successors(state):
    """
    This function returns a list of possible successor states resulting
    from applicable actions. 
    The result should be a list containing (Action, state) tuples. 
    For example [("Up", ((1, 4, 2),(0, 5, 8),(3, 6, 7))), 
                 ("Left",((4, 0, 2),(1, 5, 8),(3, 6, 7)))] 
    """ 
  
    child_states = []

    # YOUR CODE HERE . Hint: Find the "hole" first, then generate each possible
    # successor state by calling the swap_cells method.
    # Exclude actions that are not applicable. 
    l = len(state)
    for i in range(0,l):
        for j in range(0,l):            
            if state[i][j] == 0:
                if i == 0:
                    if j == 0:
                        child_states.append(("LEFT", swap_cells(state, 0, 0, 0, 1)))
                        child_states.append(("UP", swap_cells(state, 0, 0, 1, 0)))
                    elif j == l-1:
                        child_states.append(("RIGHT", swap_cells(state, 0, l-1, 0, l-2)))
                        child_states.append(("UP", swap_cells(state, 0, l-1, 1, l-1)))
                    else:
                        child_states.append(("LEFT", swap_cells(state, 0, j, 0, j+1)))
                        child_states.append(("RIGHT", swap_cells(state, 0, j, 0, j-1)))
                        child_states.append(("UP", swap_cells(state, 0, j, 1, j)))
                elif i == l-1:
                    if j == 0:
                        child_states.append(("LEFT", swap_cells(state, l-1, 0, l-1, 1)))
                        child_states.append(("DOWN", swap_cells(state, l-1, 0, l-2, 0)))
                    elif j == l-1:
                        child_states.append(("RIGHT", swap_cells(state, l-1, l-1, l-1, l-2)))
                        child_states.append(("DOWN", swap_cells(state, l-1, l-1, l-2, l-1)))
                    else:
                        child_states.append(("LEFT", swap_cells(state, l-1, j, l-1, j+1)))
                        child_states.append(("RIGHT", swap_cells(state, l-1, j, l-1, j-1)))
                        child_states.append(("DOWN", swap_cells(state, l-1, j, l-2, j)))
                elif j == 0:
                    child_states.append(("LEFT", swap_cells(state, i, 0, i, 1)))
                    child_states.append(("UP", swap_cells(state, i, 0, i+1, 0)))
                    child_states.append(("DOWN", swap_cells(state, i, 0, i-1, 0)))
                elif j == l-1:
                    child_states.append(("RIGHT", swap_cells(state, i, l-1, i, l-2)))
                    child_states.append(("UP", swap_cells(state, i, l-1, i+1, l-1)))
                    child_states.append(("DOWN", swap_cells(state, i, l-1, i-1, l-1)))
                else:
                    child_states.append(("LEFT", swap_cells(state, i, j, i, j+1)))
                    child_states.append(("RIGHT", swap_cells(state, i, j, i, j-1)))
                    child_states.append(("UP", swap_cells(state, i, j, i+1, j)))
                    child_states.append(("DOWN", swap_cells(state, i, j, i-1, j)))   
                    
                    
                
    return child_states
    
            
def goal_test(state):
    """
    Returns True if the state is a goal state, False otherwise. 
    """    
    rows = len(state)
    i = 0
    for x in range(0,rows):
        for y in range(0, rows):
            if state[x][y] != i:
                return False
            i += 1
    return True
    
   
def bfs(state):
    """
    Breadth first search.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the fringe.
    You may want to keep track of three mutable data structures:
    - The fringe of nodes to expand (operating as a queue in BFS)
    - A set of closed nodes already expanded
    - A mapping (dictionary) from a given node to its parent and associated action
    """
    states_expanded = 0
    max_fringe = 0
    fringe = []
    closed = set()
    parents = {}
    #YOUR CODE HERE
    fringe = [state]
    sol = []
    
    while len(fringe) > 0:
        current = fringe.pop(0)
        states_expanded += 1
        closed.add(current)
        child_states = get_successors(current)     
        if goal_test(current) == False:            
            for i in range(0,len(child_states)):
                child = child_states[i][1]
                if not child in closed:
                    closed.add(child)
                    fringe.append(child)
                    value = (current, child_states[i][0])
                    parents[child] = value
                    max_fringe = max(len(fringe), max_fringe)
                        
        else:            
            while current in parents:
                sol.append(parents.get(current)[1])
                current = parents[current][0]
            sol.reverse()
            return sol, states_expanded, max_fringe

    return None, states_expanded, max_fringe # No solution found
                               
     
def dfs(state):
    """
    Depth first search.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the fringe.
    You may want to keep track of three mutable data structures:
    - The fringe of nodes to expand (operating as a stack in DFS)
    - A set of closed nodes already expanded
    - A mapping (dictionary) from a given node to its parent and associated action
    """
    states_expanded = 0
    max_fringe = 0
    fringe = []
    closed = set()
    parents = {}
    fringe = [state]
    sol = []
    
    while len(fringe) > 0:
        current = fringe.pop()
        states_expanded += 1
        closed.add(current)
        child_states = get_successors(current)
              
        if goal_test(current) == False:
            for i in range(0,len(child_states)):
                child = child_states[i][1]
                if child not in closed:
                    closed.add(child)
                    fringe.append(child)
                    value = (current, child_states[i][0])
                    parents[child_states[i][1]] = value
                    max_fringe = max(len(fringe), max_fringe)

                    
        else:
            
            while current in parents:               
                sol.append(parents.get(current)[1])
                current = parents[current][0]
            sol.reverse()
            return sol, states_expanded, max_fringe
        
    return None, states_expanded, max_fringe # No solution found


def misplaced_heuristic(state):
    """
    Returns the number of misplaced tiles.
    """
    j = 0
    misplaced = 0
    for i in state:
        for x in i:
            if x != j:
                misplaced += 1
            j += 1
                  
    return misplaced # replace this


def manhattan_heuristic(state):
    """
    For each misplaced tile, compute the Manhattan distance between the current
    position and the goal position. Then return the sum of all distances.
    """
    man = 0
    v = len(state)
    for x in range(v):
        for y in range(v):
            m, n = divmod(state[x][y], v)
            man += abs(m-x)+abs(n-y)
        
    return man # replace this


def best_first(state, heuristic):
    """
    Best first search.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the fringe.
    You may want to keep track of three mutable data structures:
    - The fringe of nodes to expand (operating as a priority queue in greedy search)
    - A set of closed nodes already expanded
    - A mapping (dictionary) from a given node to its parent and associated action
    """
    # You may want to use these functions to maintain a priority queue
    from heapq import heappush
    from heapq import heappop

    states_expanded = 0
    max_fringe = 0
    fringe = []
    closed = set()
    parents = {}
    cost = heuristic(state)
    heappush(fringe, (cost, state))
    sol = []
    
    while len(fringe) > 0:
        current = heappop(fringe)[1]
        states_expanded += 1
        closed.add(current)
        child_states = get_successors(current)
              
        if goal_test(current) == False:
            for i in range(0,len(child_states)):
                child = child_states[i][1]                
                if child not in closed:
                    if heuristic(child) not in fringe:
                        cost = heuristic(child)
                        heappush(fringe, (cost, child))
                        max_fringe = max(len(fringe), max_fringe)
                        
                        value = (current, child)
                        parents[child] = value
                        max_fringe = max(len(fringe), max_fringe)
                        
        else:
            
            while current in parents:
                sol.append(parents.get(current)[1])
                current = parents[current][0]
            sol.reverse()
            return sol, states_expanded, max_fringe

    return None, states_expanded, max_fringe # No solution found


def astar(state, heuristic):
    """
    A-star search.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the fringe.
    You may want to keep track of three mutable data structures:
    - The fringe of nodes to expand (operating as a priority queue in greedy search)
    - A set of closed nodes already expanded
    - A mapping (dictionary) from a given node to its parent and associated action
    """
    # You may want to use these functions to maintain a priority queue
    from heapq import heappush
    from heapq import heappop

    states_expanded = 0
    max_fringe = 0

    fringe = []
    closed = set()
    parents = {}
    costs = {}
    costs[state] = 0
    cost = heuristic(state)
    heappush(fringe, (cost, state))
    sol = []
    
    while len(fringe) > 0:
        current = heappop(fringe)[1]
        states_expanded += 1
        closed.add(current)
        child_states = get_successors(current)
              
        if goal_test(current) == False:
            for i in range(0,len(child_states)):
                child = child_states[i][1]
                costs[child] = costs[current]+1
                if child not in closed:
                    if heuristic(child_states[i][1]) not in fringe:
                        cost = heuristic(child_states[i][1])
                        heappush(fringe, (cost+costs[child_states[i][1]], child))
                        max_fringe = max(len(fringe), max_fringe)
                        value = (current, child_states[i][0])
                        parents[child_states[i][1]] = value
                        max_fringe = max(len(fringe), max_fringe)
                        
        else:
            
            while current in parents:
                sol.append(parents.get(current)[1])
                current = parents[current][0]
            sol.reverse()
            return sol, states_expanded, max_fringe

    
    return None, states_expanded, max_fringe # No solution found


def print_result(solution, states_expanded, max_fringe):
    """
    Helper function to format test output. 
    """
    if solution is None: 
        print("No solution found.")
    else: 
        print("Solution has {} actions.".format(len(solution)))
    print("Total states expanded: {}.".format(states_expanded))
    print("Max fringe size: {}.".format(max_fringe))



if __name__ == "__main__":

    #test_state = ((0, 1, 2),
     #             (3, 4, 5),
      #            (6, 7, 8))
    #easy test case
    #test_state = ((1, 4, 2),
     #             (0, 5, 8), 
      #            (3, 6, 7))
    

    #More difficult test case
    test_state = ((7, 2, 4),
                  (5, 0, 6), 
                  (8, 3, 1))  
#
    print(state_to_string(test_state))

    print("====BFS====")
    start = time.time()
    solution, states_expanded, max_fringe = bfs(test_state) #
    end = time.time() 
    print_result(solution, states_expanded, max_fringe)
    if solution is not None:
        print(solution)
    print("Total time: {0:.3f}s".format(end-start))

    print() 
    print("====DFS====") 
    start = time.time()
    solution, states_expanded, max_fringe = dfs(test_state)
    end = time.time()
    print_result(solution, states_expanded, max_fringe)
    print("Total time: {0:.3f}s".format(end-start))

    print() 
    print("====Greedy Best-First (Misplaced Tiles Heuristic)====") 
    start = time.time()
    solution, states_expanded, max_fringe = best_first(test_state, misplaced_heuristic)
    end = time.time()
    print_result(solution, states_expanded, max_fringe)
    print("Total time: {0:.3f}s".format(end-start))


    print() 
    print("====A* (Misplaced Tiles Heuristic)====") 
    start = time.time()
    solution, states_expanded, max_fringe = astar(test_state, misplaced_heuristic)
    end = time.time()
    print_result(solution, states_expanded, max_fringe)
    print("Total time: {0:.3f}s".format(end-start))

    print() 
    print("====A* (Total Manhattan Distance Heuristic)====") 
    start = time.time()
    solution, states_expanded, max_fringe = astar(test_state, manhattan_heuristic)
    end = time.time()
    print_result(solution, states_expanded, max_fringe)
    print("Total time: {0:.3f}s".format(end-start))

