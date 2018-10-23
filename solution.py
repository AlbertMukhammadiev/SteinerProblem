import networkx as nx
import matplotlib.pyplot as plt
from sympy.geometry import Point
from genpath import generate_paths
from steiner import build_Steiner_tree, base_color
from random import randint


def create_quadrilateral():
    G = nx.Graph()
    G.add_node(0,pos=Point(randint(0,100), randint(0,100)),color='green')
    G.add_node(1,pos=Point(randint(0,100), randint(0,100)),color='green')
    G.add_node(2,pos=Point(randint(0,100), randint(0,100)),color='green')
    G.add_node(3,pos=Point(randint(0,100), randint(0,100)),color='green')
    return G


if __name__ == '__main__':
    G = create_quadrilateral()
    fig = plt.figure()
    steiner_tree, _ = build_Steiner_tree(G)
    node_color = nx.get_node_attributes(steiner_tree,'color')
    node_color = list(node_color.values())
    node_pos = nx.get_node_attributes(steiner_tree,'pos')
    nx.draw(steiner_tree, pos=node_pos, node_color=node_color, with_labels = True)
    plt.show()