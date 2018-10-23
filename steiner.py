"""This module allows to build Steiner tree for 4 points
and compute total length of edges.

Functions:
    build_Steiner_tree(G) -> (Graph, double)
    replace(G, pair) -> None
    inv_replace(G, temp) -> None
    rec_Steiner(G, path, nodes) -> None
    draw_graph(G) -> None
    eval_point(p) -> Point
"""

import networkx as nx
import matplotlib.pyplot as plt
from sympy.geometry import Point, Line2D, Segment2D, Circle, intersection, Line, Curve

from genpath import generate_paths

base_color = 'green'
temp_color = 'yellow'
steiner_color = 'aqua'


def build_Steiner_tree(G):
    """Return minimum Steiner tree and its length.

    Arguments:
    G -- a graph
    """
    paths = generate_paths(G.number_of_nodes())
    minimum = 1000
    steiner_tree = nx.empty_graph()
    for i, path in enumerate(paths):
        path.reverse()
        H = nx.Graph(G)
        try:
            rec_Steiner(H, path, list(range(H.number_of_nodes())))
            if len(list(nx.isolates(H))) == 0:
                road_length = 0
                for edge in H.edges:
                    position_u = H.nodes[edge[0]]['pos']
                    position_v = H.nodes[edge[1]]['pos']
                    road_length = road_length + position_u.distance(position_v)
                
                if road_length < minimum:
                    steiner_tree = H
                    minimum = road_length
        except:
            print(i)
            continue

    return steiner_tree, road_length



def replace(G, pair):
    """Replace two nodes with one without changing the path length.
    (according to Pompey's theorem)

    Arguments:
    G -- a graph
    pair -- a tuple of two nodes to be replaced
    """
    position_u = G.nodes[pair[0]]['pos']
    position_v = G.nodes[pair[1]]['pos']
    radius = position_u.distance(position_v)
    position_third = intersection(Circle(position_u, radius), Circle(position_v, radius))
    
    try:
        if pair[0] > pair[1]:
            position_third = position_third[1]
        else:
            position_third = position_third[0]
    except TypeError:
        if type(pair[0]) is int:
            position_third = position_third[1]
        else:
            position_third = position_third[0]

    G.add_node(pair, pos=eval_point(position_third), color=temp_color)


def inv_replace(G, temp):
    """Return the nodes replaced by temporary node
    and build a Steiner point.
    
    Arguments:
    G -- a graph
    temp -- temporary node
    """
    neighbor = next(G.neighbors(temp))
    u, v = temp
    u_v = Segment2D(G.nodes[u]['pos'], G.nodes[v]['pos'])
    temp_neighbor = Segment2D(G.nodes[temp]['pos'], G.nodes[neighbor]['pos'])
    if temp_neighbor.intersect(u_v):
        circle = Circle(G.nodes[temp]['pos'], G.nodes[u]['pos'], G.nodes[v]['pos'])
        points = circle.intersect(temp_neighbor)
        steiner_point = next((p for p in points if p != G.node[temp]['pos']))
        G.add_node(steiner_point, pos=steiner_point, color=steiner_color)
        G.add_path([u, steiner_point, v])
        G.add_edge(neighbor, steiner_point)
    else:
        if G.nodes[neighbor]['pos'].distance(G.nodes[u]['pos']) > G.nodes[neighbor]['pos'].distance(G.nodes[v]['pos']):
            G.add_path([u, v, neighbor])
        else:
            G.add_path([v, u, neighbor])

    G.remove_node(temp)


def rec_Steiner(G, path, nodes):
    """Recursively build a Steiner tree using a given path.

    Arguments:
    G -- graph
    path -- list of pairs of points that are replaced at each step
    nodes -- list of active nodes in the graph at the moment
    """
    if len(nodes) == 2:
        G.add_path(nodes)
        return
    
    pair = path.pop()
    nodes.remove(pair[0])
    nodes.remove(pair[1])
    nodes.append(pair)
    replace(G, pair)
    rec_Steiner(G, path, nodes)
    inv_replace(G, pair)


def eval_point(p):
    """Evaluate coordinates of point p."""
    return Point(tuple(p.evalf()))


def draw_graph(G):
    """Draw a given graph G taking into account nodes colors"""
    node_color = nx.get_node_attributes(G,'color')
    node_color = list(node_color.values())
    node_pos = nx.get_node_attributes(G,'pos')
    nx.draw(G, pos=node_pos, node_color=node_color, with_labels = True)
    plt.show()