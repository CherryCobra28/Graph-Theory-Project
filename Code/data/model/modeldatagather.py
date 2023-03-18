import pandas as pd
import sirdmodel as sird
import networkx as nx
from dict_zip import dict_zip
from tqdm import tqdm
import os
import edgesetter




SEED_GRAPHS = [nx.fast_gnp_random_graph(10,0.5) for i in range(100)]
def gather():
    bbara = list()
    rr = list()
    n = [30,50,70,90,110,130,150,170,190,200,300,400,500,1000,1500,2000,2500,5000,10000]
    for N in tqdm(n):
        TEST_GRAPHS = [nx.barabasi_albert_graph(N,5,initial_graph=k) for k in SEED_GRAPHS]
        R_TEST_GRAPHS = create_random_graphs(N,TEST_GRAPHS)
        bara_result = generate(TEST_GRAPHS)
        bbara.append(bara_result)
        R_result = gen_rand(R_TEST_GRAPHS,TEST_GRAPHS)
        rr.append(R_result)
    bara_done = bbara.pop(0)

    for i in bbara:
        bara_done = dict_zip(bara_done, i)
    R_done = rr.pop(0)

    for i in rr:
        R_done = dict_zip(R_done, i)

    #print(A)
    D = pd.DataFrame.from_dict(bara_done)
    L = pd.DataFrame.from_dict(R_done)
    D = pd.concat([D, L],ignore_index =True)
    print(D)
    if os.path.exists('model.csv'):
        D.to_csv('model.csv',index =False,header=False,mode='a')
    else:
        D.to_csv('model.csv',index =False)
def generate(barabasi_graphs):
        

        A,_ = sird.model(barabasi_graphs[0],0.5,0.6,graph_type='barabasi')
        
        barabasi_graphs.pop(0)
        
        for graph in barabasi_graphs:
            B,_ = sird.model(graph,0.5,0.6,graph_type='barabasi')
            #print(A)
            #print(B)
            A = dict_zip(A,B)
       
        return A
def gen_rand(random_graphs,test):
    A = test
    tester = zip(random_graphs,A)
    Alpha,_ = sird.model(random_graphs[0],0.5,0.6,graph_type='random')
    random_graphs.pop(0)
    for graph in random_graphs:
        if graph is None:
            ind = random_graphs.index(graph)
            print(test[ind].number_of_edges())
            print('WHAT')
            quit()
        Beta,_ = sird.model(graph,0.5,0.6,graph_type='random')
        #print(A)
        #print(B)
        Alpha = dict_zip(Alpha,Beta)
    return Alpha

def create_random_graphs(N: int,list_graphs: list):
    random_graphs = [nx.fast_gnp_random_graph(N,0.5) for _ in list_graphs]
    zippy = zip(random_graphs,list_graphs)
    done_random = list()
    for i,v in zippy:
        diff = edgesetter.get_difference(i,v)
        r = edgesetter.edge_rm(i,diff)
        if r is None:
            create_random_graphs(N,list_graphs)
        done_random.append(r)
    return done_random
        


if __name__ == '__main__':
    gather()