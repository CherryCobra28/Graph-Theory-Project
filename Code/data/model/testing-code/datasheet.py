import sirdmodel as sird
import pandas as pd
import networkx as nx
from dict_zip import dict_zip
from numpy import mean, std
import matplotlib.pyplot as plt

#{'n':origin_network.no_nodes,'P_i': p_i,'P_r': p_r,'Days_Taken': days_of_the_infcetion, 'survivors': no_of_survivors,'Everyone_Dead':total_death,'Infection_Type': infection_type.__str__(),'Graph_Type':graph_type}



'''{'n': [30, 30, 30, 30, 30, 30, 30, 30, 30, 30], 'P_i': [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2], 'P_r': [0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65], 'Days_Taken': [13, 14, 12, 14, 14, 13, 14, 13, 14, 13], 'survivors': [19, 20, 22, 20, 21, 23, 20, 17, 20, 20], 'Everyone_Dead': [False, False, False, False, False, False, False, False, False, False], 'Infection_Type': ['ConstantRate', 'ConstantRate', 'ConstantRate', 'ConstantRate', 'ConstantRate', 'ConstantRate', 'ConstantRate', 'ConstantRate', 'ConstantRate', 'ConstantRate'], 'Graph_Type': ['Random', 'Random', 'Random', 'Random', 'Random', 'Random', 'Random', 'Random', 'Random', 'Random'], 'intital_number_of_infected': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 'intital_number_of_immune': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'Successful_infections': [800, 785, 822, 784, 816, 832, 780, 775, 817, 747], 'highest_degree': [20, 20, 20, 20, 20, 20, 20, 20, 20, 20], 'Diameter': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3], 'average_path_length': [1.5218390804597701, 1.5218390804597701, 1.5218390804597701, 1.5218390804597701, 1.5218390804597701, 1.5218390804597701, 1.5218390804597701, 1.5218390804597701, 1.5218390804597701, 1.5218390804597701]}'''




def main():
    x =1
    params = ((30,0.5,5,10,0.5,0.2),(30,0.5,5,10,0.5,0.5),(50,0.5,5,6,0.1,0.8),(10,0.5,4,7,0.5,0.6),(15,0.7,4,5,0.666,0.333))
    for i in params:
        
        _,_,_,_,p_i,p_r = i
        done = datagather(*i)
        A,B,A_data,B_data = done
        if x ==1:
            print(data(A_data))
        with open(f'Code\data\datasheets\\01RandomGraphData{x}.txt','w') as file:
            
            K = str(data(A_data))
            tobewritten = (f'Random Graph {x} \n',K)
            file.writelines(tobewritten)
        Rfigure = plt.figure(f'Rand{x}')
        V = nx.draw(A)
        Rfigure.savefig(f'Code\data\datasheets\\01RandomGraphImage{x}.png')
        
        
        with open(f'Code\data\datasheets\\01BarabasiData{x}.txt','w') as file:
            K = str(data(B_data))
            tobewritten = (f'Barabasi Graph {x}\n',K)
            file.writelines(tobewritten)
        Bfigure = plt.figure(f'Bara{x}')
        V = nx.draw(B)
        Bfigure.savefig(f'Code\data\datasheets\\01BarabasiImage{x}.png')
        
        x+=1

def datagather(n: int, rand_p: float, barabasi_edge: int,seed_n,p_i: float,p_r:float):
    A = nx.fast_gnp_random_graph(n,rand_p) #edges = 217.5
    B = nx.barabasi_albert_graph(n,barabasi_edge,initial_graph = nx.fast_gnp_random_graph(seed_n,rand_p)) #45 + 20*5
    all_A = [sird.model(A,p_i,p_r,graph_type='Random') for _ in range(10)]
    done_A = [a | b for a,b in all_A]
    done_A = zipper(done_A)
    all_B = [sird.model(B,p_i,p_r,graph_type='Barabasi') for _ in range(10)]
    done_B = [a | b for a,b in all_B]
    done_B = zipper(done_B)
    A_data = pd.DataFrame.from_dict(done_A)
    B_data = pd.DataFrame.from_dict(done_B)
    return A,B,A_data,B_data




   
def zipper(gen: list) -> dict:
    dic = gen.pop(0)
    for i in gen:
        dic = dict_zip(dic,i)
    return dic
    
def data(data: pd.DataFrame) -> pd.Series:
    #{'highest_degree':self.highestdegree,'Diameter':self.diameter,'average_path_length':self.average_path_length,'average_clustering': self.clustering,'average_degree':self.average_degree} 
    n = data['n'][0]
    e = data['e'][0]
    p_i = data['P_i'][0]
    p_r = data['P_r'][0]
    highest_degree =data['highest_degree'][0]
    diameter = data['Diameter'][0]
    average_path_length = data['average_path_length'][0]
    average_clustering = data['average_clustering'][0]
    average_degree = data['average_degree'][0]
    daystaken = data['Days_Taken']
    survivors = data['survivors']
    number_of_total_deaths = len([x for x in data['Everyone_Dead'] if x == True])
    infectiontype = data['Infection_Type'][0]
    init_inf = data['intital_number_of_infected'][0]
    init_immune = data['intital_number_of_immune'][0]
    no_of_succ_inf = data['Successful_infections']
    
    
    
    mean_daystaken = mean(daystaken)
    std_daystaken = std(daystaken)
    mean_survivors = mean(survivors)
    std_survivors = std(survivors)
    mean_succ_inf = mean(no_of_succ_inf)
    std_succ_inf = std(no_of_succ_inf)
    data = {'n':n,'e':e,'p_i':p_i,'p_r':p_r,'init inf':init_inf,'init immune':init_immune,'highest degree': highest_degree,'diameter': diameter,'average path len': average_path_length,'average_clustering':average_clustering,'average degree':average_degree,'averagedays':mean_daystaken,'std_daystaken':std_daystaken ,'average survivors':mean_survivors,'std_survivors':std_survivors,'number of total deaths':number_of_total_deaths,'AveageSuccInf':mean_succ_inf,'std_succ_inf': std_succ_inf,'Inf Type':infectiontype}
    return pd.Series(data)



if __name__ == '__main__':
    main()


