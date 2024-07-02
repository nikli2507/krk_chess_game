import chess
import chess.svg
from pyvis.network import Network
import base64
from BoardNode import *
from heuristics import *

""" The below methods can be used for debugging and visualizing the tree search. """

def board_to_image_svg(board):
    """Generate an SVG image for the given board."""
    svg = chess.svg.board(board)
    return svg

def svg_to_data_uri(svg_str):
    """Convert SVG string to data URI."""
    encoded = base64.b64encode(svg_str.encode('utf-8')).decode('utf-8')
    return f"data:image/svg+xml;base64,{encoded}"

def visualize_tree_interactive(root):
    net = Network(notebook=True, height='100%', width='100%')
    net.force_atlas_2based()

    def add_nodes_edges(node):
        node_id = str(id(node))
        if node_id not in net.get_nodes():
            svg = board_to_image_svg(node.board)
            img_uri = svg_to_data_uri(svg)
            st = stage(node.board)
            if stage == 2:
                net.add_node(node_id, label=f'Root Node, Stage {st} (Measure={m(node.board, st)})', image=img_uri, shape='image')
            else:
                net.add_node(node_id, label=f'Root Node, Stage {st}', image=img_uri, shape='image')
        
        for child in node.children:
            child_id = str(id(child))
            if child_id not in net.get_nodes():
                svg = board_to_image_svg(child.board)
                img_uri = svg_to_data_uri(svg)
                st = stage(child.board)
                if child.heuristic == Heuristic.UNDEFINED:
                    net.add_node(child_id, label=' ', image=img_uri, shape='image')
                elif stage == 2:
                    net.add_node(child_id, label=f'Stage {st} (Measure={m(child.board, st)}), {child.heuristic.name}', image=img_uri, shape='image')
                else:
                    net.add_node(child_id, label=f'Stage {st}, {child.heuristic.name}', image=img_uri, shape='image')
            net.add_edge(node_id, child_id, arrows='to')
            add_nodes_edges(child)  # Recursively process each child

    add_nodes_edges(root)

    return net.generate_html()