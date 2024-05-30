from enum import Enum

class Heuristic(Enum):
    """Enum to represent heuristic evaluations."""
    UNDEFINED = 1
    BETTER = 2
    WORSE = 3

class BoardNode:
    """
    Represents a node in the game tree.
    """
    def __init__(self, board, parent=None):
        """
        Initialize a BoardNode.
        
        :param board: A chess.Board object representing the game state.
        :param parent: The parent BoardNode.
        """
        self.board = board
        if parent:
            parent.add_child(self)
            self.parent = parent
        else:
            self.parent = None
        self.children = []
        self.heuristic = Heuristic.UNDEFINED
        self.stage = None

    def add_child(self, child):
        self.children.append(child)

    def to_dict(self):
        """Convert the node to a dictionary representation. Used for debugging. """
        return {
            "fen": self.board.fen(),
            "heuristic": self.heuristic.name,
            "stage": self.stage
        }

