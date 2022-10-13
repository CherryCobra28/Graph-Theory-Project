import pandas as pd 
import numpy as np

data = pd.read_csv('.\data.csv',delimiter=',')

print(data.tail())
print(data.dtypes)
print(data.columns)
death = data[data['Everyone_Dead'] == True]
print(len(death))