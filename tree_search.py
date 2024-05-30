from heuristics import better, worse, find_white_rook_square, find_white_king_square, simulate_move
from BoardNode import *
from tqdm import tqdm

"""
The idea of the below methods is described in 'Huberman, Barbara Jane. A program to play chess end games. No. 65. Stanford University, 1968.'
Especially chapter 2 (program organization) is used. The methods implement the described concept from page 10-23.
"""

def get_good_move(board, tree_root=None):
    """ 
    Returns a good move and the tree root of the tree search for the current board position, where it is white's turn to move. 
    The method builds up a tree of board positions that force a better position for white. Therefore the returned tree root needs
    to be saved outside and called again with the next board position after black moved.
    """
    boardNode = BoardNode(board)
    
    if tree_root == None:
        get_move_tree(boardNode, [BoardNode(simulate_move(board, move), boardNode) for move in board.legal_moves])
        tree_root = boardNode 
    else:
        for child in tree_root.children:
            if child.board.fen().split(' ')[0] == board.fen().split(' ')[0]:
                tree_root = child
                break

    # Search through the immediate children of the root to find the best path
    best_node = None
    for child in tree_root.children:
        if has_better_leaves(child):
            best_node = child
            break

    for move in board.legal_moves:
        if simulate_move(board, move).fen().split(' ')[0] == best_node.board.fen().split(' ')[0]:
            return move, best_node # new tree root


def get_move_tree(reference_node, Q):
    """
    Recursive function that returns a tree of board positions, in which white can search to force a better position.
    param reference_node: The current board wrapped in a BoardNode object. The function will search for a better 
                          position for white from this board.
    param Q: All possible positions that can be reached from the reference_node with one move.
    """
    print("Entering get_move_tree")
    progress_bar = tqdm(total=len(Q), desc="Processing moves", unit="move")
    Q = redundant_branch_cut_off(Q)
    new_Q = []
    for q in Q:
        progress_bar.update(1)
        if worse(reference_node.board, q.board):
            continue
        elif better(reference_node.board, q.board):
            q.heuristic = Heuristic.BETTER
            progress_bar.close() 
            return True
        else:
            q_leads_to_better_pos = True
            q_could_lead_to_better_pos = True
            possible_new_qs = []
            for black_move in q.board.legal_moves:
                p = BoardNode(simulate_move(q.board, black_move), q)
                white_could_force_better_pos = False
                white_can_force_better_pos = False
                for white_move in p.board.legal_moves:

                    new_q = BoardNode(simulate_move(p.board, white_move), p)

                    if not worse(reference_node.board, new_q.board):
                        white_could_force_better_pos = True
                        if not better(reference_node.board, new_q.board):
                            possible_new_qs.append(new_q)
                        else:
                            new_q.heuristic = Heuristic.BETTER
                            white_can_force_better_pos = True
                            break
                    else:
                        # delete node
                        new_q.parent.children = [child for child in new_q.parent.children if child.board.fen() != new_q.board.fen()]

                if not white_can_force_better_pos:
                    q_leads_to_better_pos = False

                if not white_could_force_better_pos:
                    q_could_lead_to_better_pos = False
                    q.parent.children = [child for child in q.parent.children if child.board.fen() != q.board.fen()]
                    break

            if q_leads_to_better_pos:
                if any([has_better_leaves(q) for q in reference_node.children]):
                    progress_bar.close()  
                    return True
            elif q_could_lead_to_better_pos:
                new_Q.extend(possible_new_qs)

    progress_bar.close()
    return get_move_tree(reference_node, new_Q)

def has_better_leaves(q):
    """ Used to find the next good move path in the tree. A path is good when white can force a better position. """
    if q.heuristic == Heuristic.BETTER:   # we arrived at the end of the tree
        return True     
    if q.children == []:
        return False
    better_q_for_each_p = True        
    for p in q.children:
        better_q = False
        for q_new in p.children:
            if len(q_new.children) > 0:
                better_q = has_better_leaves(q_new)
                if better_q:
                    break
            elif q_new.heuristic == Heuristic.BETTER:
                better_q = True
                break
        if not better_q:
            better_q_for_each_p = False
            break
    return better_q_for_each_p

def redundant_branch_cut_off(Q):
    """ Implements the redundant branch cut-off described in the dissertation at page 21. """
    new_Q = []
    for q in Q:
        delete_q = False
        previous_qs = find_previous_qs(q, [])
        for previous_q in previous_qs:
            if same_white_piece_positions(q.board, previous_q.board):
                delete_q = True
                break
        if not delete_q:
            new_Q.append(q)
    return new_Q

def find_previous_qs(q, previous_qs):
    if q.parent.parent == None:
        return previous_qs
    previous_qs.append(q.parent.parent)
    return find_previous_qs(q.parent.parent, previous_qs)

def same_white_piece_positions(board1, board2):
    """ Check if the white rook and king are on the same squares in both boards. """
    if find_white_rook_square(board1) == find_white_rook_square(board2) and find_white_king_square(board1) == find_white_king_square(board2):
        return True
    return False

