import networkx as nx
from betterdiameter import betterdiameter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def main(n):
    #A = nx.barabasi_albert_graph(n,20)
    #B = nx.watts_strogatz_graph(n,20,0.6)
    #f = plt.figure('Barabasi')
    #nx.draw_networkx(A,with_labels=True)
    #f.show()
    #g = plt.figure('Stro')
    #nx.draw(B,with_labels=True)
    #g.show()
    #input()
    #a = dict(enumerate(nx.degree_histogram(A)))
    #b = dict(enumerate(nx.degree_histogram(B)))
    #print(f'Barabasi Diameter: {betterdiameter(A)}')
    #print(f'Strogatz Diameter: {betterdiameter(B)}')
    #print(f'Barabasi Degree Dist: {a}')
    #print(f'Strogatz Degree Dist: {b}')
    #
    #degree = a.keys()
    #frequency = a.values()
    #
    #L = {'Degree':degree,'Frequency':frequency}
    #P = pd.DataFrame(L)
    #P.to_csv('DegreeDist.csv')
    
    
    m=50
    #G = nx.barabasi_albert_graph(1000, m)
    G = nx.watts_strogatz_graph(10000,50,0.7)

    degree_freq = nx.degree_histogram(G)
    degrees = range(len(degree_freq))
    plt.figure(figsize=(12, 8)) 
    plt.loglog(degrees[m:], degree_freq[m:],'go-') 
    plt.xlabel('Degree')
    plt.ylabel('Frequency')
    plt.show()
    input()
    dA = {'degrees':degrees[m:],'frequency': degree_freq[m:]}
    D = pd.DataFrame(dA)
    D.to_csv('wattsstrogatz.csv',index = False)
    #dista = plt.figure('Barabasi Dist')
    #counts,bins = np.histogram(nx.degree_histogram(A))
    #plt.hist(range(len(nx.degree_histogram(A))),bins)
    #dista.show()
    #input()
    #quit()
    #distb = plt.figure('Wattz Strogatz')
    #counts1,bins1 = np.histogram(nx.degree_histogram(B))
    #plt.stairs(bins1,counts1)
    #distb.show()
    #input()

    
    
    
    
if __name__ == '__main__':
    main(50)