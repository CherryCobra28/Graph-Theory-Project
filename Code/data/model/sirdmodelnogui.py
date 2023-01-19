'''
This program impletments an algorithm to infect a network, 
selecting one node at random and then at a rate p, will attempt to infect other nodes
 
 
 STRETCH GOALS:
 1. RUN PROGRAM ON RANDOM, WATTZ-STROGATZ, SCALE FREE AND ALBERT-BARABASI (\\)
 2. IMMPLEMENT MULTIPLE SIRD MODELS (\\)
 
 
 
'''

from abc import ABC, abstractmethod
from copy import deepcopy #used to compare the starting graph with the end result
import random as rand #Random helps for random numbers
from math import floor,comb
import networkx as nx #Adds the networkx package, used to create graph objects
import matplotlib.pyplot as plt #A library to plot graphs
from betterdiameter import betterdiameter
import modelexceptions









class infection_graph: 
    '''Creates a clas that we use to control and store information using the graph chosen for infection'''
    def __init__(self,network: nx.Graph, initial_infected: int, intial_immune: int):
        """_summary_

        Args:
            network (nx.Graph): _description_
        """        
        #bepsi
        self.graph = network
        self.vertices = list(nx.nodes(self.graph))
        self.no_nodes = nx.number_of_nodes(self.graph)
        self.edges = len(nx.edges(self.graph))
        self.degrees = dict(nx.degree(self.graph)) #returns a dictionary with the nodes as keys and their degree as value
        self.histogram = dict(enumerate(nx.degree_histogram(self.graph)))#Creates a dictionary where the degree is the key and the frequency of that degree is the value
        self.highestdegree = list(self.histogram)[-1] #Gives the last element of the histogram to give the highest degree
        self.diameter = betterdiameter(self.graph) #Returns the furthest distance between nodes in the graph
        try:
            self.average_path_length = nx.average_shortest_path_length(self.graph)
        except Exception:
            self.average_path_length = 0
            
        ########################################################################
        self.no_of_intitial_infected  = initial_infected
        self.no_of_intitial_immune  = intial_immune

        self.infected = set() #Initalises the empty list
        zeros = [0]*len(self.vertices)
        self.daysinfected = dict(zip(self.vertices,zeros))#Keeps count of how long each node has been infected
        self.timesrecovered = dict(zip(self.vertices,zeros))
        self.no_of_successful_infections = 0
        
        for _ in range(intial_immune):
            self.init_immune()
        
        
        for _ in range(initial_infected):
            self.inital_infection() #Picks a vertex at random to start the infection
        self.PersonalInfection = self.PersonalInfectionRates()
        ########################################################################
        
        self.colours = self.colour() #Initialises the colour dict that we use to colour nodes in the graph
        
        
    def init_immune(self) -> None:
        r_number = rand.randrange(0,len(self.vertices))
        node = self.vertices[r_number]
        if self.timesrecovered[node]>0:
            self.init_immune()
        self.timesrecovered[node] += 1
        
    def inital_infection(self) -> None:
        r_number = rand.randrange(0,len(self.vertices))
        if self.timesrecovered[r_number] > 0:
            self.initial_infection()
        if self.vertices[r_number] in self.infected:
            self.inital_infection()
        self.infected.add(self.vertices[r_number])
        
    def stats(self) -> dict:
        '''returns readable info about the graph, here it gives the: degrees of each node,
        the histogram of the degrees, the highest degree in the graph aka the super hubs and the diameter of the graph'''
        
        return {'highest_degree':self.highestdegree,'Diameter':self.diameter,'average_path_length':self.average_path_length} 
    def inf_stats(self) -> dict:
        return {'intital_number_of_infected': self.no_of_intitial_infected,'intital_number_of_immune': self.no_of_intitial_immune,'Successful_infections': self.no_of_successful_infections}
    def die_or_recover(self,node,r: float) -> None:
        """_summary_

        Args:
            node (_type_): _description_
            r (float): _description_
        """        
        '''This Method runs after a node has been infceted for k days and will attempt to allow the node to recover at p = r
        or die at p = 1-r'''
        r_no = rand.random()
        if r_no < r:
            """if we succeed then the node is removed from the infceted list and the time its spent infected is put back to 0"""
            self.infected.discard(node)
            self.daysinfected.update({node:0})
            self.timesrecovered[node] +=1 
        else:
            '''however if it fails the node is killed, being removed from the infceted list, removed from the graph, has its time infected
            put to 0 and is removed from the colours list to make sure the plot later doesnt attempt to colour a node
            that doesnt exist'''
            self.infected.discard(node)
            self.graph.remove_node(node)
            self.daysinfected.update({node:0})
            self.colours.pop(node)
        
    def colour(self) -> dict:
        '''Here we colour the nodes on whether theyre a hub or a super hub, here hubs are defined as node with a degree greater than the median degree,
        super hubs are defined as nodes with the highest degrees in the graph'''
        colours = dict()
        hubsize = floor(len(self.histogram)/2)
        hub = list(self.histogram)[hubsize]
        for key,val in self.degrees.items():
            if val == self.highestdegree:
                colours.update({key:'yellow'})
            elif hub < val < self.highestdegree :
                colours.update({key:'green'})
            else:
                colours.update({key:'blue'})
        return colours
                
    def PersonalInfectionRates(self) -> dict:
        samples = [rand.random() for _ in range(self.no_nodes)]
        personal_infections = dict(zip(self.vertices,samples))
        return personal_infections

def modifier(x: int) -> int:
    """_summary_

    Args:
        x (int): _description_

    Returns:
        int: _description_
    """    
    mods = list(range(-5,6))
    index = floor(11*x)
    if index == 11:
        index -= 1
    return mods[index]    
    
class infection_strat(ABC):  
    @abstractmethod
    def infect(infclass: infection_graph, p: float) -> None:
        pass
    @abstractmethod
    def __str__():
        pass
    @abstractmethod
    def assumptions():
        pass
class ConstantRateInfection(infection_strat):
    def infect(infclass: infection_graph,p: float) -> None:#function to infect a vertex, p is the probaility of infection use a float 
        """_summary_

        Args:
            infclass (infection_graph): _description_
            p (float): _description_
        """        
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
                infclass.no_of_successful_infections += 1
            else:
                pass
            
    def __str__():
        return 'ConstantRate'
    def assumptions():
        return 'Rate of infection is constant\n'
    
class PersonalInfection(infection_strat):
    def infect(infclass: infection_graph, p: float) -> None:
        """_summary_

        Args:
            infclass (infection_graph): _description_
            p (float): _description_
        """        
        spreaders = []
        for i in infclass.infected: #this part gets all the neighburs of each infected node ready to then attempt to infect them
            k = nx.all_neighbors(infclass.graph, i)
            for n in k:
                spreaders.append(n)
        for node in spreaders:#for each node in the spreaders list the rate of infection is p and will be added  to the infected class
            personal_rate = infclass.PersonalInfection.get(node)
            r_no = rand.random()
            if infclass.timesrecovered[node] > 0:
                pass
            elif r_no < personal_rate:
                infclass.infected.add(node)
            else:
                pass
    def __str__():
        return 'PersonalRate'
    
class SkillCheckInfection(infection_strat):
    def infect(infclass: infection_graph,p:float) -> None:
        """_summary_

        Args:
            infclass (infection_graph): _description_
            p (float): _description_
        """        
        spreaders = []
        for i in infclass.infected: #this part gets all the neighburs of each infected node ready to then attempt to infect them
            k = nx.all_neighbors(infclass.graph, i)
            for n in k:
                spreaders.append(n)
        for node in spreaders:#for each node in the spreaders list the rate of infection is p and will be added  to the infected class
            personal_rate = infclass.PersonalInfection.get(node)

            infection_roll = rand.randint(1,20) + modifier(p) 
            resist_roll = rand.randint(1,20) + modifier(personal_rate)
            success = infection_roll>resist_roll
            
            if infclass.timesrecovered[node] > 0:
                pass
            elif success:
                infclass.infected.add(node)
            else:
                pass
    def __str__():
        return 'SkillCheck'
       
def days_infected_checker(infection: infection_graph,p_r: float, fatal_days: int = 10 ) -> None:
    """_summary_

    Args:
        infection (infection_graph): _description_
        p_r (float): _description_
        fatal_days (int, optional): _description_. Defaults to 10.
    """    
    for node in infection.daysinfected:
            if node in infection.infected:
                infection.daysinfected[node] += 1
            if infection.daysinfected[node] > fatal_days:
                infection.die_or_recover(node,p_r)
    
def model(graph: nx.Graph,p_i: float, p_r: float,intial_infected: int = 1,intial_immune: int = 0,enable_vis: bool = False,infection_type: infection_strat = ConstantRateInfection,graph_type: str = 'Not Defined') -> tuple[dict,dict]:
    """Takes our input graph, plus the infection parameters to yield a tuple contain the information of the infection.

    Args:
        graph (nx.Graph): The graph that our model will be ran on.
        p_i (float): The infection rate of the virus.
        p_r (float): The recovery rate of the infcected
        enable_vis (bool, optional): Turns on or off the graph visuals. Defaults to False.
        infection_type (infection_strat, optional): Decides how the virus will behave. Defaults to ConstantRateInfection.
        graph_type (str, optional): What type of graph we are running on. Defaults to 'Not Defined'.

    Raises:
        modelexceptions.ModelError: If the model fails to run we raise a model error
    Returns:
        tuple[dict,dict]: The first dictionary represents the data from the infection and the second dictionary constains data about the graph that the model is running on
    """    
    infection_network = infection_graph(deepcopy(graph),initial_infected=intial_infected,intial_immune = intial_immune) #Creates an instance of the infection_graph witnode
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
                no_of_survivors = 0 #Everyones dead, no survivors
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
                survivors = list(nx.nodes(infection_network.graph))
                
                no_of_survivors = len(survivors)
                
                total_death = False
                if enable_vis is True:
                    '''Here we render both the orginal grpah and a graph of all the survivors to compare the devasation or lack there of'''
                    f = plt.figure('Starting Graph')
                    nx.draw_networkx(origin_network.graph,node_color = origin_network.colours.values() ,with_labels=True)
                    f.show()
                    g = plt.figure('The survivors')
                    nx.draw(infection_network.graph,node_color = infection_network.colours.values(),with_labels=True)
                    g.show()
                    input()
            
            '''Returns a lot of useful info about the graph'''
            #no_of_recovered = [val for _, val in infection_network.timesrecovered.items() if val >0]
            #print(no_of_recovered)
            infection_info = {'n':origin_network.no_nodes,'e': origin_network.edges,'P_i': p_i,'P_r': p_r,'Days_Taken': days_of_the_infcetion, 'survivors': no_of_survivors,'Everyone_Dead':total_death,'Infection_Type': infection_type.__str__(),'Graph_Type':graph_type} | infection_network.inf_stats()
            return infection_info,origin_network.stats()     
        #Increments the time the infcetions been going on for
        days_of_the_infcetion += 1
    else:
        raise modelexceptions.ModelError
    
def main():
    #infection_data,origin_graph = model(*userpanel())
    infection_data,origin_graph = model(nx.barabasi_albert_graph(20,5),0.8,0.9)
    print(infection_data)
    print(origin_graph)

if __name__ == '__main__':
    main()
   
    

















