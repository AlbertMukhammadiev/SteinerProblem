from unittest import TestCase, main
from sympy.geometry import Point
import networkx as nx
import matplotlib.pyplot as plt

from steiner import build_Steiner_tree, inv_replace, replace

class SteinerTestCase(TestCase):
    def setUp(self):
        """initial set up"""
        self.G = nx.Graph()
        self.G.add_node(0,pos=Point(0,0),color='green')
        self.G.add_node(1,pos=Point(0,2),color='green')
        self.G.add_node(2,pos=Point(4,0),color='green')
        self.G.add_node(3,pos=Point(4,2),color='green')

        self.path1 = [(0,1),((0,1),2)]
        self.path2 = [(0,3), ((0,3),1)]

        self.H = nx.Graph()
        self.H.add_node(0,pos=Point(3,3),color='green')
        self.H.add_node(1,pos=Point(3,7),color='green')
        self.H.add_node(2,pos=Point(11,7),color='green')
        self.H.add_node(3,pos=Point(11,3),color='green')


    def test_inv_replace1(self):
        """Verify correctness of replacement if there is intersection"""
        self.H.add_node((2,3),pos=Point(13,5),color='yellow')
        self.H.add_path([0, 1, (2,3)])
        inv_replace(self.H, (2,3))
        self.assertTrue(self.H.number_of_nodes() == 5)
        green_nodes = [u for u in self.H.nodes() if self.H.nodes[u]['color'] == 'green']
        self.assertListEqual(green_nodes, [0,1,2,3])
        steiner_nodes = [u for u in self.H.nodes() if self.H.nodes[u]['color'] == 'aqua']
        self.assertTrue(len(steiner_nodes) == 1)
        self.assertFalse(len(list(nx.isolates(self.H))))


    def test_inv_replace2(self):
        """Verify correctness of replacement if there is no intersection"""
        self.H.add_node((2,3),pos=Point(8,5),color='yellow')
        self.H.add_path([0, 1, (2,3)])
        inv_replace(self.H, (2,3))
        self.assertTrue(self.H.number_of_nodes() == 4)
        green_nodes = [u for u in self.H.nodes() if self.H.nodes[u]['color'] == 'green']
        self.assertListEqual(green_nodes, [0,1,2,3])
        self.assertTrue(self.H.has_edge(1,2))
        self.assertFalse(len(list(nx.isolates(self.H))))


    def test_replace(self):
        """Verify correctness of the nodes replacement"""
        replace(self.H, (2,3))
        self.assertTrue(self.H.number_of_nodes() == 5)
        green_nodes = [u for u in self.H.nodes() if self.H.nodes[u]['color'] == 'green']
        temp_nodes = [u for u in self.H.nodes() if self.H.nodes[u]['color'] == 'yellow']
        self.assertListEqual(green_nodes, [0,1,2,3])
        self.assertTrue(len(temp_nodes) == 1)


if __name__ == '__main__':
    main()