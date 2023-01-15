import pandas as pd
import sirdmodel as sird
import networkx as nx
from dict_zip import dict_zip
from tqdm import tqdm
import os




SEED_GRAPHS = [nx.fast_gnp_random_graph(10,0.5) for i in range(100)]
def gather():
    
    n = [30,50,70]#,90,110,130,150,170,190,200]#,300,400,500,1000,1500,2000,2500,5000,10000]
    result = []

    for N in tqdm(n):
        K = generate(N)
        result.append(K)
    done = result.pop(0)

    for i in result:
        done = dict_zip(done, i)
        

    #print(A)
    D = pd.DataFrame.from_dict(done)
    print(D)
    if os.path.exists('model.csv'):
        D.to_csv('model.csv',index =False,header=False,mode='a')
    else:
        D.to_csv('model.csv',index =False)
def generate(N):
        TEST_GRAPHS = [nx.barabasi_albert_graph(N,5,initial_graph=k) for k in SEED_GRAPHS]
        A,_ = sird.model(TEST_GRAPHS[0],0.5,0.6,graph_type='barabasi')
        TEST_GRAPHS.pop(0)
        for graph in TEST_GRAPHS:
            B,_ = sird.model(graph,0.5,0.6,graph_type='barabasi')
            #print(A)
            #print(B)
            A = dict_zip(A,B)
        return A
    


if __name__ == '__main__':
    gather()