import numpy as np; import pandas as pd; import sirdmodel;import networkx as nx








#
#
#
#

def datacreate():
    virus = [0.6,0.5]
    m = 5
    g = nx.complete_graph(m+1)
    e = m
    n = 30
    d = pd.DataFrame()
    index = 0 
    for i in range(101):
        A = sirdmodel.main(g,n,e,virus[0],virus[1],enable_vis='False')[0]
        
        
        a = pd.DataFrame(A,index =[i])
        d = pd.concat([d,a],ignore_index=True)
        index += 1
    
    d.to_csv('data.csv',index = False)

def dataobserve():
    a = pd.read_csv('data.csv')
    print(a)
    
    
    
if __name__ == '__main__':
    k = input('create or observe')
    choice = 'data'+k+'()'
    eval(choice)