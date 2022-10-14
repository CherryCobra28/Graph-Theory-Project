import numpy as np; import pandas as pd; import sirdmodel;import networkx as nx








#
#
#
#

def data():
    virus = [0.6,0.5]
    g = nx.complete_graph(5)
    e = [1,2,3,4,5,1,2,3,4,5,1]
    n = [50,100,150,200,250,300,350,400,450,500]
    d = pd.DataFrame()
    for _ in range(101):
        for x in n:
            A = [sirdmodel.main(g,x,e[0],virus[0],virus[1],enable_vis=False)[0],sirdmodel.main(g,x,e[1],virus[0],virus[1],enable_vis=False)[0],sirdmodel.main(g,x,e[2],virus[0],virus[1],enable_vis=False)[0],sirdmodel.main(g,x,e[3],virus[0],virus[1],enable_vis=False)[0],sirdmodel.main(g,x,e[4],virus[0],virus[1],enable_vis=False)[0],sirdmodel.main(g,x,e[5],virus[0],virus[1],enable_vis=False)[0],sirdmodel.main(g,x,e[6],virus[0],virus[1],enable_vis=False)[0],sirdmodel.main(g,x,e[7],virus[0],virus[1],enable_vis=False)[0],sirdmodel.main(g,x,e[7],virus[0],virus[1],enable_vis=False)[0],sirdmodel.main(g,x,e[8],virus[0],virus[1],enable_vis=False)[0],sirdmodel.main(g,x,e[9],virus[0],virus[1],enable_vis=False)[0],sirdmodel.main(g,x,e[10],virus[0],virus[1],enable_vis=False)[0]]
            for i in A:
                a = pd.DataFrame.from_dict([i])
                d = pd.concat([d,a],ignore_index=True)
    
    return d
            
    #print(d.head())
    #d.to_csv('.\data.csv')
data().to_csv('data.csv',index = False)