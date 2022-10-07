'''This program impletments a  ery simple algorithm to infect a network, 
    selecting one node at random and then at a rate p, will attempt to infect other nodes 
'''
import networkx as nx #Adds the networkx package, used to create graph objects
import numpy as np #Numpy is needed for matrix manipulation
import random as rand #Random helps for random numbers
import matplotlib.pyplot as plt


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
    def __repr__(self):
        b = f'{self.infected}' #the __repr__ returns a readable version of the lsit of infected nodes
        return b
    def die_or_recover(self,node,r: float):
        r_no = rand.randrange(0,101)
        if r_no < 100*r:
            self.infected.discard(node)
            self.daysinfected.update({node:0})
            return(f'{node=} HAS RECOVERD')
        else:
            self.infected.discard(node)
            self.graph.remove_node(node)
            self.daysinfected.update({node:0})
            return(f'{node=} HAS DIED')



def infect(infclass: infection_graph,p: float):#function to infect a vertex, p is the probaility of infection use a float 
    spreaders = []
    for i in infclass.infected: #this part gets all the neighburs of each infected node ready to then attempt to infect them
        k = nx.all_neighbors(infclass.graph, i)
        for n in k:
            spreaders.append(n)
    for node in spreaders:#for each node in the spreaders list the rate of infection is p and will be added  to the infected class
        r_no = rand.randrange(0,101)
        if r_no < 100*p:
            infclass.infected.add(node)
        else:
            pass
    





def main():
    Letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    #graph =  np.matrix('0 1 1; 1 0 0; 1 0 0')
   # G = nx.from_numpy_matrix(graph)
    G = nx.barabasi_albert_graph(10,1)
    adj = nx.to_numpy_array(G)
    Numbers = range(nx.number_of_nodes(G))
    labels = dict(zip(Numbers,Letters))
    G = nx.relabel_nodes(G,labels)
    cp_G = nx.from_numpy_array(adj)
    cp_G = nx.relabel_nodes(cp_G,labels)
    list_of_nodes = list(nx.nodes(G))
    A = infection_graph(G)


    counter = 0
    for i in range(100):
        print(A.infected)
        infect(A,0.5)
        print(A.daysinfected)
        for key in A.daysinfected:
            if key in A.infected:
                A.daysinfected[key] += 1
                if A.daysinfected[key] > 10:
                    print(A.die_or_recover(key,0.5))








        #print(repr(A))
        #print(set(A.infected))
        #if A.infected == set(nx.nodes(A.graph)):
        #    print('INFECTED')
        #    print(set(A.infected))
        #    break
        if len(A.infected) == 0:
            if len(nx.nodes(A.graph)) == 0:
                print('Everyone died')
                subax1 = plt.subplot(121)
                nx.draw(cp_G,with_labels=True)
                plt.show()
            else:
                print('Everyone became immune')
                surviors = list(nx.nodes(A.graph))
                print(f'{surviors=}')
                subax1 = plt.subplot(121)
                nx.draw(cp_G,with_labels=True)
                plt.show()
            print(counter)
            break
                
            

        counter += 1
        print(counter)


if __name__ == '__main__':
    main()



















