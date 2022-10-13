import numpy as np; import pandas as pd; import sirdmodel















def data():
    d1 = pd.DataFrame()
    d2 = pd.DataFrame()
    d3 = pd.DataFrame()
    
    for i in range(100):
        dic = pd.DataFrame([sirdmodel.main(100,5,0.4,0.5,'False')])
        d1 = pd.concat([d1,dic],ignore_index=True)
    for i in range(100):
        dic = pd.DataFrame([sirdmodel.main(100,10,0.4,0.5,'False')])
        d1 = pd.concat([d1,dic],ignore_index=True)
    for i in range(100):
        dic = pd.DataFrame([sirdmodel.main(100,50,0.4,0.5,'False')])
        d1= pd.concat([d1,dic],ignore_index=True)
    print(d.head())
    d.to_csv('.\data.csv')