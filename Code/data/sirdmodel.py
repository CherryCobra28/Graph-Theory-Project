'''This program impletments a  ery simple algorithm to infect a network, 
    selecting one node at random and then at a rate p, will attempt to infect other nodes 
'''
import networkx as nx #Adds the networkx package, used to create graph objects
import numpy as np #Numpy is needed for matrix manipulation
import random as rand #Random helps for random numbers
import matplotlib.pyplot as plt #A library to plot graphs
from copy import deepcopy #used to compare the starting graph with the end result
import pandas as pd




class infection_graph(): #Creates a class based off the grapgh we are going to analyise and sorts important data about said graph
    def __init__(self,network):
        self.graph = network #Stores the graph we are studying 
        self.infected = set() #Initalises the empty list
        self.degrees = dict(nx.degree(network))
        self.colours = dict()
        self.histogram = dict(enumerate(nx.degree_histogram(network)))
        self.highestdegree = list(self.histogram)[-1]
        #self.diameter = nx.diameter(network)
        vertices = list(nx.nodes(self.graph))
        length = len(vertices)
        r_number = rand.randrange(0,length)
        self.infected.add(vertices[r_number]) #Picks a vertex at random to start the infection
        zeros = [0]*length
        self.daysinfected = dict(zip(vertices,zeros))
        self.colour()
    def __repr__(self):
        b = f'{self.degrees}\n{self.histogram=}\n{self.highestdegree=}\n{self.diameter=} ' #the __repr__ returns a readable version of the lsit of infected nodes
        return b
    def die_or_recover(self,node,r: float):
        r_no = rand.random()
        if r_no < r:
            self.infected.discard(node)
            self.daysinfected.update({node:0})
            return(f'{node=} HAS RECOVERD')
        else:
            self.infected.discard(node)
            self.graph.remove_node(node)
            self.daysinfected.update({node:0})
            self.colours.pop(node)
            return(f'{node=} HAS DIED')
    def colour(self):
        for key in self.degrees:
            if self.degrees[key] == self.highestdegree:
                self.colours.update({key:'yellow'})
            elif 5 < self.degrees[key] < self.highestdegree :
                self.colours.update({key:'green'})
            else:
                self.colours.update({key:'blue'})

class cgraph:
    def __init__(self,network):
        self.graph = network 
        self.degrees = dict(nx.degree(network))
        self.colours = []
        self.histogram = dict(enumerate(nx.degree_histogram(network)))
        self.highestdegree = list(self.histogram)[-1]
        #self.diameter = nx.diameter(network)
        self.colour()
    def __repr__(self):
        return f'{self.degrees=}\n {self.histogram=}\n {self.highestdegree=}\n {self.diameter=}'
    def colour(self):
        for key in self.degrees:
            if self.degrees[key] == self.highestdegree:
                self.colours.append('yellow')
            elif 5 < self.degrees[key] < self.highestdegree :
                self.colours.append('green')
            else:
                self.colours.append('blue')
        

def infect(infclass: infection_graph,p: float):#function to infect a vertex, p is the probaility of infection use a float 
    spreaders = []
    for i in infclass.infected: #this part gets all the neighburs of each infected node ready to then attempt to infect them
        k = nx.all_neighbors(infclass.graph, i)
        for n in k:
            spreaders.append(n)
    for node in spreaders:#for each node in the spreaders list the rate of infection is p and will be added  to the infected class
        r_no = rand.random()
        if r_no < p:
            infclass.infected.add(node)
        else:
            pass
    





def main(no_nodes: int, edges: int, p_i: float, p_r: float,enable_vis: bool):
    G = nx.barabasi_albert_graph(no_nodes,edges)
    cp_G = deepcopy(G)
    
    list_of_nodes = list(nx.nodes(G))
    A = infection_graph(G)
    B = cgraph(cp_G)

    counter = 0
    for i in range(100000):
        #print(A.infected)
        infect(A,p_i)
        #print(A.daysinfected)
        for key in A.daysinfected:
            if key in A.infected:
                A.daysinfected[key] += 1
                if A.daysinfected[key] > 10:
                    #print(A.die_or_recover(key,p_r))
                    A.die_or_recover(key,p_r)








        #print(repr(A))
        #print(set(A.infected))
        #if A.infected == set(nx.nodes(A.graph)):
        #    print('INFECTED')
        #    print(set(A.infected))
        #    break
        if len(A.infected) == 0:
            if len(nx.nodes(A.graph)) == 0:
               #print('Everyone died')
                no_of_surviors = 0
                if enable_vis == 'True':
                    f = plt.figure('Staring graph')
                    #subax1 = plt.subplot(121)
                    nx.draw(B.graph,node_colours = B.colours,with_labels=True)
                    f.show()
                    input()
            else:
                #print('Everyone became immune')
                surviors = list(nx.nodes(A.graph))
                #print(f'{surviors=}')
                no_of_surviors = len(surviors)
                #print(f'{no_of_surviors=}')
                
                if enable_vis == 'True':
                    f = plt.figure('Starting Graph')
                    #subax1 = plt.subplot(121)
                    nx.draw_networkx(B.graph,node_color = B.colours ,with_labels=True)
                    f.show()
                    g = plt.figure('The Surviors')
                    #subax1 = plt.subplot(121)
                    nx.draw(A.graph,node_color = A.colours.values(),with_labels=True)
                    g.show()
                    input()
            #print(counter)
            if no_of_surviors == 0:
                total_death = True
            else:
                total_death = False
            print(no_of_surviors)
            return {'n':no_nodes,'edges added': edges,'P_i': p_i,'P_r': p_r,'Days_Taken': counter, 'Surviors': no_of_surviors,'Everyone_Dead':total_death}
                
            

        counter += 1
        #print(counter)
    




if __name__ == '__main__':
    n,e,p_i,p_r = input('Number of Nodes:'),input('Number of initial edges:'),input('Probaility of infection:'),input('Probability to Recover:')
    enable_vis = input('Show Graphs?:')
    n,e,p_i,p_r = int(n),int(e),float(p_i),float(p_r)
    main(n,e,p_i,p_r,enable_vis)



















