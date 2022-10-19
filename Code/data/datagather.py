
import numpy as np; import pandas as pd; import sirdmodel;import networkx as nx; from betterdiameter import betterdiameter; import math








#
#
#
#

def datacreate():
    virus = [0.6,0.5]
    m = 5
    g = nx.complete_graph(m+1)
    e = m
    n = [30,50,70,90,110,130,150,170,190,200,300,400,500,1000,1500,2000,2500,10000]
    d = pd.DataFrame()
    index = 0
    for x in n:
        diam_approx = math.log(x)/math.log(math.log(x))
        
        
        for i in range(101):
            G = nx.barabasi_albert_graph(x,5,initial_graph = g)
            #A = sirdmodel.main(g,n,e,virus[0],virus[1],enable_vis='False')[0]

            A = {'Number_of_Nodes':n,'Real_Diameter':betterdiameter(G),'Aprrox Diameter':diam_approx}
            a = pd.DataFrame(A)
            d = pd.concat([d,a],ignore_index=True)
            #print('Finished 1')
            index += 1
    
    d.to_csv('data.csv',index = False)

def dataobserve():
    a = pd.read_csv('data.csv')
    print(a)
    
    
    
if __name__ == '__main__':
    k = input('create or observe')
    choice = f'data{k}()'
    eval(choice)