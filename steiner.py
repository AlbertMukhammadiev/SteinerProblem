import networkx as nx
import matplotlib.pyplot as plt
from sympy.geometry import Point, Line2D, Segment2D, Circle, intersection, Line, Curve

removed_color = 'white'
temp_color = 'yellow'
base_color = 'green'
steiner_color = 'aqua'

def magic_point(point):
    return Point(tuple(point.evalf()))


def replace(G, pair):
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

    
    G.add_node(pair, pos=magic_point(position_third), color=temp_color)
    #G.add_node(pair, pos=position_third.evalf(), color=temp_color)
    #G = nx.Graph()
    #G.add_path([pair[0], pair, pair[1]])


def inv_replace(G, temp):
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


def steiner(G, path, nodes, num=[1]):
    if len(nodes) == 2:
        G.add_path(nodes)
        return
    
    pair = path.pop()
    nodes.remove(pair[0])
    nodes.remove(pair[1])
    nodes.append(pair)
    replace(G, pair)

    # node_color = nx.get_node_attributes(G,'color')
    # node_color = list(node_color.values())
    # node_pos = nx.get_node_attributes(G,'pos')
    # nx.draw(G, pos=node_pos, node_color=node_color, with_labels = True)
    # plt.show()
    # plt.subplot(3,2,num[0])
    # num[0] = num[0] + 1

    steiner(G, path, nodes)

    # node_color = nx.get_node_attributes(G,'color')
    # node_color = list(node_color.values())
    # node_pos = nx.get_node_attributes(G,'pos')
    # nx.draw(G, pos=node_pos, node_color=node_color, with_labels = True)
    # plt.show()
    # plt.subplot(3,2,num[0])
    # num[0] = num[0] + 1

    inv_replace(G, pair)

    # node_color = nx.get_node_attributes(G,'color')
    # node_color = list(node_color.values())
    # node_pos = nx.get_node_attributes(G,'pos')
    # nx.draw(G, pos=node_pos, node_color=node_color, with_labels = True)
    # plt.show()
    # plt.subplot(3,2,num[0])
    # num[0] = num[0] + 1