from flask import Flask, jsonify, request, render_template
import chess 
from flask_cors import CORS
from tree_search import get_good_move
import os
from heuristics import new_board, get_board_info
from utils import simulate_move
from visualization import visualize_tree_interactive


app = Flask(__name__)
CORS(app)
app.root = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/custom_setup', methods=['POST'])
def custom_setup():
    """
    Set up a custom board configuration based on provided FEN or KRK piece positions and returns the
    corresponding FEN string. Resets the current search tree root.
    """
    app.root = None
    data = request.json
    board = None
    if 'fen' in data:
        board = chess.Board(data['fen'])
    else:
        board = new_board(data['wk'], data['wr'], data['bk'])
    fen = board.fen()
    return jsonify({"board_fen": fen, "board_info": get_board_info(board)})

@app.route('/setup', methods=['GET'])
def setup_board():
    """
    Set up the initial board configuration and return FEN string.
    """
    app.root = None
    board = new_board('a8', 'c8', 'g2')
    fen = board.fen()
    return jsonify({"board_fen": fen, "board_info": get_board_info(board)})

@app.route('/move', methods=['POST'])
def get_move():
    """
    Based on the current board position returns a good move to make for the white player.
    """
    data = request.json
    board_fen = data['board']
    board = chess.Board(board_fen)
    if app.root != None and len(app.root.children) == 0:
        app.root = None
    move, app.root = get_good_move(board, app.root)

    return jsonify({"move": move.uci(), "board_info": get_board_info(simulate_move(board, move)), "tree_html": visualize_tree_interactive(app.root)})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)

