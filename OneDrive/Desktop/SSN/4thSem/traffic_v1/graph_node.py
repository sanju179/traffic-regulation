class Node:
    def __init__(self,node_name,traffic_number):
        self.name=node_name
        self.n1=0
        self.n2=0
        self.before_node={}
        self.after_node={}
        self.traffic_no=traffic_number


class Edge:
    def __init__(self,from_node,to_node): # these nodes must be objects and not the name of the node.
        self.frm=from_node
        self.to=to_node
        self.wt=None

    def assign_wt(self,weight):
        self.wt=weight
        
class Graph:
    def __init__(self):
        self.vertices=0
        self.edges=0
        self.nodes=[]
        self.edges_lst=[]
        
    def insert_node(self,name,traffic_no):
        node=Node(name,traffic_no) # object of the node
        self.nodes.append(node)
        self.vertices+=1
        return
    
    def insert_edge(self,from_edge,to_edge):
        #print(from_edge,to_edge)
        sum=0

        for i in self.nodes:
            if i.name==from_edge or i.name==to_edge:
                sum+=1
            if i.name==from_edge:
                f=i
            if i.name==to_edge:
                t=i
                
        if sum!=2:
            print('The entered nodes are not in the graph or map')

        edge_ob=Edge(f,t)
        traffic_wt_1=f.traffic_no
        traffic_wt_2=t.traffic_no

        #weight calculation (to be edited) - considering density and distance
        wt=(traffic_wt_1+traffic_wt_2)/2
        edge_ob.assign_wt(wt)


        for k in self.nodes:
            if k.name==from_edge:
                i=k
            if k.name==to_edge:
                j=k
        f.after_node[edge_ob]=wt
        f.n2+=1
        t.before_node[edge_ob]=wt
        t.n1+=1
        
        self.edges+=1
        self.edges_lst.append(edge_ob)  
        return
        
    def print_graph(self):
        for i in self.nodes:
            print(i.name,i.n1,i.n2,i.before_node,i.after_node)
            
    def dijkstra(self,source_node, dest_node):
        source=None
        # complexity = O(N)
        # find the source address
        for i in self.nodes:
            if i.name==source_node:
                source=i
                break
            
        # complexity = O(N)
        # updating dictionaries
        inf=999999999999999999
        dis_dict={}
        path_dict={}
        for i in self.nodes:
            if i==source:
                dis_dict[i.name]=0
                path_dict[i.name]=None
                continue
            
            dis_dict[i.name]=inf
            path_dict[i.name]=[]
            
        #print(path_dict,dis_dict)
        
        # TIME COMPLEXITY = O(V*E)
        
        queue=[source]
        
        while queue:
            x=queue.pop(-1)
            
            for j in self.edges_lst:
                if j.frm==x and dis_dict[x.name]+j.wt<dis_dict[j.to.name]:
                    # we have to check for the condition and then update the dictionaries
                    
                        
                    queue.append(j.to)
                    dis_dict[j.to.name]=dis_dict[x.name]+j.wt
                    
                    path_dict[j.to.name].append(j.frm.name) 
                    # if the path is more we are supposed to del the list and create a new path
                    
                    #break
                
            #break
        
        print(queue,dis_dict,path_dict)

        curr = dest_node
        optimal_path = [curr]
        while curr != source_node:
            curr = path_dict[curr][-1]
            optimal_path.append(curr)
        print(optimal_path[::-1])
        return optimal_path[::-1]

    
    

""" 

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

ob.print_graph()
ob.dijkstra('A','F')


 """
""" 
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

ob.print_graph()
ob.dijkstra('A','D') """
#self.assertEqual(ob.dijkstra('A','D'), ['A', 'B', 'D'])
        