import networkx as nx
import matplotlib.pyplot as plt
from sympy.geometry import Point, Segment2D, Circle
from genpath import generate_paths
from steiner import steiner

from random import randint

removed_color = 'white'
temp_color = 'yellow'
base_color = 'green'
steiner_color = 'aqua'


def draw_graph(G, name):
    fig = plt.figure()
    node_color = nx.get_node_attributes(G,'color')
    node_color = list(node_color.values())
    node_pos = nx.get_node_attributes(G,'pos')
    nx.draw(G, pos=node_pos, node_color=node_color, with_labels = True)
    #plt.show()
    fig.savefig(name)
    plt.close(fig)

def test1():
    G = nx.Graph()
    G.add_node(0,pos=Point(6,12),color='green')
    G.add_node(1,pos=Point(2,8),color='green')
    G.add_node(2,pos=Point(5,4),color='green')
    G.add_node(3,pos=Point(10,4),color='green')
    G.add_node(4,pos=Point(12,9),color='green')

    paths = generate_paths(5)
    
    for path in paths:
        path.reverse()
        H = G.copy()
        try:
            steiner(H, path, [0,1,2,3,5])
        except WrongTreeException:
            continue
        draw_graph(H, name)


def graph2():
    G = nx.Graph()
    # G.add_node(0,pos=Point(0,0),color='green')
    # G.add_node(1,pos=Point(0,2),color='green')
    # G.add_node(2,pos=Point(4,0),color='green')
    # G.add_node(3,pos=Point(4,2),color='green')

    # G.add_node(0,pos=Point(0,0),color='green')
    # G.add_node(1,pos=Point(2,1),color='green')
    # G.add_node(2,pos=Point(4,0),color='green')
    # G.add_node(3,pos=Point(6,1),color='green')

    # G.add_node(0,pos=Point(0,0),color='green')
    # G.add_node(1,pos=Point(0,4),color='green')
    # G.add_node(2,pos=Point(4,0),color='green')
    # G.add_node(3,pos=Point(4,5),color='green')
    
    G.add_node(0,pos=Point(randint(0,100), randint(0,100)),color='green')
    G.add_node(1,pos=Point(randint(0,100), randint(0,100)),color='green')
    G.add_node(2,pos=Point(randint(0,100), randint(0,100)),color='green')
    G.add_node(3,pos=Point(randint(0,100), randint(0,100)),color='green')
    


    return G

def get_tree():
    G = graph2()
    paths = generate_paths(4)
    minimum = 1000
    steiner_tree = nx.empty_graph()
    for path in paths:
        name = str(path) + '.png'
        path.reverse()
        H = nx.Graph(G)
        try:
            steiner(H, path, [0,1,2,3])
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
            continue
        
        draw_graph(H, name)

    return steiner_tree

fig = plt.figure()
steiner_tree = get_tree()
node_color = nx.get_node_attributes(steiner_tree,'color')
node_color = list(node_color.values())
node_pos = nx.get_node_attributes(steiner_tree,'pos')
nx.draw(steiner_tree, pos=node_pos, node_color=node_color, with_labels = True)
plt.show()