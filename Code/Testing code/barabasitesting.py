import networkx as nx; import numpy as np; import matplotlib.pyplot as plt; import pysnooper
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
    match choice:
        case 'W':
            return nx.wheel_graph(5)
        case 'C':
            return nx.cycle_graph(5)
        case 'K':
            return nx.complete_graph(5)
        case 'S':
            return nx.star_graph(5)
        case 'R':
            return nx.erdos_renyi_graph(5,0.9)
        case _:
            graphchoice()    
        
        
        
        
        
        
#@pysnooper.snoop()
def main(): 

    G = colourgraph(graphchoice())
    print(repr(G))
    F = colourgraph(nx.barabasi_albert_graph(30,5,initial_graph=G.graph))
    print(repr(F))




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