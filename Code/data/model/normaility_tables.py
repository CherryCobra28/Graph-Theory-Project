import pandas as pd
from scipy.stats import shapiro
n= [30,50,70,90,110,130,150,170,190,200,300,400,500,1000,1500,2000,2500]
starter = pd.DataFrame()
for i in n: 
    Model_data = pd.read_csv(f'model_data\\{i}_data.csv')
    starter = pd.concat([starter,Model_data],ignore_index=False)
print(starter)

farter = pd.DataFrame()
for i in n: 
    Model_data = pd.read_csv(f'graph_model_data\\{i}_data.csv')
    farter = pd.concat([farter,Model_data],ignore_index=False)
print(farter)







def basic_zero(x: float):
    if x < 0.00001:
        return 0.0
    else:
        return x


def results(A: list, d: pd.DataFrame, c:pd.DataFrame):
    r_highest_degree = []
    r_average_shortest = []
    r_clustering = []
    r_days_taken_results = []
    r_survirvors_results = []
    b_highest_degree = []
    b_average_shortest = []
    b_clustering = []
    b_days_taken_results = []
    b_survirvors_results = []
    
    for i in A:
        Model_data = d[d['n']==i]
        Model_data_barabasi = Model_data[(Model_data['Graph_Type']=='barabasi')]
        Model_data_random = Model_data[(Model_data['Graph_Type']=='random')]
        
        Graph_Model_data = c[c['n']==i]
        Graph_Model_data_barabasi = Graph_Model_data[(Graph_Model_data['Graph_Type']=='barabasi')]
        Graph_Model_data_random = Graph_Model_data[(Graph_Model_data['Graph_Type']=='random')]
        
        highest_degrees =basic_zero(list(shapiro(Graph_Model_data_barabasi['highest_degree']))[1])
        b_highest_degree.append(highest_degrees)
        
        l =basic_zero(list(shapiro(Graph_Model_data_barabasi['average_path_length']))[1])
        b_average_shortest.append(l)
        
        l =basic_zero(list(shapiro(Graph_Model_data_barabasi['average_clustering']))[1])
        b_clustering.append(l)
        
        highest_degrees =basic_zero(list(shapiro(Graph_Model_data_random['highest_degree']))[1])
        r_highest_degree.append(highest_degrees)
        
        l =basic_zero(list(shapiro(Graph_Model_data_random['average_path_length']))[1])
        r_average_shortest.append(l)
        
        l =basic_zero(list(shapiro(Graph_Model_data_random['average_clustering']))[1])
        r_clustering.append(l)
        
    
        
    
        daystakenstat =basic_zero(list(shapiro(Model_data_barabasi['Days_Taken']))[1])
        b_days_taken_results.append(daystakenstat)
        survivorstat = basic_zero(list(shapiro(Model_data_barabasi['survivors']))[1])
        b_survirvors_results.append(survivorstat)
        daystakenstat =basic_zero(list(shapiro(Model_data_random['Days_Taken']))[1])
        r_days_taken_results.append(daystakenstat)
        survivorstat = basic_zero(list(shapiro(Model_data_random['survivors']))[1])
        r_survirvors_results.append(survivorstat)
        
        
        
        
        
    return pd.DataFrame({'n':A,'Highest Degree': r_highest_degree,'Average Shortest Path':r_average_shortest,'Average Clustering': r_clustering,'Days_Taken':r_days_taken_results, 'survivors':r_survirvors_results}), pd.DataFrame({'n':A,'Highest Degree': b_highest_degree,'Average Shortest Path':b_average_shortest,'Average Clustering': b_clustering,'Days_Taken':b_days_taken_results, 'survivors':b_survirvors_results}) 






L,M = results(n,starter,farter)
L.to_latex('random_normality_tables.tex',index=False)
M.to_latex('barabasi_normality_tables.tex',index=False)