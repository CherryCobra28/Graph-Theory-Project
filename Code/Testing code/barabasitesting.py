import networkx as nx; import numpy as np; import matplotlib.pyplot as plt; import math
class colourgraph:
    def __init__(self,g):
        self.graph = g
        self.degrees = dict(nx.degree(g))
        self.colours = []
        self.histogram = dict(enumerate(nx.degree_histogram(g)))
        self.highestdegree = list(self.histogram)[-1]
        self.diameter = nx.diameter(g)
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
        
def graphchoice():
    choice = input('Wheel, Cycle, Komplete, Star, Random')      
    
    if choice == 'W':
        return nx.wheel_graph(5)
    elif choice == 'C':
        return nx.cycle_graph(5)
    elif choice == 'K':
        return nx.complete_graph(5)
    elif choice == 'S':
        return nx.star_graph(5)
    elif choice == 'R':
        return nx.erdos_renyi_graph(5,0.9)
    else:
        graphchoice()    
        
        
        
        
        
        
#@pysnooper.snoop()
def main(): 

    G = graphchoice()
    N = 100
    F = nx.barabasi_albert_graph(N,4,initial_graph=G)
    d = (math.log(N))/(math.log(math.log(N)))
    print(f'{nx.diameter(F)},{d=},ratio = {d/nx.diameter(F)}')
    c_bar = nx.average_clustering(F)
    c_est = ((math.log(N))**2)/N
    print(f'{c_bar=},{c_est=},ratio = {c_est/c_bar}')
    print(nx.transitivity(F))
    f = plt.figure('Starting Graph')
    #subax1 = plt.subplot(111)
    nx.draw(G.graph,node_color = G.colours,with_labels=True)
    f.show()
    g = plt.figure('Barabasi-Albert Model')
    #subax1 = plt.subplot(111)
    nx.draw(F.graph,node_color = F.colours,with_labels=True)
    g.show()
    input()
main()