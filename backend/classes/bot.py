#! /bin/python3

from game import *
from squares import *
from random import randint, choice

def evaluate_opening(self, fen):
    pass

def evaluate_random(self, board, moves):
    o_pos = list(moves.keys())
    chosen_pos = o_pos[randint(0, len(o_pos)-1)]
    while not moves[chosen_pos]:
        chosen_pos = o_pos[randint(0, len(o_pos)-1)]
    chosen_move = moves[chosen_pos][randint(0, len(moves[chosen_pos])-1)]
    return Square.index_to_tile(chosen_pos) + Square.index_to_tile(chosen_move)

def evaluate_game(board, depth, alpha, beta, max_player, max_colour):
    """Minimax algorithm with alpha-beta pruning"""
    if depth == 0 or game.game_over():
        return None, node.eval

    moves = board.get_moves()
    best_move = random.choice(moves)

    if max_player: 
        max_eval = -float('inf')
        for move in moves:
            temp_board = board.copy()
            temp_board.move(move)
            current_eval = evaluate_game(board, depth-1, alpha, beta, False, max_colour)[1]
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
            temp_board = board.copy()
            temp_board.move(move)
            current_eval = evaluate_game(board, depth-1, alpha, beta, True, max_colour)[1]
            if current_eval < min_eval:
                min_eval = current_eval
                best_move = move
            alpha = min(beta, current_eval)
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
    b = Bot(0)
    colour = 1

    for loop in range(30):
        white, black, w_boards, b_boards = a.get_legal_moves()
        new = b.evaluate_middlegame(a, white if colour else black)
        a.move(new)
        print(a)
        colour = 0 if colour else 1
