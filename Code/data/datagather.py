

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
    n = [30,50,70,90,110,130,150,170,190,200,300,400,500,1000]#1500,2000,2500,5000,10000]
    d = pd.DataFrame()
    index = 0
    for x in n:
        print(f'{x=}')
        diam_approx = math.log(x)/math.log(math.log(x))
        cluster_approx = (math.log(x)**2)/x
        g = nx.fast_gnp_random_graph(int(x/2),0.5)
        for i in tqdm(range(2)):
            G = nx.barabasi_albert_graph(x,int(x/2 -1),initial_graph = g)
            #A = sirdmodel.main(g,n,e,virus[0],virus[1],enable_vis='False')[0]
            clusters = np.asarray(list(nx.clustering(G).values()))
            av = np.mean(clusters)
            A = {'Number_of_Nodes':x,'Real_Diameter':betterdiameter(G),'Aprrox_Diameter':diam_approx,'Average_Clustering':av,'Approx_Clustering':cluster_approx}
            a = pd.DataFrame(A, index = [index])
            d = pd.concat([d,a],ignore_index=True)
            #print('Finished 1')
            index += 1
    
    d.to_csv('.\data.csv',index = False)

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
        ratios.append(realdiams.mean()/approx)
        sd = (realdiams.mean()-approx)**2
        sd = math.sqrt(sd)
        sdofdiams.append(sd)
        clusters = explore['Average_Clustering']
        meanrcluster.append(clusters.mean())
        sdofrcluster.append(clusters.std())
        approxC = list(explore['Approx_Clustering'])[0]
        approxcluster.append(approxC)
        ratioofclsuter.append(clusters.mean()/approxC)
        sdC = (clusters.mean()-approx)**2
        sdC = math.sqrt(sdC)
        sdofcluster.append(sdC)
        
        
    B = {'N':n,'Average_Diam':means,'Standard_Deviation': sdofreal,'Aprrox_Diam':approxdiam,'Ratio_Between_Diams': ratios, 'Standard_deviation_Between_Real_approx':sdofdiams, 'Average_Clustering': meanrcluster,'S.D of Clsutering': sdofrcluster, 'Approx_Clustering':approxC,'Ratio_Between_Clustering':ratioofclsuter,'S.D_Between_Aprrox_and_Real': sdofcluster  }
    data = pd.DataFrame(B)  
    print(data) 
    
    
    
    
    
if __name__ == '__main__':
    k = input('create or observe')
    choice = f'data{k}()'
    eval(choice)