'''This program impletments a  ery simple algorithm to infect a network, 
    selecting one node at random and then at a rate p, will attempt to infect other nodes 
'''
import networkx as nx #Adds the networkx package, used to create graph objects
import numpy as np #Numpy is needed for matrix manipulation
import random as rand #Random helps for random numbers
import matplotlib.pyplot as plt #A library to plot graphs
from copy import deepcopy #used to compare the starting graph with the end result

class infection_graph(): #Creates a class based off the grapgh we are going to analyise and sorts important data about said graph
    def __init__(self,network):
        self.graph = network #Stores the graph we are studying 
        self.infected = set() #Initalises the empty list
        vertices = list(nx.nodes(self.graph))
        length = len(vertices)
        r_number = rand.randrange(0,length)
        self.infected.add(vertices[r_number]) #Picks a vertex at random to start the infection
        zeros = [0]*length
        self.daysinfected = dict(zip(vertices,zeros))
        self.new_node_name = len(vertices)
    def __repr__(self):
        b = f'{self.infected}' #the __repr__ returns a readable version of the lsit of infected nodes
        return b
    def die_or_recover(self,node,r: float):
        r_no = rand.randrange(0,10001)
        if r_no < 10000*r:
            self.infected.discard(node)
            self.daysinfected.update({node:0})
            return(f'{node=} HAS RECOVERD')
        else:
            self.infected.discard(node)
            self.graph.remove_node(node)
            return(f'{node=} HAS DIED')
    def birth(self,b_r):
        r = rand.randrange(0,10001)
        if r < 10000*b_r:
            nodes = list(nx.nodes(self.graph))
            new_node = self.new_node_name
            self.new_node_name += 1
            T = True
            attempt = 0
            parent_1 = nodes[rand.randrange(0,len(nodes))]
            p1neighbours = list(nx.neighbors(self.graph,parent_1))
            if len(p1neighbours) != 0:
                parent_2 = p1neighbours[rand.randrange(0,len(p1neighbours))]

                try:
                    connect = list(nx.neighbors(self.graph,parent_2))
                except nx.NetworkXError:
                    f = plt.figure('Staring graph')
                    subax1 = plt.subplot(121)
                    nx.draw(self.graph,with_labels=True)
                    f.show()
                    input()


                self.graph.add_node(new_node) 
                self.graph.add_edge(parent_1,new_node)
                self.graph.add_edge(parent_2,new_node)
                self.daysinfected.update({new_node:0})
                return f'{new_node=},between {parent_1} and {parent_2}'
            else:
                return f'No One was Born'
        else:
            return f'No One was Born'


def infect(infclass: infection_graph,p: float):#function to infect a vertex, p is the probaility of infection use a float 
    spreaders = []
    for i in infclass.infected: #this part gets all the neighburs of each infected node ready to then attempt to infect them
        k = nx.all_neighbors(infclass.graph, i)
        for n in k:
            spreaders.append(n)
    for node in spreaders:#for each node in the spreaders list the rate of infection is p and will be added  to the infected class
        r_no = rand.randrange(0,10001)
        if r_no < 10000*p:
            infclass.infected.add(node)
        else:
            pass

    

def random(node):
    r1 = rand.randrange(0,len(node))
    r2 = rand.randrange(0,len(node))
    return r1,r2   





def main(no_nodes: int, edges: int, p_i: float, p_r: float,enable_vis: bool):
    #Letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    #graph =  np.matrix('0 1 1; 1 0 0; 1 0 0')
    #G = nx.from_numpy_matrix(graph)
    G = nx.barabasi_albert_graph(no_nodes,edges)
    #Numbers = range(nx.number_of_nodes(G))
    #labels = dict(zip(Numbers,Letters))
    #G = nx.relabel_nodes(G,labels)
    cp_G = deepcopy(G)
    list_of_nodes = list(nx.nodes(G))
    A = infection_graph(G)

    counter = 0
    for i in range(100000):
        print(A.infected)
        infect(A,p_i)
        print(A.daysinfected)
        for key in A.daysinfected:
            if key in A.infected:
                A.daysinfected[key] += 1
                if A.daysinfected[key] > 10:
                    print(A.die_or_recover(key,p_r))
            else:
                A.daysinfected.update({key:0})
        print(A.birth(0.6))







        #print(repr(A))
        #print(set(A.infected))
        #if A.infected == set(nx.nodes(A.graph)):
        #    print('INFECTED')
        #    print(set(A.infected))
        #    break
        if len(A.infected) == 0:
            if len(nx.nodes(A.graph)) == 0:
                print('Everyone died')
                if enable_vis == 'True':
                    f = plt.figure('Staring graph')
                    subax1 = plt.subplot(121)
                    nx.draw(cp_G,with_labels=True)
                    f.show()
                    input()
            else:
                print('Everyone became immune')
                surviors = list(nx.nodes(A.graph))
                print(f'{surviors=}')
                no_of_surviors = len(surviors)
                print(f'{no_of_surviors=}')
                if enable_vis == 'True':
                    f = plt.figure('Starting Graph')
                    subax1 = plt.subplot(121)
                    nx.draw(cp_G,with_labels=True)
                    f.show()
                    g = plt.figure('The Surviors')
                    subax1 = plt.subplot(121)
                    nx.draw(A.graph,with_labels=True)
                    g.show()
                    input()
            print(counter)
            break
                
            

        counter += 1
        print(counter)


if __name__ == '__main__':
    n,e,p_i,p_r = input('Number of Nodes:'),input('Number of initial edges:'),input('Probaility of infection:'),input('Probability to Recover:')
    enable_vis = input('Show Graphs?:')
    n,e,p_i,p_r = int(n),int(e),float(p_i),float(p_r)
    main(n,e,p_i,p_r,enable_vis)



















