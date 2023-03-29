import pandas as pd
from scipy.stats import ttest_ind
n=[1000,1500,2000,2500]
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
    highest_degree = []
    average_shortest = []
    clustering = []
    days_taken_results = []
    survirvors_results = []
    
    for i in A:
        Model_data = d[d['n']==i]
        Model_data_barabasi = Model_data[(Model_data['Graph_Type']=='barabasi')]
        Model_data_random = Model_data[(Model_data['Graph_Type']=='random')]
        
        Graph_Model_data = c[c['n']==i]
        Graph_Model_data_barabasi = Graph_Model_data[(Graph_Model_data['Graph_Type']=='barabasi')]
        Graph_Model_data_random = Graph_Model_data[(Graph_Model_data['Graph_Type']=='random')]
        
        highest_degrees =basic_zero(list(ttest_ind(Graph_Model_data_barabasi['highest_degree'], Graph_Model_data_random['highest_degree'],equal_var= False))[1])
        highest_degree.append(highest_degrees)
        
        l =basic_zero(list(ttest_ind(Graph_Model_data_barabasi['average_path_length'], Graph_Model_data_random['average_path_length'],equal_var= False))[1])
        average_shortest.append(l)
        
        l =basic_zero(list(ttest_ind(Graph_Model_data_barabasi['average_clustering'], Graph_Model_data_random['average_clustering'],equal_var= False))[1])
        clustering.append(l)
        
    
        
        
        
        daystakenstat =basic_zero(list(ttest_ind(Model_data_barabasi['Days_Taken'], Model_data_random['Days_Taken'],equal_var= False))[1])
        days_taken_results.append(daystakenstat)
        survivorstat = basic_zero(list(ttest_ind(Model_data_barabasi['survivors'], Model_data_random['survivors'],equal_var= False))[1])
        survirvors_results.append(survivorstat)
    return pd.DataFrame({'n':A,'Highest Degree': highest_degree,'Average Shortest Path':average_shortest,'Average Clustering': clustering,'Days_Taken':days_taken_results, 'survivors':survirvors_results})






L = results(n,starter,farter)
L.to_latex('tablesbiggestn.tex',index=False)