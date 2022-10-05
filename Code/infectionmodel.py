'''This program impletments a  ery simple algorithm to infect a network, 
    selecting one node at random and then at a rate p, will attempt to infect other nodes 
'''
import networkx as nx #Adds the networkx package, used to create graph objects
import numpy as np #Numpy is needed for matrix manipulation
import random as rand #Random helps for random numbers

class infection_graph(): #Creates a class based off the grapgh we are going to analyise and sorts important data about said graph
    def __init__(self,network):
        self.graph = network #Stores the graph we are studying 
        self.infected = [] #Initalises the empty list
        vertices = list(nx.nodes(self.graph))
        length = len(vertices)
        r_number = rand.randrange(0,length)
        self.infected.append(vertices[r_number]) #Picks a vertex at random to start the infection
    def __repr__(self):
        b = f'{self.infected}' #the __repr__ returns a readable version of the lsit of infected nodes
        return b
    def app(self,new_infected):
        self.infected.append(new_infected) #Method to append values to the infected_graph class


def infect(infclass: infection_graph,p: float):#function to infect a vertex, p is the probaility of infection use a float 
    spreaders = []
    for i in infclass.infected: #this part gets all the neighburs of each infected node ready to then attempt to infect them
        k = nx.all_neighbors(infclass.graph, i)
        for n in k:
            spreaders.append(n)
    for node in spreaders:#for each node in the spreaders list the rate of infection is p and will be added  to the infected class
        r_no = rand.randrange(0,101)
        if r_no < 100*p:
            infclass.infected.append(node)
        else:
            pass





def main():
    Letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    graph =  np.matrix('0 1 1; 1 0 0; 1 0 0')
    G = nx.from_numpy_matrix(graph)
    Numbers = range(nx.number_of_nodes(G))
    labels = dict(zip(Numbers,Letters))
    G = nx.relabel_nodes(G,labels)
    list_of_nodes = list(nx.nodes(G))
    A = infection_graph(G)


    counter = 0
    for i in range(1000):
        infect(A,0.5)
        print(repr(A))
        print(set(A.infected))
        if set(A.infected) == set(nx.nodes(A.graph)):
            print('INFECTED')
            break
        counter += 1
        print(counter)


if __name__ == '__main__':
    main()



















