import networkx as nx
from math import floor
import matplotlib.pyplot as plt
class cgraph:
    '''This is just a copy of the above class to process the orginal graph before the infection '''
    def __init__(self,network):
        self.graph = network 
        self.degrees = dict(nx.degree(network))
        self.colours = []
        self.histogram = dict(enumerate(nx.degree_histogram(network)))
        self.highestdegree = list(self.histogram)[-1]
        self.colour()
    def stats(self):
        return {'histogram':self.histogram, 'highest_degree':self.highestdegree,'Diameter':self.diameter}
    def colour(self):
        hubsize = floor(len(self.histogram)/2)
        hub = list(self.histogram)[hubsize]
        print(hub)
        
        for key in self.degrees:
            if self.degrees[key] == self.highestdegree:
                self.colours.append('yellow')
            elif hub < self.degrees[key] < self.highestdegree :
                self.colours.append('green')
            else:
                self.colours.append('blue')
                
G = nx.barabasi_albert_graph(20,5)

graph = cgraph(G)


nx.draw_networkx(graph.graph,node_color = graph.colours ,with_labels=True)
plt.show()
input()
