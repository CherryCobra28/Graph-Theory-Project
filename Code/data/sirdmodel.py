'''
This program impletments an algorithm to infect a network, 
selecting one node at random and then at a rate p, will attempt to infect other nodes
 
'''
import networkx as nx #Adds the networkx package, used to create graph objects
import random as rand #Random helps for random numbers
import matplotlib.pyplot as plt #A library to plot graphs
from copy import deepcopy #used to compare the starting graph with the end result




class infection_graph(): #Creates a class based off the grapgh we are going to analyise and sorts important data about said graph
    def __init__(self,network):
        self.graph = network #Stores the graph we are studying 
        self.infected = set() #Initalises the empty list
        self.degrees = dict(nx.degree(network)) #returns a dictionary with the nodes as keys and their degree as value
        self.colours = dict() #Initialises the colour dict that we use to colour nodes in the graph
        self.histogram = dict(enumerate(nx.degree_histogram(network)))#Creates a dictionary where the degree is the key and the frequency of that degree is the value
        self.highestdegree = list(self.histogram)[-1] #Gives the last element of the histogram to give the highest degree
        self.diameter = nx.diameter(network) #Returns the furthest distance between nodes in the graph
        vertices = list(nx.nodes(self.graph))
        r_number = rand.randrange(0,len(vertices))
        self.infected.add(vertices[r_number]) #Picks a vertex at random to start the infection
        zeros = [0]*len(vertices)
        self.daysinfected = dict(zip(vertices,zeros))#Keeps count of how long each node has been infected
        self.colour() #Colours the nodes
    def __repr__(self):
        '''The __repr__ returns readable info about the graph, here it gives the: degrees of each node,
        the histogram of the degrees, the highest degree in the graph aka the super hubs and the diameter of the graph'''
        b = f'{self.degrees}\n{self.histogram=}\n{self.highestdegree=}\n{self.diameter=} '
        return b
    def die_or_recover(self,node,r: float):
        '''This Method runs after a node has been infceted for k days and will attempt to allow the node to recover at p = r
        or die at p = 1-r'''
        r_no = rand.random()
        if r_no < r:
            '''if we succeed then the node is removed from the infceted list and the time its spent infected is put back to 0'''
            self.infected.discard(node)
            self.daysinfected.update({node:0})
            return(f'{node=} HAS RECOVERD')
        else:
            '''however if it fails the node is killed, being removed from the infceted list, removed from the graph, has its time infected
            put to 0 and is removed from the colours list to make sure the plot later doesnt attempt to colour a node
            that doesnt exist'''
            self.infected.discard(node)
            self.graph.remove_node(node)
            self.daysinfected.update({node:0})
            self.colours.pop(node)
            return(f'{node=} HAS DIED')
    def colour(self):
        '''Here we colour the nodes on whether theyre a hub or a super hub, here hubs are defined as node with a degree > 5 
        super hubs are defined as nodes with the highest degrees in the graph'''
        for key in self.degrees:
            if self.degrees[key] == self.highestdegree:
                self.colours.update({key:'yellow'})
            elif 5 < self.degrees[key] < self.highestdegree :
                self.colours.update({key:'green'})
            else:
                self.colours.update({key:'blue'})

class cgraph:
    '''This is just a copy of the above class to process the orginal graph before the infection '''
    def __init__(self,network):
        self.graph = network 
        self.degrees = dict(nx.degree(network))
        self.colours = []
        self.histogram = dict(enumerate(nx.degree_histogram(network)))
        self.highestdegree = list(self.histogram)[-1]
        self.diameter = nx.diameter(network)
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
    




'''
Our main function takes a number of parameters:
init_graph: This is the graph before using a barabasi-ablert transform to make it scale-free
no_nodes: how many nodes we want the barabasi graph to have
edges: the number of edges to add each barabasi iteration we go through
p_i: probability of infection
p_r: probaility of recovery alternatively 1-p_r is the death rate
enable_vis: takes True or False, this decides if we render the plots of the graphs at the end
'''
def main(init_graph: nx.graph,no_nodes: int, edges: int, p_i: float, p_r: float,enable_vis: bool):
    '''G is our barabsi graph which we build off our init graph'''
    G = nx.barabasi_albert_graph(no_nodes,edges,initial_graph = init_graph)
    cp_G = deepcopy(G) #Makes a copy of G so we can compare later
    
    infection_network = infection_graph(G) #Creates an instance of the infection_graph with G
    origin_network = cgraph(cp_G) #creates a instance of the cgraph class with the copy of G

    days_of_the_infcetion = 0
    '''For all intensive purposes this for loop will run forever until either all the nodes die or the infection dies out'''
    for i in range(100000):
        infect(infection_network,p_i) #We call the infect func on our graph and we will do this many times
        '''Here we look in daysinfected and increment the time a node has been infected by one then see if any node has been
        infected for more than 10 days if so the node will attempt to recover or die'''
        for key in infection_network.daysinfected:
            if key in infection_network.infected:
                infection_network.daysinfected[key] += 1
                if infection_network.daysinfected[key] > 10:
                    
                    infection_network.die_or_recover(key,p_r)

        '''If there is no nodes left infected either everyones dead or everyones recovered'''
        if len(infection_network.infected) == 0:
            '''If theres no nodes left in the graph everyones dead'''
            if len(nx.nodes(infection_network.graph)) == 0:
                no_of_surviors = 0 #Everyones dead, no survivors
                total_death = True
                if enable_vis == 'True':
                    '''We render the plot of the orginal graph to see how it looked and maybe why everyone died,
                    theres no point showing the final graph as itll just be empty'''
                    f = plt.figure('Staring graph')
                    #subax1 = plt.subplot(121)
                    nx.draw(origin_network.graph,node_colours = origin_network.colours,with_labels=True)
                    f.show()
                    input()
            else:
                '''Otherwise if people did survive then we make a list of everyone who survived'''
                surviors = list(nx.nodes(infection_network.graph))
                
                no_of_surviors = len(surviors)
                
                total_death = False
                if enable_vis == 'True':
                    '''Here we render both the orginal grpah and a graph of all the survivors to compare the devasation or lack there of'''
                    f = plt.figure('Starting Graph')
                    nx.draw_networkx(origin_network.graph,node_color = origin_network.colours ,with_labels=True)
                    f.show()
                    g = plt.figure('The Surviors')
                    nx.draw(infection_network.graph,node_color = infection_network.colours.values(),with_labels=True)
                    g.show()
                    input()
            
            '''Returns a lot of useful info about the graph'''
            return {'n':no_nodes,'edges added': edges,'P_i': p_i,'P_r': p_r,'Days_Taken': days_of_the_infcetion, 'Surviors': no_of_surviors,'Everyone_Dead':total_death},repr(origin_network)
                
            
        #Increments the time the infcetions been going on for
        days_of_the_infcetion += 1
        #print(days_of_the_infcetion)
def graphchoice(m):
    '''Here we choose which graph we will be using a barabasi transform on'''
    choice = input('(W)heel, (C)ycle, (K)omplete, (S)tar, (R)andom')      
    match choice:
        case 'W':
            return nx.wheel_graph(m+1)
        case 'C':
            return nx.cycle_graph(m+1)
        case 'K':
            return nx.complete_graph(m+1)
        case 'S':
            return nx.star_graph(m+1)
        case 'R':
            return nx.erdos_renyi_graph(m+1,0.5)
        case _:
            graphchoice()  




if __name__ == '__main__':
    '''Here is where the actual code runs
    We ask the user for input for every parameter of the main function
    '''
        
    n,e,p_i,p_r = input('Number of Nodes:'),input('Barabasi edges to add:'),input('Probaility of infection:'),input('Probability to Recover:')
    graph = graphchoice(e)
    enable_vis = input('Show Graphs?:')
    n,e,p_i,p_r = int(n),int(e),float(p_i),float(p_r)
    tup = main(graph,n,e,p_i,p_r,enable_vis)
    '''Then we print out the results of the infection'''
    infection_data = tup[0]
    origin_graph = tup[1]
    print(infection_data)
    print(origin_graph)
    


















