#! /bin/python3

from squares import *
from random import randint, choice
from time import sleep

def evaluate_random(moves):
    """Gets a random move (for testing purposes)."""
    sleep(0.5)
    try:
        chosen_move = moves[randint(0, len(moves)-1)]
    except ValueError:
        return None
    return chosen_move

def evaluate_game(board, depth, alpha, beta, max_player):
    """
    Minimax algorithm with alpha-beta pruning (Depth First Search algorithm).
    board: Board object
    depth (int): Depth of the node we are on.
    alpha, beta (float/int): Parameters used for pruning.
    max_player (int/bool): Integer or Boolean that shows if the evaluation should be maxed or minimized.
    """
    moves = board.get_legal_moves(not max_player)       #Gets legal moves of the opposite player (because WHITE = 1 and BLACK = 0)
    game_over = board.game_over()
    if depth == 0 or not len(moves):        #For leaf nodes of the graph (at the end of the recursion or end of game)
        return "", board.evaluate_board(not max_player)
    elif game_over == 1:        #Checkmate
        return "", 30000
    elif game_over == 2 or game_over == 3:      #Tie
        return "", 0

    best_move = choice(moves)

    if max_player:
        max_eval = -float('inf')
        for move in moves:
            temp_board = board.board_copy()     #Makes a copy of the board object
            temp_board.move(move)       #Makes a move
            current_eval = evaluate_game(temp_board, depth-1, alpha, beta, False)[1]        #Recursively calls the Minimax algorithm function
            if current_eval > max_eval:         #Saves the best move and best evaluation
                max_eval = current_eval
                best_move = move
            alpha = max(alpha, max_eval)
            if beta <= alpha:       #Prunes branch if needed
                break
        return best_move, max_eval
    else:
        min_eval = float('inf')
        for move in moves:
            temp_board = board.board_copy()
            temp_board.move(move)
            current_eval = evaluate_game(temp_board, depth-1, alpha, beta, True)[1]
            if current_eval < min_eval:
                min_eval = current_eval
                best_move = move
            beta = min(beta, min_eval)
            if beta <= alpha:
                break
        return best_move, min_eval
        

if __name__ == "__main__":
    """Initial tests for the Bot file. These tests may no longer be valid anymore since the class was modified a lot since then."""
    from board import *
    from fen import *

    ex = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    a = Board(fen_str=ex)
    #a.move("d2d4")
    #a.move("e7e6")

    for loop in range(30):
        white, black = a.get_legal_moves()
        new = evaluate_game(a, white if colour else black)
        a.move(new)
        print(a)
        colour = 0 if colour else 1
