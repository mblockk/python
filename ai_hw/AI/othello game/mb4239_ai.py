#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
COMS W4701 Artificial Intelligence - Programming Homework 2

An AI player for Othello. This is the template file that you need to  
complete and submit. 

@author: YOUR NAME AND UNI 
"""

import random
import sys
import time

visited = dict()

# You can use the functions in othello_shared to write your AI 
from othello_shared import find_lines, get_possible_moves, get_score, play_move


##FROM HERE 


def compute_utility(board, color):
    """
    Return the utility of the given board state
    (represented as a tuple of tuples) from the perspective
    of the player "color" (1 for dark, 2 for light)
    """
    p1, p2 = get_score(board)
    if color == 2:
        return p2-p1
    else:
        return p1-p2


############ MINIMAX ###############################

def minimax_min_node(board, color):
     
    if board in visited:
        return visited[board]
    
    elif len(get_possible_moves(board, color)) == 0:
        visited[board] = compute_utility(board, color)
        return compute_utility(board, color)
    else:
        visited[board] = compute_utility(board, color)        
        return min(minimax_max_node(play_move(board, color, move[0], move[1]), 2) for move in get_possible_moves(board,color))

    

def minimax_max_node(board, color):
    if board in visited:
        return visited[board]
    
    elif len(get_possible_moves(board, color)) == 0:
        visited[board] = compute_utility(board, color)
        return compute_utility(board, color)
    else:
        visited[board] = compute_utility(board, color)
        return max(minimax_min_node(play_move(board, color, move[0], move[1]), 1) for move in get_possible_moves(board, color))

    
def select_move_minimax(board, color):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board. 
    """
    v = float("-inf")
    
    for moves in get_possible_moves(board, color):
        i, j = moves[0], moves[1]
        
        maybe = minimax_max_node(play_move(board, color, i, j), color)
        if maybe > v:
            best_move = i, j
            v = maybe

    return best_move


############ ALPHA-BETA PRUNING #####################

#alphabeta_min_node(board, color, alpha, beta, level, limit)
def alphabeta_min_node(board, color, alpha, beta, level, limit):
    v = float("inf")

    node_ordering = sorted(get_possible_moves(board,color), key=lambda i: compute_utility(play_move(board, color, i[0], i[1]), 2))  
    if board in visited:
        return visited[board]
    
    elif level == limit:
        visited[board] = compute_utility(board, color)
        return compute_utility(board, 1)
    
    elif len(get_possible_moves(board, color)) == 0:
        visited[board] = compute_utility(board, color)
        return compute_utility(board, 1)
    
    
    
    else:
        for moves in node_ordering:
        ##for moves in get_possible_moves(board,color):        
            visited[board] = compute_utility(board, color)
            v = min(v, alphabeta_max_node(play_move(board, color, moves[0], moves[1]), 2, alpha, beta, level+1, limit))
            if v <= alpha:
                return v
            beta = min(beta, v)
        
    return v


#alphabeta_max_node(board, color, alpha, beta, level, limit)
def alphabeta_max_node(board, color, alpha, beta, level, limit):
    v = float("-inf")
    
    
    node_ordering = sorted(get_possible_moves(board,color), key=lambda i: compute_utility(play_move(board, color, i[0], i[1]), 1), reverse = True)
    if board in visited:
        return visited[board]
    elif level == limit:
        visited[board] = compute_utility(board, color)
        return compute_utility(board, 2)
    elif len(get_possible_moves(board, color)) == 0:
        visited[board] = compute_utility(board,color)
        return compute_utility(board, 2)
    
    else:
        for moves in node_ordering:
        ##for moves in get_possible_moves(board,color):
            visited[board] = compute_utility(board, color)
            v = max(v, alphabeta_min_node(play_move(board, color, moves[0], moves[1]), 1, alpha, beta, level+1, limit))
            if v >= beta:
                return v
            alpha = max(alpha, v)
    return v


def select_move_alphabeta(board, color): 
    v = float("-inf")
    alpha = float("-inf")
    beta = float("+inf")
    level = 0
    limit = 4
    
    for moves in get_possible_moves(board, color):
        i, j = moves[0], moves[1]
        
        maybe = alphabeta_max_node(play_move(board, color, i, j), color, alpha, beta, level, limit)
        if maybe > v:
            best_move = i, j
            v = maybe

    return best_move


## TO HERE WRITTEN BY ME

####################################################
def run_ai():
    """
    This function establishes communication with the game manager. 
    It first introduces itself and receives its color. 
    Then it repeatedly receives the current score and current board state
    until the game is over. 
    """
    print("AB AI") # First line is the name of this AI  
    color = int(input()) # Then we read the color: 1 for dark (goes first), 
                         # 2 for light. 

    while True: # This is the main loop 
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input() 
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over. 
            print 
        else: 
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The 
                                  # squares in each row are represented by 
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)
                    
            # Select the move and send it to the manager 
            movei, movej = select_move_alphabeta(board, color)
            #movei, movej = select_move_minimax(board, color)
            
            print("{} {}".format(movei, movej)) 


if __name__ == "__main__":
    run_ai()
