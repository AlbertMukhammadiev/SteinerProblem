import networkx as nx
import matplotlib.pyplot as plt
from sympy.geometry import Point, Segment2D, Circle, intersection, Line
from sympy import pi

from random import choice

base_color = 'green'
steiner_color = 'aqua'
temp_color = 'yellow'
candidates = dict()
name = ['1.png']
#path = [Point(5,0), Point(5/2), Point(40849364905389/12500000000000, 1), Point(0,2), Point(0,2), Point(0,0)]

def draw_graph2(G):
    for u in G.nodes():
        v = u.evalf()
        G.node[u]['pos'] = v

    node_color = nx.get_node_attributes(G,'color')
    node_color = list(node_color.values())

    node_pos = nx.get_node_attributes(G,'pos')
    nx.draw(G, pos=node_pos, node_color=node_color, with_labels = True)
    

    plt.axhline(0, color='black', linewidth=3)
    plt.axvline(0, color='black', linewidth=3)
    plt.axhline(-1, color='grey', linewidth=0.5)
    plt.axvline(-1, color='grey', linewidth=0.5)
    plt.axhline(1, color='grey', linewidth=0.5)
    plt.axvline(1, color='grey', linewidth=0.5)
    plt.axhline(2, color='grey', linewidth=0.5)
    plt.axvline(2, color='grey', linewidth=0.5)
    plt.axhline(-2, color='grey', linewidth=0.5)
    plt.axvline(-2, color='grey', linewidth=0.5)
    plt.show()

def create_graph():
    G = nx.Graph()
    G.add_node(1, pos=(0,1), color=base_color)
    G.add_node(2, pos=(0,-1), color=base_color)
    G.add_node(3, pos=(4,1), color=temp_color)
    G.add_node(4, pos=(5,0), color=base_color)
    G.add_node(5, pos=(4,-1), color=temp_color)
    G.add_node(6, pos=(1,0), color=steiner_color)

    G.add_edge(1, 6, color=base_color)
    G.add_edge(2, 6, color=base_color)
    G.add_edge(6, 4, color=base_color)
    G.add_edge(3, 4, color=base_color)
    G.add_edge(5, 4, color=base_color)

    return G


def create_triangle():
    G = nx.Graph()
    G.add_node(Point(0, 0), color=base_color)
    G.add_node(Point(0, 2), color=base_color)
    G.add_node(Point(1, 2), color=base_color)
    return G


def create_rectangle():
    G = nx.Graph()
    G.add_node(Point(0, 0), color=base_color)
    G.add_node(Point(0, 2), color=base_color)
    G.add_node(Point(5, 0), color=base_color)
    G.add_node(Point(5, 2), color=base_color)
    return G


def steiner(graph):
    

    if graph.number_of_nodes() == 2:
        graph.add_path(graph.nodes)
        return graph
    else:
        nodes = list(graph.nodes)
        u = choice(nodes)
        nodes.remove(u)
        v = choice(nodes)
        # u = path.pop()
        # v = path.pop()
        print(u)
        print(v)
        graph.remove_node(u)
        graph.remove_node(v)
        points = third_vertex(u, v)
        
        graph2 = nx.Graph(graph)
        graph2.add_node(points[1], color=temp_color)

        #draw_graph2(graph)


        fig = plt.figure()
        for_draw = nx.Graph(graph)
        for_draw.add_node(Point(-10, -10), color=base_color)
        for_draw.add_node(Point(10, 10), color=base_color)
        draw_graph2(for_draw)
        fig.savefig(name[0])
        name[0] = '1' + name[0]
        
        graph2 = steiner(graph2)

        #draw_graph2(graph)
        
        if inv_replace(graph2, points[1], u, v):
            return graph2
        else:
            graph.add_node(points[0], color=base_color)
            graph = steiner(graph)
            inv_replace(graph, points[0], u, v)
            return graph






def concatenate(G, u):
    if (G.number_of_nodes() == 1):
        G.add_node(u)
        G.add_edge(list(G.nodes)[0], u)
        return True

    dead_nodes = [v for v in G.nodes if sum(1 for _ in G.neighbors(v)) == 1]
    distances = [p.distance(u) for p in dead_nodes]
    minpos = distances.index(min(distances))

    neighbor = [v for v in G.neighbors(dead_nodes[minpos])].pop()
    line1, line2 = Line(u, dead_nodes[minpos]), Line(neighbor, dead_nodes[minpos])
    is_successful = line1.angle_between(line2) >= 2 / 3 * pi
    if is_successful:
        G.add_edge(u, dead_nodes[minpos])
        G.node[u]['color'] = base_color
    return is_successful


def third_vertex(u, v):
    radius = u.distance(v)
    c1 = Circle(u, radius, eval=True)
    c2 = Circle(v, radius)
    return [Point(tuple(p.evalf())) for p in intersection(c1, c2)]


def inv_replace(G, temp, u, v):
    neighbor = [w for w in G.neighbors(temp)].pop()
    circle = Circle(temp, u, v)
    segment = Segment2D(temp, neighbor)
    intersection_points = circle.intersect(segment)
    steiner_point = next((point for point in intersection_points if point != temp), None)

    if steiner_point is None:
        return False

    G.remove_node(temp)
    G.add_node(steiner_point)
    G.add_edge(steiner_point, u)
    G.add_edge(steiner_point, v)
    G.add_edge(steiner_point, neighbor)
    G.add_node(u)
    G.add_node(v)
    G.node[steiner_point]['color'] = steiner_color
    G.node[u]['color'] = base_color
    G.node[v]['color'] = base_color

    return True

G1 = create_rectangle()

G1 = steiner(G1)

# G1.add_path(G1.nodes)
# node_pos = nx.get_node_attributes(G1,'pos')
# nx.draw(G1, pos=node_pos, with_labels = True)

fig = plt.figure()
for_draw = nx.Graph(G1)
for_draw.add_node(Point(-10, -10), color=base_color)
for_draw.add_node(Point(10, 10), color=base_color)
draw_graph2(for_draw)
fig.savefig(name[0])
name[0] = '1' + name[0]