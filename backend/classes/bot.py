#! /bin/python3

from squares import *
from random import randint, choice
from time import sleep

def evaluate_opening(fen):
    pass

def evaluate_random(moves):
    sleep(0.5)
    try:
        chosen_move = moves[randint(0, len(moves)-1)]
    except ValueError:
        return None
    return chosen_move

def evaluate_game(board, depth, alpha, beta, max_player, max_colour):
    """Minimax algorithm with alpha-beta pruning"""
    moves = board.get_legal_moves(not max_player)
    if depth == 0 or not len(moves):
        return None, board.evaluate_board(not max_player)

    best_move = choice(moves)

    if max_player:
        max_eval = -float('inf')
        for move in moves:
            temp_board = board.board_copy()
            temp_board.move(move)
            current_eval = evaluate_game(temp_board, depth-1, alpha, beta, False, max_colour)[1]
            if current_eval > max_eval:
                max_eval = current_eval
                best_move = move
            alpha = max(alpha, current_eval)
            if beta <= alpha:
                break
        return best_move, max_eval
    else:
        min_eval = float('inf')
        for move in moves:
            temp_board = board.board_copy()
            temp_board.move(move)
            current_eval = evaluate_game(temp_board, depth-1, alpha, beta, True, max_colour)[1]
            if current_eval < min_eval:
                min_eval = current_eval
                best_move = move
            beta = min(beta, current_eval)
            if beta <= alpha:
                break
        return best_move, min_eval
        

if __name__ == "__main__":
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
