import random
import networkx as nx
import matplotlib.pyplot as plt
import os

class Node:
    def __init__(self, node_name, traffic_number):
        self.name = node_name
        self.n1 = 0
        self.n2 = 0
        self.before_node = {}
        self.after_node = {}
        self.traffic_no = traffic_number

class Edge:
    def __init__(self, from_node, to_node, distance):
        self.frm = from_node
        self.to = to_node
        self.wt = None
        self.distance = distance

    def assign_wt(self, weight):
        self.wt = weight

class Graph:
    def __init__(self):
        self.vertices = 0
        self.edges = 0
        self.nodes = []
        self.edges_lst = []
        
    def insert_node(self, name, traffic_no):
        node = Node(name, traffic_no)
        self.nodes.append(node)
        self.vertices += 1
    
    def insert_edge_oneway(self, from_edge, to_edge, distance):
        sum = 0

        for i in self.nodes:
            if i.name == from_edge or i.name == to_edge:
                sum += 1
            if i.name == from_edge:
                f = i
            if i.name == to_edge:
                t = i
                
        if sum != 2:
            print('The entered nodes are not in the graph or map')

        edge_ob = Edge(f, t, distance)
        a = f.traffic_no
        b = t.traffic_no

        wt = (a + b) / 2
        edge_ob.assign_wt((1/(wt+int(float(distance))))*1000)

        f.after_node[edge_ob] = wt
        f.n2 += 1
        t.before_node[edge_ob] = wt
        t.n1 += 1
        
        self.edges += 1
        self.edges_lst.append(edge_ob)  
    
    def print_graph(self):
        for i in self.nodes:
            print(i.name, i.n1, i.n2, i.before_node, i.after_node)
            
    def dijkstra(self, source_node, dest_node):
        source = None
        distance=0

        for i in self.nodes:
            if i.name == source_node:
                source = i
                break
            
        inf = float("inf")
        dis_dict = {}
        path_dict = {}
        for i in self.nodes:
            if i == source:
                dis_dict[i.name] = 0
                path_dict[i.name] = None
                continue
            
            dis_dict[i.name] = inf
            path_dict[i.name] = []
        
        queue = [source]
        
        while queue:
            x = queue.pop(0)
            
            for j in self.edges_lst:
                if j.frm == x and dis_dict[x.name] + j.wt > dis_dict[j.to.name]:
                    queue.append(j.to)
                    dis_dict[j.to.name] = int(dis_dict[x.name] + j.wt)
                    path_dict[j.to.name].append(j.frm.name)
        
        curr = dest_node
        optimal_path = [curr]
        while curr != source_node:
            curr = path_dict[curr][-1]
            optimal_path.append(curr)
        
        path=optimal_path[::-1]
        
        
        distance=dis_dict[dest_node]
        return path,distance


    def find_weight(self, wt_1, wt_2):
        x = random.randrange(5, 9)
        y = random.randrange(5, 9)
        a = (wt_1 / 10) * x
        b = (wt_2 / 10) * y
        return x, a, b
    
    def density(self, x, distance):
        if x == 5:
            return 900 / distance
        elif x == 6:
            return 700 / distance
        elif x == 7:
            return 500 / distance
        elif x == 8:
            return 300 / distance
        else:
            return 100 / distance

    def insert_edge_twoway(self, from_edge, to_edge, distance):
        self.insert_edge_oneway(from_edge, to_edge, distance)
        self.insert_edge_oneway(to_edge, from_edge, distance)


def run(start,end,mode):
    ob = Graph()

    ob.insert_node('A', 4)
    ob.insert_node('B', 6)
    ob.insert_node('C', 8)
    ob.insert_node('D', 2)
    ob.insert_node('E', 2)
    ob.insert_node('F', 7)
    ob.insert_node('G', 5)
    ob.insert_node('H', 3)
    ob.insert_node('I', 9)

    ob.insert_edge_oneway('A', 'B', 10)
    ob.insert_edge_oneway('B', 'D', 20)
    ob.insert_edge_twoway('A', 'C', 10)
    ob.insert_edge_twoway('G', 'D', 5)
    ob.insert_edge_oneway('C', 'B', 10)
    ob.insert_edge_oneway('C', 'E', 20)
    ob.insert_edge_oneway('E', 'A', 10)
    ob.insert_edge_twoway('E', 'D', 20)
    ob.insert_edge_twoway('B', 'F', 15)
    ob.insert_edge_twoway('C', 'G', 18)
    ob.insert_edge_twoway('E', 'H', 25)
    ob.insert_edge_twoway('H', 'I', 17)
    ob.insert_edge_twoway('A', 'G', 20)
    ob.insert_edge_oneway('I', 'F', 10)
    ob.insert_edge_twoway('I', 'C', 20)
    ob.insert_edge_oneway('H', 'G', 10)
    x,dis = ob.dijkstra(start, end)
    

    graph = nx.DiGraph()
    for node in ob.nodes:
        graph.add_node(node.name, traffic_no=node.traffic_no)
    for edge in ob.edges_lst:
        graph.add_edge(edge.frm.name, edge.to.name, weight=int(edge.wt))

    # Adjusting the edge lengths based on the edge weights
    pos = nx.circular_layout(graph)

    # Drawing the graph using networkx and matplotlib
    nx.draw_networkx(
        graph,
        pos,
        with_labels=True,
        labels={node: node for node in graph.nodes()},
        node_size=500,
        node_color='lightblue',
        edge_color='black'
    )

    # To Add edge labels
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

    # Get the current working directory
    current_directory = os.getcwd()

    # Create the path to the 'flasktest' folder
    """ flasktest_folder_path = os.path.join(current_directory, 'flasktest')

    # Create the 'flasktest' directory if it doesn't exist
    if not os.path.exists(flasktest_folder_path):
        os.makedirs(flasktest_folder_path)
 """
    # Create the path to the 'static' folder within 'flasktest'
    static_folder_path = os.path.join(current_directory, 'static')

    # Create the 'static' directory if it doesn't exist
    if not os.path.exists(static_folder_path):
        os.makedirs(static_folder_path)


    plt.title('Graph Visualization')
    plt.axis('off')
    plt.savefig(os.path.join(static_folder_path, 'graph_before_dijkstra.png'))
    if mode == 0:
        plt.show()

    # Dijkstra
    nx.draw_networkx(
        graph,
        pos,
        with_labels=True,
        labels={node: node for node in graph.nodes()},
        node_size=500,
        node_color='lightblue',
        edge_color='black'
    )
    edge_labels = nx.get_edge_attributes(graph, 'weight')

    # Highlight the shortest path
    path = ob.dijkstra(str(start), str(end))
    print(path)
    path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    for edge in graph.edges:
        if (edge[0], edge[1]) in path_edges or (edge[1], edge[0]) in path_edges:
            graph.edges[edge]['color'] = 'springgreen'
        else:
            graph.edges[edge]['color'] = 'red'

    edge_colors = [graph.edges[edge]['color'] for edge in graph.edges]
    weights = [edge_labels[edge] / 5.5 for edge in graph.edges]
    nx.draw_networkx_edges(
        graph,
        pos,
        edgelist=graph.edges,
        edge_color=edge_colors,
        width=weights
    )

    # Add edge labels
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

    plt.title('Shortest Path Visualization')
    plt.axis('off')
    plt.savefig(os.path.join(static_folder_path, 'graph_after_dijkstra.png'))
    if mode == 0:
        plt.show()
    return (str(x),dis)

if __name__ == "__main__":
    run('A','F',1)
