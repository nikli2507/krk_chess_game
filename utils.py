import chess
import requests

def simulate_move(board, move):
    """ Returns the board after the move has been made. """
    board_prime = board.copy()
    board_prime.push(move)
    return board_prime

def find_white_rook_square(board):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece and piece.piece_type == chess.ROOK and piece.color == chess.WHITE:
            return square
    return None

def find_white_king_square(board):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece and piece.piece_type == chess.KING and piece.color == chess.WHITE:
            return square
    return None

def new_board(wk, wr, bk):
    """
    Set up a new chess board with specified positions for the kings and the white rook.
    
    :param wk: Position of the white king.
    :param wr: Position of the white rook.
    :param bk: Position of the black king.
    :return: A chess.Board object.
    """
    board = chess.Board()
    board.clear_board()  # clear all pieces
    board.push(chess.Move.null())  # make it blacks move
    board.set_piece_at(chess.parse_square(wk), chess.Piece(chess.KING, chess.WHITE))
    board.set_piece_at(chess.parse_square(wr), chess.Piece(chess.ROOK, chess.WHITE))
    board.set_piece_at(chess.parse_square(bk), chess.Piece(chess.KING, chess.BLACK))
    return board