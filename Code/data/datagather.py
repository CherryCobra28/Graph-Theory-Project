import numpy as np; import pandas as pd; import sirdmodel
from multiprocessing import Pool







#from multiprocessing import Pool
#def square(n):
#    return n**2
#if __name__=='__main__':
#    numbers=[1,5,9]
#    pool=Pool(processes=3)
#    print(pool.map(square,numbers))   
#
#
#
#
#

def data():
    d = pd.DataFrame()
    for _ in range(101):
        A = [sirdmodel.main(100,5,0.6,0.5,enable_vis=False),sirdmodel.main(100,10,0.6,0.5,enable_vis=False),sirdmodel.main(100,50,0.6,0.5,enable_vis=False),sirdmodel.main(100,5,0.7,0.5,enable_vis=False),sirdmodel.main(100,10,0.7,0.5,enable_vis=False),sirdmodel.main(100,50,0.7,0.5,enable_vis=False),sirdmodel.main(100,5,0.6,0.6,enable_vis=False),sirdmodel.main(100,10,0.6,0.6,enable_vis=False),sirdmodel.main(100,50,0.6,0.6,enable_vis=False),sirdmodel.main(200,5,0.6,0.5,enable_vis=False),sirdmodel.main(200,10,0.6,0.5,enable_vis=False),sirdmodel.main(200,50,0.6,0.5,enable_vis=False),sirdmodel.main(1000,45,0.8,0.2,enable_vis=False),sirdmodel.main(123,15,0.2,0.8,enable_vis=False),sirdmodel.main(2000,100,0.9,0.01,enable_vis=False)]
        for i in A:
            a = pd.DataFrame.from_dict([i])
            d = pd.concat([d,a],ignore_index=True)
    
    return d
            
    #print(d.head())
    #d.to_csv('.\data.csv')
data().to_csv('data.csv',index = False)