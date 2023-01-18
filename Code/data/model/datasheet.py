import sirdmodel as sird
import pandas as pd
import networkx as nx
from dict_zip import dict_zip
from numpy import mean, std
#{'n':origin_network.no_nodes,'P_i': p_i,'P_r': p_r,'Days_Taken': days_of_the_infcetion, 'survivors': no_of_survivors,'Everyone_Dead':total_death,'Infection_Type': infection_type.__str__(),'Graph_Type':graph_type}



'''{'n': [30, 30, 30, 30, 30, 30, 30, 30, 30, 30], 'P_i': [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2], 'P_r': [0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65], 'Days_Taken': [13, 14, 12, 14, 14, 13, 14, 13, 14, 13], 'survivors': [19, 20, 22, 20, 21, 23, 20, 17, 20, 20], 'Everyone_Dead': [False, False, False, False, False, False, False, False, False, False], 'Infection_Type': ['ConstantRate', 'ConstantRate', 'ConstantRate', 'ConstantRate', 'ConstantRate', 'ConstantRate', 'ConstantRate', 'ConstantRate', 'ConstantRate', 'ConstantRate'], 'Graph_Type': ['Random', 'Random', 'Random', 'Random', 'Random', 'Random', 'Random', 'Random', 'Random', 'Random'], 'intital_number_of_infected': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 'intital_number_of_immune': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'Successful_infections': [800, 785, 822, 784, 816, 832, 780, 775, 817, 747], 'highest_degree': [20, 20, 20, 20, 20, 20, 20, 20, 20, 20], 'Diameter': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3], 'average_path_length': [1.5218390804597701, 1.5218390804597701, 1.5218390804597701, 1.5218390804597701, 1.5218390804597701, 1.5218390804597701, 1.5218390804597701, 1.5218390804597701, 1.5218390804597701, 1.5218390804597701]}'''


def main():
    A = nx.fast_gnp_random_graph(300,0.5) #edges = 217.5
    B = nx.barabasi_albert_graph(300,8,initial_graph = nx.fast_gnp_random_graph(10,0.5)) #45 + 20*5
    p_i = 0.2
    p_r = 0.65
    all_A = [sird.model(A,p_i,p_r,graph_type='Random') for _ in range(1000)]
    done_A = [a | b for a,b in all_A]
    done_A = zipper(done_A)
    all_B = [sird.model(B,p_i,p_r,graph_type='Barabasi') for _ in range(1000)]
    done_B = [a | b for a,b in all_B]
    done_B = zipper(done_B)
    A_data = pd.DataFrame.from_dict(done_A)
    B_data = pd.DataFrame.from_dict(done_B)
    
    
    print(data(A_data))
    print(data(B_data))




   
def zipper(gen: list) -> dict:
    dic = gen.pop(0)
    for i in gen:
        dic = dict_zip(dic,i)
    return dic
    
def data(data: pd.DataFrame) -> pd.Series:
    n = data['n'][0]
    e = data['e'][0]
    p_i = data['P_i'][0]
    p_r = data['P_r'][0]
    daystaken = data['Days_Taken']
    survivors = data['survivors']
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
    data = {'n':n,'e':e,'p_i':p_i,'p_r':p_r,'averagedays':mean_daystaken,'std_daystaken':std_daystaken ,'average survivors':mean_survivors,'std_survivors':std_survivors,'AveageSuccInf':mean_succ_inf,'std_succ_inf': std_succ_inf,'Inf Type':infectiontype,'init inf':init_inf,'init immune':init_immune}
    return pd.Series(data)



if __name__ == '__main__':
    main()


