
import numpy as np; import pandas as pd; import sirdmodel;import networkx as nx; from betterdiameter import betterdiameter; import math

from tqdm import tqdm






#
#
#
#

def datacreate():
    virus = [0.6,0.5]
    m = 5
    g = nx.complete_graph(m+1)
    e = m
    n = [30,50,70,90,110,130,150]#170,190,200,300,400,500,1000,1500,2000,2500,10000]
    d = pd.DataFrame()
    index = 0
    for x in n:
        print(f'{x=}')
        diam_approx = math.log(x)/math.log(math.log(x))
        cluster_approx = (math.log(x)**2)/x
        
        for i in tqdm(range(101)):
            G = nx.barabasi_albert_graph(x,5,initial_graph = g)
            #A = sirdmodel.main(g,n,e,virus[0],virus[1],enable_vis='False')[0]

            A = {'Number_of_Nodes':x,'Real_Diameter':betterdiameter(G),'Aprrox_Diameter':diam_approx,'Average_Clustering':nx.average_clustering(G),'Approx_Clustering':cluster_approx}
            a = pd.DataFrame(A, index = [index])
            d = pd.concat([d,a],ignore_index=True)
            #print('Finished 1')
            index += 1
    
    d.to_csv('.\data.csv',index = False)

def dataobserve():
    a = pd.read_csv('.\data\data.csv')
    print(a)
    
    
    
if __name__ == '__main__':
    k = input('create or observe')
    choice = f'data{k}()'
    eval(choice)