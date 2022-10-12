import pandas as pd 
import numpy as np

data = pd.read_csv('.\data.csv',delimiter=',')
data.drop(columns=data.columns[0],axis = 1, inplace=True)
print(data.tail())
print(data.dtypes)

death = data[['Everyone die?']]
print(death)