import networkx as nx
from sirdmodel import model
from dict_zip import zipper
import pandas as pd
from tqdm import tqdm

def gather():
    result = []
    parametern = [x for x in tqdm(range(6,2000)) if x%5 == 0]
    seed = nx.fast_gnp_random_graph(5,0.5)
    graphs = [nx.barabasi_albert_graph(x,3,initial_graph = seed) for x in tqdm(parametern)]
    for n in tqdm(graphs):
        results = model(n,0.6,0.3)
        we_care,_ = results
        result.append(we_care)
    done = zipper(result)
    care = {'n':done['n'],'e':done['e'],'survivors':done['survivors']}
    Data = pd.DataFrame.from_dict(care)
    print(Data)


if __name__ == '__main__':
    gather()