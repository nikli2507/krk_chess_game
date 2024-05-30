import chess
from utils import *

"""
All below methods are described in 'Huberman, Barbara Jane. A program to play chess end games. No. 65. Stanford University, 1968.'
Especially chapter 3 (definition of better and worse) and 4 (rook and king against king) are used. The methods are direct
implementations of the pseudo code and descriptions in the dissertation.
"""

def stage(board):
    if board.is_checkmate():
        return 4
    if board.is_stalemate():
        return 0
    if board.turn == chess.BLACK:
        if any(board.is_capture(move) for move in board.legal_moves):
            return 0
    if goodquad(board) and squad(board) > 2:
        return 2
    if goodquad(board) and squad(board) == 2:
        return 3
    return 1
    
def m(board, stage):
    if stage in {0, 1, 3, 4}:
        return 0
    elif stage == 2:
        return squad(board)

def better(p, q):
    st_p = stage(p)
    st_q = stage(q)

    wr_p = find_white_rook_square(p)
    wk_p = p.king(chess.WHITE)
    d_wkr_p = chebyshev_distance(wr_p, wk_p)

    wr_q = find_white_rook_square(q)
    wk_q = q.king(chess.WHITE)
    d_wkr_q = chebyshev_distance(wr_q, wk_q)

    return st_q > st_p or (st_q == st_p and m(q, st_q) < m(p, st_q)) \
           or (st_p == 2 and st_q == 2 and d_wkr_q < d_wkr_p)

def worse(p, q):
    st_p = stage(p)
    st_q = stage(q)

    wr_p = find_white_rook_square(p)
    wk_p = p.king(chess.WHITE)
    d_wkr_p = chebyshev_distance(wr_p, wk_p)

    wr_q = find_white_rook_square(q)
    wk_q = q.king(chess.WHITE)
    d_wkr_q = chebyshev_distance(wr_q, wk_q)

    return st_q == 0 or (st_q == st_p and m(p, st_p) < m(q, st_q)) \
           or (st_p == 2 and  (st_q == 1 or (st_q == 2 and m(p, 2) == m(q, 2)))) \
           and d_wkr_p == 1 and (d_wkr_q > 1 or (st_q == 1 and wr_p != wr_q)) \
           or (st_p == 3 and (st_q == 2 or (st_q == 1 and d_wkr_q > 1) \
                              or (st_q == 3 and d_wkr_q > 1 \
                                  and d_wkr_q >= d_wkr_p)))

def chebyshev_distance(sq1, sq2):
    x1, y1 = divmod(sq1, 8)
    x2, y2 = divmod(sq2, 8)
    return max(abs(x1 - x2), abs(y1 - y2))

def quad(board):
    wr = find_white_rook_square(board)
    if wr == None: # rook has been taken
        return False
    bk = board.king(chess.BLACK)
    wk = board.king(chess.WHITE)

    rook_rank, rook_file = chess.square_rank(wr), chess.square_file(wr)
    bk_rank, bk_file = chess.square_rank(bk), chess.square_file(bk)
    wk_rank, wk_file = chess.square_rank(wk), chess.square_file(wk)
    
    if bk_rank < rook_rank and bk_file < rook_file: # bottom left
        if wk_rank > rook_rank or wk_file > rook_file: # white king not in the quadrant
            return True
    elif bk_rank < rook_rank and bk_file > rook_file: # bottom right
        if wk_rank > rook_rank or wk_file < rook_file:
            return True
    elif bk_rank > rook_rank and bk_file < rook_file: # top left
        if wk_rank < rook_rank or wk_file > rook_file:
            return True
    elif bk_rank > rook_rank and bk_file > rook_file: # top right
        if wk_rank < rook_rank or wk_file < rook_file:
            return True
    else: # not in a quadrant
        return False

    return False

def squad(board):
    wr = find_white_rook_square(board)
    bk = board.king(chess.BLACK)
    wk = board.king(chess.WHITE)

    rook_rank, rook_file = chess.square_rank(wr), chess.square_file(wr)
    bk_rank, bk_file = chess.square_rank(bk), chess.square_file(bk)
    wk_rank, wk_file = chess.square_rank(wk), chess.square_file(wk)
    
    if bk_rank < rook_rank and bk_file < rook_file: # bottom left
        if wk_rank > rook_rank or wk_file > rook_file: # white king not in the quadrant
            return rook_rank * rook_file
    elif bk_rank < rook_rank and bk_file > rook_file: # bottom right
        if wk_rank > rook_rank or wk_file < rook_file:
            return rook_rank * abs(rook_file-7)
    elif bk_rank > rook_rank and bk_file < rook_file: # top left
        if wk_rank < rook_rank or wk_file > rook_file:
            return abs(rook_rank-7) * rook_file
    elif bk_rank > rook_rank and bk_file > rook_file: # top right
        if wk_rank < rook_rank or wk_file < rook_file:
            return abs(rook_rank-7) * abs(rook_file-7)
    else: # not in a quadrant
        return -1

    return -1

def goodquad(board):
    if not quad(board):
        return False
    
    wr = find_white_rook_square(board)
    bk = board.king(chess.BLACK)
    wk = board.king(chess.WHITE)
    
    wk_rook_dist = chebyshev_distance(wk, wr)
    bk_rook_dist = chebyshev_distance(bk, wr)
    
    if board.turn == chess.WHITE:
        return wk_rook_dist <= bk_rook_dist+1
    else:
        return wk_rook_dist <= bk_rook_dist