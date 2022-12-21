'''
This program impletments an algorithm to infect a network, 
selecting one node at random and then at a rate p, will attempt to infect other nodes
 
 
 STRETCH GOALS:
 1. RUN PROGRAM ON RANDOM, WATTZ-STROGATZ, SCALE FREE AND ALBERT-BARABASI
 2. IMMPLEMENT MULTIPLE SIRD MODELS
 
 
 
'''

from abc import ABC, abstractmethod
from copy import deepcopy
 #used to compare the starting graph with the end result
import random as rand #Random helps for random numbers
from math import floor,comb
import networkx as nx #Adds the networkx package, used to create graph objects
import matplotlib.pyplot as plt #A library to plot graphs
import PySimpleGUI as sg
from betterdiameter import betterdiameter


class graph_constructer:
    def barabasi(init_graph: nx.Graph, no_nodes: int, edges: int) -> nx.Graph:
        try:
            return nx.barabasi_albert_graph(no_nodes,edges,initial_graph = init_graph)
        except nx.exception.NetworkXError:
            print(f'Number of edges must be less that number of nodes, {edges}>{no_nodes}')
            userpanel()
        
    def random_graph(no_nodes: int, Eedges: int) -> nx.Graph:
        p = Eedges/comb(no_nodes,2)
        try:
            return nx.erdos_renyi_graph(no_nodes,p)
        except nx.exception.NetworkXErrror:
            userpanel()
    def watts(n:int, k:int,p: float)-> nx.Graph:
        try:
            return nx.watts_strogatz_graph(n,k,p)
        except nx.exception.NetworkXErrror:
            userpanel()
        
    def scale_free(n,a,b,c) -> nx.Graph:
        try:
            nx.scale_free_graph(n,a,b,c)
        except nx.exception.NetworkXErrror:
            userpanel()



class infection_graph: 
    '''Creates a clas that we use to control and store information using the graph chosen for infection'''
    def __init__(self,network):
        #bepsi
        self.graph = network
        self.graph_prop()
        self.infection_props()
        self.colours = dict() #Initialises the colour dict that we use to colour nodes in the graph
        self.colour() #Colours the node
        
    def graph_prop(self) -> None:
        self.vertices = list(nx.nodes(self.graph))
        self.no_nodes = nx.number_of_nodes(self.graph)
        self.degrees = dict(nx.degree(self.graph)) #returns a dictionary with the nodes as keys and their degree as value
        self.histogram = dict(enumerate(nx.degree_histogram(self.graph)))#Creates a dictionary where the degree is the key and the frequency of that degree is the value
        self.highestdegree = list(self.histogram)[-1] #Gives the last element of the histogram to give the highest degree
        self.diameter = betterdiameter(self.graph) #Returns the furthest distance between nodes in the graph
        try:
            self.average_path_length = nx.average_shortest_path_length(self.graph)
        except Exception:
            self.average_path_length = 0

    def infection_props(self) -> None:
        self.infected = set() #Initalises the empty list
        zeros = [0]*len(self.vertices)
        r_number = rand.randrange(0,len(self.vertices))
        self.infected.add(self.vertices[r_number]) #Picks a vertex at random to start the infection
        self.daysinfected = dict(zip(self.vertices,zeros))#Keeps count of how long each node has been infected
        self.timesrecovered = dict(zip(self.vertices,zeros))

    def stats(self) -> dict:
        '''returns readable info about the graph, here it gives the: degrees of each node,
        the histogram of the degrees, the highest degree in the graph aka the super hubs and the diameter of the graph'''
        
        return {'histogram':self.histogram, 'highest_degree':self.highestdegree,'Diameter':self.diameter,'average_path_length':self.average_path_length} 
    def die_or_recover(self,node,r: float) -> str:
        '''This Method runs after a node has been infceted for k days and will attempt to allow the node to recover at p = r
        or die at p = 1-r'''
        r_no = rand.random()
        if r_no < r:
            """if we succeed then the node is removed from the infceted list and the time its spent infected is put back to 0"""
            self.infected.discard(node)
            self.daysinfected.update({node:0})
            self.timesrecovered[node] +=1 
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
        
    def colour(self) -> None:
        '''Here we colour the nodes on whether theyre a hub or a super hub, here hubs are defined as node with a degree greater than the median degree,
        super hubs are defined as nodes with the highest degrees in the graph'''
        hubsize = floor(len(self.histogram)/2)
        hub = list(self.histogram)[hubsize]
        for key in self.degrees:
            if self.degrees[key] == self.highestdegree:
                self.colours.update({key:'yellow'})
            elif hub < self.degrees[key] < self.highestdegree :
                self.colours.update({key:'green'})
            else:
                self.colours.update({key:'blue'})
                
    def PersonalInfectionRates(self) -> dict:
        pass
    
    


    
    
    
class infection_strat(ABC):
    @abstractmethod
    def infect(infclass: infection_graph, p: float) -> None:
        pass
class ConstantRateInfection(infection_strat):
    def infect(infclass: infection_graph,p: float) -> None:#function to infect a vertex, p is the probaility of infection use a float 
        spreaders = []
        for i in infclass.infected: #this part gets all the neighburs of each infected node ready to then attempt to infect them
            k = nx.all_neighbors(infclass.graph, i)
            for n in k:
                spreaders.append(n)
        for node in spreaders:#for each node in the spreaders list the rate of infection is p and will be added  to the infected class
            r_no = rand.random()
            if infclass.timesrecovered[node] > 0:
                pass
            elif r_no < p:
                infclass.infected.add(node)
            else:
                pass
class PersonalInfection(infection_strat):
    def infect(infclass: infection_graph) -> None:
        pass
class SkillCheckInfection(infection_strat):
    def infect(infclass: infection_graph,p:float) -> None:
        pass
       
def days_infected_checker(infection: infection_graph,p_r: float, fatal_days: int = 10 ) -> None:
    for node in infection.daysinfected:
            if node in infection.infected:
                infection.daysinfected[node] += 1
                if infection.daysinfected[node] > fatal_days:
                    
                    infection.die_or_recover(node,p_r)
    
def main(graph: nx.Graph,p_i: float, p_r: float,enable_vis: bool = False,infection_type: infection_strat = ConstantRateInfection) -> tuple:
    """Takes our input graph, plus the infection parameters to yield a tuple contain the information of the infection.

    Parameters
    ----------
    graph : NetworkX graph
        The graph that our model will be ran on.

    p_i : float
        The infection rate of the virus.
    p_r : float
        The recovery rate of the infcected
    enable_vis : bool
        Turns on or off the graph visuals
        Default to False
    infection_type : infection_strat
        Decides how the virus will behave

    Returns
    -------
    data : tuple
        data frm the infection and the graphs supplied
    """
    infection_network = infection_graph(graph) #Creates an instance of the infection_graph witnode
    origin_network = deepcopy(infection_network) #Makes a copy of G so we can compare later
    days_of_the_infcetion = 0
    '''For all intensive purposes this for loop will run forever until either all the nodes die or the infection dies out'''
    for _ in range(100000):
        infection_type.infect(infection_network,p_i) #We call the infect func on our graph and we will do this many times
        '''Here we look in daysinfected and increment the time a node has been infected by one then see if any node has been
        infected for more than 10 days if so the node will attempt to recover or die'''
        days_infected_checker(infection_network,p_r)
        '''If there is no nodes left infected either everyones dead or everyones recovered'''
        if len(infection_network.infected) == 0:
            '''If theres no nodes left in the graph everyones dead'''
            if len(nx.nodes(infection_network.graph)) == 0:
                no_of_surviors = 0 #Everyones dead, no survivors
                total_death = True
                if enable_vis is True:
                    '''We render the plot of the orginal graph to see how it looked and maybe why everyone died,
                    theres no point showing the final graph as itll just be empty'''
                    f = plt.figure('Staring graph')
                    #subax1 = plt.subplot(121)
                    nx.draw(origin_network.graph,node_color = origin_network.colours.values(),with_labels=True)
                    f.show()
                    input()
            else:
                '''Otherwise if people did survive then we make a list of everyone who survived'''
                surviors = list(nx.nodes(infection_network.graph))
                
                no_of_surviors = len(surviors)
                
                total_death = False
                if enable_vis is True:
                    '''Here we render both the orginal grpah and a graph of all the survivors to compare the devasation or lack there of'''
                    f = plt.figure('Starting Graph')
                    nx.draw_networkx(origin_network.graph,node_color = origin_network.colours.values() ,with_labels=True)
                    f.show()
                    g = plt.figure('The Surviors')
                    nx.draw(infection_network.graph,node_color = infection_network.colours.values(),with_labels=True)
                    g.show()
                    input()
            
            '''Returns a lot of useful info about the graph'''
            infection_info = {'n':origin_network.no_nodes,'P_i': p_i,'P_r': p_r,'Days_Taken': days_of_the_infcetion, 'Surviors': no_of_surviors,'Everyone_Dead':total_death}
            return infection_info,origin_network.stats()     
        #Increments the time the infcetions been going on for
        days_of_the_infcetion += 1

def graphchoice(m,choice) -> nx.Graph:
    '''Here we choose which graph we will be using a barabasi transform on'''   

    if choice == 'Wheel':
        return nx.wheel_graph(m+1)
    elif choice == 'Cycle' :
        return nx.cycle_graph(m+1)
    elif choice == 'Complete':
        return nx.complete_graph(m+1)
    elif choice == 'Star':
        return nx.star_graph(m+1)
    elif choice == 'Erdos-Renyi':
        return nx.erdos_renyi_graph(m+1,0.5)
        
def userpanel() -> nx.Graph:
    '''Here is where the actual code runs, We ask the user for input for every parameter of the main function'''
    sg.theme('Green')
    list_of_graph_types = ['Barabasi-Albert','Watts-Strogats','Erdos Random','Scale Free']
    layout = [[sg.Text('Which type of graph would you like to test?')],
              [sg.Listbox(values=list_of_graph_types, key='-LIST-', enable_events=True)],
              [sg.Submit()],
              [sg.Cancel()]
              ]
    window = sg.Window('SIRD Infection Model', layout)
    while True:

            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Exit'):
                quit()
            elif 'Submit' in event:
                break
    window.close()
    try:
        graph_type = values['-LIST-'][0]
    except IndexError:
        userpanel()
    
    if graph_type == 'Barabasi-Albert':
        sg.theme('Green')
        list_of_graphs = ['Wheel','Cycle','Complete','Star','Erdos-Renyi']   
        layout = [[sg.Text('No of nodes')],
                  [sg.InputText()],
                  [sg.Text('Barabasi Edges')],
                  [sg.InputText()],
                  [sg.Text('P of infection')],
                  [sg.InputText()],
                  [sg.Text('P of Recovery')],
                  [sg.InputText()],
                  [sg.Text('Choice of seed graph:')],
                  [sg.Listbox(values=list_of_graphs,size=(15,5), key='-LIST-', enable_events=True)],
                  [sg.Checkbox('Enable Graphs?',default = True, key= '-IN-' )],
                  [sg.Submit()],
                  [sg.Cancel()]]


        window = sg.Window('SIRD Infection Model', layout)
        while True:

            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Exit'):
                quit()
            elif 'Submit' in event:
                break
            
            
        window.close()
        if values['-IN-'] is  True:
            enable_vis = True
        else:
            enable_vis = False
        try:
            n,e,p_i,p_r = values[0],values[1],values[2],values[3]
            n,e,p_i,p_r = int(n),int(e),float(p_i),float(p_r)
        except ValueError:
            print('Please input the correct data types')
            userpanel()
     #n,e,p_i,p_r = input('Number of Nodes:'),input('Barabasi edges to add:'),input('Probaility of infection:'),input('Probability to Recover:')
     #enable_vis = input('Show Graphs?:')
        graph = graphchoice(e,values['-LIST-'][0])
        user_graph = graph_constructer.barabasi(graph,n,e)
        
   

    elif graph_type == 'Watts-Strogats':
        pass
    elif graph_type == 'Erdos Random':
        pass
    elif graph_type == 'Scale Free':
        pass  
    infection_data,origin_graph = main(user_graph,p_i,p_r,enable_vis)
    print(infection_data)
    print(origin_graph)
   





if __name__ == '__main__':
    userpanel()
   
    


















