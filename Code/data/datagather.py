

import numpy as np; import pandas as pd
import networkx as nx; from betterdiameter import betterdiameter; import math

from tqdm import tqdm






#
#
#
#

def datacreate():
    virus = [0.6,0.5]
    m = 5
    
    e = m
    n = [30,50,70,90,110,130,150,170,190,200,300,400,500,1000,1500,2000,2500,5000,10000]
    d = pd.DataFrame()
    index = 0
    SEED_GRAPH = [nx.fast_gnp_random_graph(10,0.5) for i in range(100)]
    for x in n:
        print(f'{x=}')
        diam_approx = math.log(x)/math.log(math.log(x))
        cluster_approx = (math.log(x)**2)/x
        for i in tqdm(SEED_GRAPH):
            G = nx.barabasi_albert_graph(x,5,initial_graph = i)


            A = {'Number_of_Nodes':x,'Real_Diameter':betterdiameter(G),'Aprrox_Diameter':diam_approx,'Average_Clustering':nx.average_clustering(G),'Approx_Clustering':cluster_approx}
            a = pd.DataFrame(A, index = [index])
            d = pd.concat([d,a],ignore_index=True)

            index += 1

    d.to_csv('data.csv',index = False)

def dataobserve():
    a = pd.read_csv('data.csv')
    #print(a)
    n = [30,50,70,90,110,130,150,170,190,200,300,400,500,1000,1500,2000,2500,5000,10000]
    means = []
    sdofreal = []
    approxdiam = []
    ratios = []
    sdofdiams = []
    meanrcluster = []
    sdofrcluster = []
    approxcluster = []
    ratioofclsuter = []
    sdofcluster = []
    for x in n:
        
        explore = a[a['Number_of_Nodes'] == x]
        realdiams = explore['Real_Diameter']
        means.append(realdiams.mean())
        sdofreal.append(realdiams.std())
        approx = list(explore['Aprrox_Diameter'])[0]
        approxdiam.append(approx)
        ratios.append(approx/realdiams.mean())
        sd = (realdiams.mean()-approx)**2
        sd = math.sqrt(sd)
        sdofdiams.append(sd)
        clusters = explore['Average_Clustering']
        meanrcluster.append(clusters.mean())
        sdofrcluster.append(clusters.std())
        approxC = list(explore['Approx_Clustering'])[0]
        approxcluster.append(approxC)
        ratioofclsuter.append(approxC/clusters.mean())
        sdC = (clusters.mean()-approx)**2
        sdC = math.sqrt(sdC)
        sdofcluster.append(sdC)
        
        
    B = {'N':n,'Average_Diam':means,'Standard_Deviation': sdofreal,'Aprrox_Diam':approxdiam,'Ratio_Between_Diams': ratios, 'Standard_deviation_Between_Real_approx':sdofdiams, 'Average_Clustering': meanrcluster,'S.D of Clsutering': sdofrcluster, 'Approx_Clustering':approxcluster,'Ratio_Between_Clustering':ratioofclsuter,'S.D_Between_Aprrox_and_Real': sdofcluster  }
    data = pd.DataFrame(B)  
    print(data.head())
    data.to_csv('datasum.csv') 
    
    
    
    
    
if __name__ == '__main__':
    k = input('create or observe')
    choice = f'data{k}()'
    eval(choice)