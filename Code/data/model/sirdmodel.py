'''
This program impletments an algorithm to infect a network, 
selecting one node at random and then at a rate p, will attempt to infect other nodes
 
 
 STRETCH GOALS:
 1. RUN PROGRAM ON RANDOM, WATTZ-STROGATZ, SCALE FREE AND ALBERT-BARABASI (\)
 2. IMMPLEMENT MULTIPLE SIRD MODELS (\)
 
 
 
'''

from abc import ABC, abstractmethod
from copy import deepcopy #used to compare the starting graph with the end result
import random as rand #Random helps for random numbers
from math import floor,comb
import logging
import networkx as nx #Adds the networkx package, used to create graph objects
import matplotlib.pyplot as plt #A library to plot graphs
from betterdiameter import betterdiameter
try:
    import PySimpleGUI as sg
    NOGUI = False
except ImportError:
    print('PySimpleGUI is not available, please try installing PySimpleGUI')
    NOGUI = True
    sg = None
logging.basicConfig(level=logging.WARNING)

class infection_graph: 
    """The infect graph class is the object that we will be using for a majority of the programs run time, it creates an object that holds data about the on goign infection
    """    
    def __init__(self,network: nx.Graph, initial_infected: int, intial_immune: int,enable_vis: bool):
        """__init__() is run when the object is first created, here we intialise all the values ou program will require

        Args:
            network (nx.Graph): This is the network the infection will be ran on
            initial_infected (int): This determines how many people will be infected on day 0 of the infection
            intial_immune (int): This determines how many people will be natrually immune to the infection from day 0
        """        
        self.graph = network #This is the network the infection is running on
        self.vertices = list(nx.nodes(self.graph)) #this is a list of all the vertices in the network
        self.no_nodes = nx.number_of_nodes(self.graph)#the total number of nodes in the network
        self.edges = nx.number_of_edges(self.graph)#the number of edges in the network
        self.degrees = dict(nx.degree(self.graph)) #returns a dictionary with the nodes as keys and their degree as value
        self.histogram = dict(enumerate(nx.degree_histogram(self.graph)))#Creates a dictionary where the degree is the key and the frequency of that degree is the value
        self.highestdegree = list(self.histogram)[-1] #Gives the last element of the histogram to give the highest degree
        self.average_degree = sum([key*val for key, val in self.histogram.items()])/self.no_nodes #we take all the values from the histogram dictionary, multiply the frequency by the degree then take the mean of that
        if self.no_nodes >= 3000: #If the number of nodes is greater than 2000, claulating the diameter and cluerting coeffcitn is quit slow so we use an aprroximation instead
            try:
                self.diameter = nx.approximation.diameter(self.graph) #This uses a 2 pass algorithm, it randomly selcts tow nodes from the graph and claulates the diameter between them, then does this again and which ever is higher is selcted as the diameter. This will be a lower bound for the diameter
            except Exception:
                self.diameter = 10**6 #This is just a large number for if it is not connceted, putting infinity here would stop us anaylsing the data as easy
            self.clustering = nx.approximation.average_clustering(self.graph)#This approx imation works by slecting a node at random and seeing if two of its neighbours are connected to each other, it repeats that 1000 times then retunrs the fraction of trianles found
            self.average_path_length = 0.5 * self.diameter
        else:
            self.diameter = betterdiameter(self.graph) #See betterdiameter documentation
            self.clustering = nx.average_clustering(self.graph)#returns the average clustering coeffcient by calculating the local clustering coefficent for each node
            try:
                self.average_path_length = nx.average_shortest_path_length(self.graph) #This calulates the average shortest path length for the graph, if the graph is discconncted this will raise and exception
            except Exception: #Incase of that exception we set the average shortest path length to 0
                self.average_path_length = 0
        if enable_vis:
            self.pos = nx.spring_layout(self.graph)# This sets a standard layout for when we output images of the graph
        ########################################################################
        self.no_of_intitial_infected  = initial_infected
        self.no_of_intitial_immune  = intial_immune
        self.infected = set() #We store each infected node here. We intialize self.infected as a set as in python a set can only have unique values so if node 3 was added twice then only one would be saved
        zeros = [0]*self.no_nodes #a list of 0s for each node in the graph
        self.daysinfected = dict(zip(self.vertices,zeros))#A dictionary mapping each node to how long they have been infected
        self.timesrecovered = dict(zip(self.vertices,zeros))#A dictionary mapping each node to the number of times they recoverd (Currenly if the times recoverd is greater than 0 then the node is immune)
        self.no_of_successful_infections = self.no_of_intitial_infected #the number of times the infection has infected another node
        #######################################################################
        for _ in range(intial_immune): #adds immune people equal to init_immune parameter
            self.init_immune()
        for _ in range(initial_infected):
            self.inital_infection() #Picks a vertex at random to start the infection
        self.PersonalInfection = self.PersonalInfectionRates() #Creates a personal infection rate for each node (only used for the PersonalInfection and SkillCheck infection strategies)
        ########################################################################
        self.colours = self.colour() #Initialises the colour dict that we use to colour nodes in the graph
             
    def init_immune(self) -> None:
        """Makes nodes immune from day 0
        """        
        r_number = rand.randrange(0,self.no_nodes) #Pick a random integer between 0 and self.no nodes
        node = self.vertices[r_number]#using that random integer it selects the node from the graph
        if self.timesrecovered[node]>0: #if the node is already immune it runs the function gain to pick a different node
            self.init_immune()
        self.timesrecovered[node] += 1 #Adds 1 to the timesrecoverd dictionary to make the node immune
        
    def inital_infection(self) -> None:
        """Infects the intial nodes at day 0
        """        
        r_number = rand.randrange(0,self.no_nodes)
        if self.timesrecovered[r_number] > 0: #If the node is already immune it cant infect the node
            self.initial_infection()
        if self.vertices[r_number] in self.infected: #if the node is already infected it selects another node
            self.inital_infection()
        self.infected.add(self.vertices[r_number]) #adds the node to self.infcected
        
    def stats(self) -> dict:
        """This function gives information about the garphs structure

        Returns:
            dict: Contains the highest degree, diameter, average path length, avergae clustering, and the average degree
        """        
        return {'highest_degree':self.highestdegree,
                'Diameter':self.diameter,
                'average_path_length':self.average_path_length,
                'average_clustering': self.clustering,
                'average_degree':self.average_degree} 
    def inf_stats(self) -> dict:
        """This function returns information about the infection

        Returns:
            dict: Contains the number of intial infected, intial immune and the number of successful infections
        """        
        return {'intital_number_of_infected': self.no_of_intitial_infected,
                'intital_number_of_immune': self.no_of_intitial_immune,
                'Successful_infections': self.no_of_successful_infections}
    
    def die_or_recover(self,node,r: float) -> None:
        """This function handles nodes either dying or recovering depending on our model parameters
        They recover with probability r and die with probability 1-r

        Args:
            node (node): The node that is going to recover or die
            r (float): The recovery rate as set by the model
        """        
        r_no = rand.random() #chooses a random float from 0 to 1
        if r_no < r:
            """if the node recovers, it is removed from the infected set, has its time spent infected set to 0 and has its times recovered increased to 1 (making the node immune)"""
            self.infected.discard(node)
            self.daysinfected.update({node:0})
            self.timesrecovered[node] +=1 
            logging.debug(f"{node} has recovered")
        else:
            '''however if it fails the node is killed, being removed from the infected set, removed from the graph, has its time infected
            put to 0 and is removed from the colours list to make sure the plot later doesnt attempt to colour a node
            that doesnt exist'''
            self.infected.discard(node)
            self.graph.remove_node(node)
            self.daysinfected.update({node:0})
            self.colours.pop(node)
            logging.debug(f"{node} has died")
        
    def colour(self) -> dict:
        '''Here we colour the nodes on whether theyre a hub or a super hub, here hubs are defined as node with a degree greater than the median degree,
        super hubs are defined as nodes with the highest degrees in the graph
        
        Returns:
            dict: Conatins each node and its corresponding colour
        '''
        colours = dict()
        hubsize = floor(len(self.histogram)/2) #The median degree of the graph
        hub = list(self.histogram)[hubsize] #uses the median to grab the hub nodes 
        for key,val in self.degrees.items():
            if val == self.highestdegree: #if the node is a super hub its coloured yellow
                colours.update({key:'yellow'})
            elif hub < val < self.highestdegree : #if the node has degree is greater thena hub and less than the highest degree then its coloured green
                colours.update({key:'green'})
            else:
                colours.update({key:'blue'})
        return colours 
                
    def PersonalInfectionRates(self) -> dict:
        """Creates all the personal infection rates for the nodes

        Returns:
            dict: Contains each node and its personal infection rate pulled from a uniform  distribution
        """        
        samples = [rand.random() for _ in range(self.no_nodes)]
        personal_infections = dict(zip(self.vertices,samples))
        return personal_infections

def modifier(x: float) -> int:
    """Used for the skill check infection strategy

    Args:
        x (float): The infection rate

    Returns:
        int: An integer from -5 to +5
    """    
    mods = list(range(-5,6))
    index = floor(11*x)
    if index == 11:
        index -= 1
    return mods[index]    
    
class infection_strat(ABC): 
    """This is an abstract base class for the infection strategies, it sets the blueprint for what the infection strategies should look like
    They should have:
        An Infection method
        A __str__ method for a string representation of the strat
        An assumptions dunction that returns the assumptions the infection strategy makes
    """     
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
    """This is the main infection strategy basiing off a constant rate to infect each node
    """    
    def infect(infclass: infection_graph,p: float) -> None:
        """This method infects usinga constant rate to infect each node

        Args:
            infclass (infection_graph): The graph we are using in the model
            p (float): The constant rate of infection
        """        
        to_be_infected = []
        for i in infclass.infected: #this part gets all the neighburs of each infected node ready to then attempt to infect them
            k = nx.all_neighbors(infclass.graph, i)
            for n in k:
                to_be_infected.append(n)
        to_be_infected = [x for x in  to_be_infected if x not in infclass.infected] #We filter out any nodes that are already infected
        for node in to_be_infected:#for each node in the   to_be_infected list the rate of infection is p and will be added  to the infected class
            r_no = rand.random() #A random float from 0 to 1
            if infclass.timesrecovered[node] > 0: #if infclass.timesrecovered[node] is greater than 0 the node is immune so we ignore it
                pass
            elif node in infclass.infected:
                pass
            elif r_no < p: #if the R-no is less than p the node becomes infected 
                infclass.infected.add(node) #it is added to the infected set
                infclass.no_of_successful_infections += 1 #we have successfully infected so we add 1 to the number of successful infections
                logging.debug(f"{node} was infected")
            else: #If the node isnt infected we ignore it
                pass
            
    def __str__() -> str:
        """Returns a string representation of the strategy"""
        return 'ConstantRate'
    
    def assumptions() -> list[str]:
        """Returns a list of assumptions about the strat"""
        return ['Rate of infection is constant\n']
    
    
"""Do the other strategies later"""    
class PersonalInfection(infection_strat):
    """In this strategy everyone has a personal infection rate, so we are techinally agnostic on how he infecctionous of the virus
    """    
    def infect(infclass: infection_graph, p: float) -> None:   
        to_be_infected = []
        for i in infclass.infected: #this part gets all the neighburs of each infected node ready to then attempt to infect them
            k = nx.all_neighbors(infclass.graph, i)
            for n in k:
                to_be_infected.append(n)
        for node in to_be_infected:#for each node in the   to_be_infected list the rate of infection is p and will be added  to the infected class
            personal_rate = infclass.PersonalInfection.get(node)
            r_no = rand.random()
            if infclass.timesrecovered[node] > 0:
                pass
            elif node in infclass.infected:
                pass
            elif r_no < personal_rate:
                infclass.infected.add(node)
                infclass.no_of_successful_infections += 1
                logging.debug(f"{node} was infected")
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
        to_be_infected = []
        for i in infclass.infected: #this part gets all the neighburs of each infected node ready to then attempt to infect them
            k = nx.all_neighbors(infclass.graph, i)
            for n in k:
                to_be_infected.append(n)
        for node in to_be_infected:#for each node in the   to_be_infected list the rate of infection is p and will be added  to the infected class
            personal_rate = infclass.PersonalInfection.get(node)

            infection_roll = rand.randint(1,20) + modifier(p) 
            resist_roll = rand.randint(1,20) + modifier(personal_rate)
            success = infection_roll>resist_roll
            
            if infclass.timesrecovered[node] > 0:
                pass
            elif node in infclass.infected:
                pass
            elif success:
                infclass.infected.add(node)
                infclass.no_of_successful_infections += 1
                logging.debug(f"{node} was infected")
            else:
                pass
            
    def __str__():
        return 'SkillCheck'
       
def days_infected_checker(infection: infection_graph,p_r: float, fatal_days: int = 10 ) -> None:
    """This function checks how long the node has been infected for so the node can either die or recover

    Args:
        infection (infection_graph): The graph were studying
        p_r (float): The reocvery rate from the model
        fatal_days (int, optional): The number of days it takes for the virus to either kill someone or recover. Defaults to 10.
    """    
    for node in infection.daysinfected: 
            if node in infection.infected: #if its infected add 1 to its days infected
                infection.daysinfected[node] += 1
            if infection.daysinfected[node] > fatal_days: #if the daysinfected is greater than fatal days then it will either die or recover
                infection.die_or_recover(node,p_r)
    
def model(graph: nx.Graph,p_i: float, p_r: float,intial_infected: int = 1,intial_immune: int = 0,enable_vis: bool = False,infection_type: infection_strat = ConstantRateInfection,graph_type: str = 'Not Defined') -> tuple[dict,dict]:
    """The main SIRD model

    Args:
        graph (nx.Graph): The input graph which the model will run on
        p_i (float): Probaility of infection
        p_r (float): Probability of recovery
        intial_infected (int, optional): Number of intial infected people. Defaults to 1.
        intial_immune (int, optional): Number of intially immune people. Defaults to 0.
        enable_vis (bool, optional): Decides wether to show a visualisation of the graph. Defaults to False.
        infection_type (infection_strat, optional): The infection strategy. Defaults to ConstantRateInfection.
        graph_type (str, optional): The type of graph were using. Defaults to 'Not Defined'.

    Raises:
        Exception: If the model is not running correctly. we will raise an error

    Returns:
        tuple[dict,dict]: The tuple contains information about the graph, the infection parameters and data from the model
    """    
    infection_network = infection_graph(deepcopy(graph),initial_infected=intial_infected,intial_immune = intial_immune,enable_vis=enable_vis) #Creates an instance of the infection_graph
    origin_network = deepcopy(infection_network) #Makes a copy of G so we can compare later
    days_of_the_infcetion = 0
    '''For all intensive purposes this for loop will run forever until either all the nodes die or the infection dies out'''
    for _ in range(100000):
        infection_type.infect(infection_network,p_i) #We call the infect func on our graph and we will do this many times
        '''Here we look in daysinfected and increment the time a node has been infected by one then see if any node has been
        infected for more than 10 days if so the node will attempt to recover or die'''
        days_infected_checker(infection_network,p_r,10)
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
                no_of_survivors = len(nx.nodes(infection_network.graph))
                total_death = False
                if enable_vis is True:
                    '''Here we render both the orginal grpah and a graph of all the survivors to compare the devasation or lack there of'''
                    f = plt.figure('Starting Graph')
                    nx.draw_networkx(origin_network.graph,node_color = origin_network.colours.values() ,pos=origin_network.pos,with_labels=True)
                    f.show()
                    g = plt.figure('The survivors')
                    nx.draw(infection_network.graph,node_color = infection_network.colours.values(),pos=infection_network.pos,with_labels=True)
                    g.show()
                    input()
            
            '''Returns a lot of useful info about the graph'''
            infection_info = {'n':origin_network.no_nodes,
                              'e': origin_network.edges,
                              'P_i': p_i,
                              'P_r': p_r,
                              'Days_Taken': days_of_the_infcetion,
                              'survivors': no_of_survivors,
                              'Everyone_Dead':total_death,
                              'Infection_Type': infection_type.__str__(),
                              'Graph_Type':graph_type} | infection_network.inf_stats()
            return infection_info,origin_network.stats()     
        #Increments the time the infcetions been going on for
        days_of_the_infcetion += 1
    else:
        err = "The model failed to complete for unforseen reasons"
        raise Exception(err)

##GUI##
#############################################################################
class graph_constructer:
    """_summary_
    """    
    def barabasi(init_graph: nx.Graph, no_nodes: int, edges: int) -> nx.Graph:
        """_summary_

        Args:
            init_graph (nx.Graph): _description_
            no_nodes (int): _description_
            edges (int): _description_

        Returns:
            nx.Graph: _description_
        """        
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
        
    def scale_free(n: int,a: float,b: float,c: float) -> nx.Graph:
        try:
            nx.scale_free_graph(n,a,b,c)
        except nx.exception.NetworkXErrror:
            userpanel()

def graphchoice(m:int,choice: str) -> nx.Graph:
    """_summary_

    Args:
        m (int): _description_
        choice (str): _description_

    Returns:
        nx.Graph: _description_
    """    
    
    
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

class Panel:
    """_summary_

    Returns:
        _type_: _description_
    """    
    def __init__(self):
        self.LIST_OF_INFECTION_MODELS = {'ConstantRate':ConstantRateInfection,'Personal':PersonalInfection,'SkillCheck':SkillCheckInfection}
        
    def barabasi(self) -> tuple:
        """_summary_

        Returns:
            tuple: _description_
        """        
        graph_type = 'Barabasi'
        sg.theme('Green')
        LIST_OF_GRAPHS = ('Wheel','Cycle','Complete','Star','Erdos-Renyi')
        layout = [[sg.Text('No of nodes')],
                  [sg.InputText()],
                  [sg.Text('Barabasi Edges')],
                  [sg.InputText()],
                  [sg.Text('Choice of seed graph:')],
                  [sg.Listbox(values=LIST_OF_GRAPHS,size=(15,5), key='Graph_Type', enable_events=True)],
                  [sg.Checkbox('Enable Graphs?',default = True, key= 'Enable_Vis' )],
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
        if values['Enable_Vis'] is  True:
            enable_vis = True
        else:
            enable_vis = False
        try:
            n,e= values[0],values[1]
            n,e= int(n),int(e)
        except ValueError:
            print('Please input the correct data types')
            self.barabasi()
         #n,e,p_i,p_r = input('Number of Nodes:'),input('Barabasi edges to add:'),input('Probaility of infection:'),input('Probability to Recover:')
         #enable_vis = input('Show Graphs?:')
        graph = graphchoice(e,values['Graph_Type'][0])
        user_graph = graph_constructer.barabasi(graph,n,e)
        return (user_graph,enable_vis,graph_type)

    def watts_strogatz(self) -> tuple:
        graph_type = 'Watts-Strogatz'
        sg.theme('Green')
        layout = [[sg.Text('No of nodes')],
                  [sg.InputText()],
                  [sg.Text('k:')],
                  [sg.InputText()],
                  [sg.Text('p:')],
                  [sg.InputText()],
                  [sg.Checkbox('Enable Graphs?',default = True, key= 'Enable_Vis' )],
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
        if values['Enable_Vis'] is  True:
            enable_vis = True
        else:
            enable_vis = False
        try:
            n,k,p = values[0],values[1],values[2]
            n,k,p = int(n),int(k),float(p)
        except ValueError:
            print('Please input the correct data types')
            self.watts_strogatz()

        user_graph = graph_constructer.watts(n,k,p)
        return (user_graph,enable_vis,graph_type)

    def scale_free(self):
        graph_type = 'Scale-Free'
        sg.theme('Green')
        layout = [[sg.Text('No of nodes (int)')],
                  [sg.InputText()],
                  [sg.Text('alpha (float)')]
                  [sg.InputText()],
                  [sg.Text('beta (float)')],
                  [sg.InputText()],
                  [sg.Text('gamma (float)')],
                  [sg.InputText()],
                  [sg.Checkbox('Enable Graphs?',default = True, key= 'Enable_Vis' )],
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
        if values['Enable_Vis'] is  True:
            enable_vis = True
        else:
            enable_vis = False
        try:
            n,a,b,c = values[0],values[1],values[2],values[3]
            n,a,b,c = int(n),float(a),float(b),float(c)
        except ValueError:
            print('Please input the correct data types')
            self.scale_free()
        user_graph = graph_constructer.scale_free(n,a,b,c,graph_type)
        return (user_graph,enable_vis)
    
    def erdos_renyi(self):
        graph_type = 'Erdos-Renyi'
        sg.theme('Green')
        layout = [[sg.Text('No of nodes (int)')],
                  [sg.InputText()],
                  [sg.Text('Expected No of edges')]
                  [sg.InputText()],
                  [sg.Checkbox('Enable Graphs?',default = True, key= 'Enable_Vis' )],
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
        if values['Enable_Vis'] is  True:
            enable_vis = True
        else:
            enable_vis = False
        try:
            n,e = values[0],values[1]
            n,e= int(n),float(e)
        except ValueError:
            print('Please input the correct data types')
            self.erdos_renyi()
        user_graph = graph_constructer.random_graph(n,e)
        return (user_graph,enable_vis,graph_type)
    
    def infect_panel(self):
        sg.theme('Green')
        layout = [[sg.Text('P of infection')],
                  [sg.InputText()],
                  [sg.Text('P of Recovery')],
                  [sg.InputText()],
                  [sg.Text('Number of Intial Infected')],
                  [sg.InputText()],
                  [sg.Text('Number of Intial Immune')],
                  [sg.InputText()],
                  [sg.Listbox(values=list(self.LIST_OF_INFECTION_MODELS.keys()),size=(15,5),key='Infection',enable_events=True)],
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
        try:
            p_i,p_r,init_infected,init_immune = float(values[0]),float(values[1]),int(values[2]),int(values[3])
        except ValueError:
            print('Pleaae use the coreect data types')
            self.infect_panel()
        infection_type_key = values['Infection'][0]
        infection_type = self.LIST_OF_INFECTION_MODELS[infection_type_key]
        return (p_i,p_r,init_infected,init_immune,infection_type)
    
def userpanel() -> tuple:
    """_summary_

    Returns:
        tuple: _description_
    """    
    sg.theme('Green')
    panel = Panel()
    LIST_OF_GRAPH_TYPES = {'Barabasi-Albert':panel.barabasi,'Watts-Strogats':panel.watts_strogatz,'Erdos Random':panel.erdos_renyi,'Scale Free':panel.scale_free}
    layout = [[sg.Text('Which type of graph would you like to test?')],
              [sg.Listbox(values=list(LIST_OF_GRAPH_TYPES.keys()),size=(20,10), key='-LIST-', enable_events=True)],
              [sg.Submit()],
              [sg.Cancel()]
              ]
    window = sg.Window('SIRD Infection Model', layout)
    while True:

            event, values = window.read()
            logging.debug(event)
            if event in (sg.WIN_CLOSED, 'Exit'):
                quit()
            elif 'Submit' in event:
                break
    window.close()
    try:
        graph_type = values['-LIST-'][0]
    except IndexError:
        userpanel()
    
    graph_params = LIST_OF_GRAPH_TYPES[graph_type]()
    infect_params = panel.infect_panel()
    #(p_i,p_r,init_infected,init_immune,infection_type)
    #(user_graph,enable_vis,graph_type)
    #(graph: nx.Graph,p_i: float, p_r: float,intial_infected: int = 1,intial_immune: int = 0,enable_vis: bool = False,infection_type: infection_strat = ConstantRateInfection,graph_type: str = 'Not Defined')
    parameters = (graph_params[0],infect_params[0],infect_params[1],infect_params[2],infect_params[3],graph_params[1],infect_params[4],graph_params[2])
    return parameters
    
def output_window(results):
    infect_info, orginstats = results
    infect_info = list(infect_info.items())
    orginstats = list(orginstats.items())
    layout_origin = [[x[0],x[1]] for x in orginstats]
    lay_origin = [[sg.Text(f'{x[0]}:{x[1]}')] for x in layout_origin]
    layout_infect = [[x[0],x[1]] for x in infect_info]
    lay_infect = [[sg.Text(f'{x[0]}:{x[1]}')] for x in layout_infect]
    sg.theme('Green')
    layout = [lay_origin, lay_infect]
    window = sg.Window('Output', layout)
    while True:

        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            quit()
        elif 'Submit' in event:
            break
    window.close()
    
    
    
def main():
    if NOGUI is False:
        result = model(*userpanel())
        output_window(result)
    else:
        t = nx.fast_gnp_random_graph(10,0.5)
        infection_data,origin_graph = model(nx.barabasi_albert_graph(1000000,5,initial_graph = t),0.5,0.6)
        print(infection_data)
        print(origin_graph)

if __name__ == '__main__':
    main()
   
    


















