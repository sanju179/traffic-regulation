import unittest
from graph_node import *

class Graph_Test(unittest.TestCase):

    def test_dijkstra(self):

        """*************FIRST TEST CASE***************"""  
        ob=Graph()
        ob.insert_node('A',1)
        ob.insert_node('B',9)
        ob.insert_node('C',7)
        ob.insert_node('D',3)
        ob.insert_node('E',1)
        ob.insert_node('F',1)
        ob.insert_edge('A','B')
        ob.insert_edge('B','D')
        ob.insert_edge('D','F')
        ob.insert_edge('A','C')
        ob.insert_edge('C','E')
        ob.insert_edge('E','F')

        #ob.print_graph()
    
        self.assertEqual(ob.dijkstra('A','F'), ['A', 'C', 'E', 'F'])

        """*************SECOND TEST CASE***************"""

        ob=Graph()
        ob.insert_node('A',4)
        ob.insert_node('B',6)
        ob.insert_node('C',8)
        ob.insert_node('D',2)
        ob.insert_node('E',2)

        ob.insert_edge('A','B')
        ob.insert_edge('B','D')
        ob.insert_edge('A','C')
        ob.insert_edge('C','D')
        ob.insert_edge('C','B')
        ob.insert_edge('C','E')
        ob.insert_edge('E','A')
        ob.insert_edge('E','D')

        self.assertEqual(ob.dijkstra('A','D'), ['A', 'B', 'D'])
        
if __name__ == "__main__":
    unittest.main()