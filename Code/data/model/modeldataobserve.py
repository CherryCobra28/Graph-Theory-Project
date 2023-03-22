import pandas as pd



def dataloader():
    return pd.read_csv('model.csv')

def infection_data_parser(Data: pd.DataFrame):
    graphtypes = set(Data['Graph_Type'])
    data_sum = Data[['Graph_Type','n','e','Days_Taken','survivors','Everyone_Dead','Successful_infections']].groupby(['Graph_Type','n']).describe()
    print(data_sum['survivors'])
    data_sum.to_excel('model_sum.xlsx')
    #for graph in graphtypes:
    #    graph_data = Data[Data['Graph_Type'] == graph]
    #    #graph_sizes = sorted(set(data['n']))
    #    dataframes = []
    #    #for x in graph_sizes:
    #        #current_size = graph_data[graph_data['n']==x]
    #    sum_data = graph_data[['n','e','Days_Taken','survivors','Everyone_Dead','Successful_infections']].groupby('n').describe()
    #    print(sum_data)
    #print(data_sum)



if __name__ == '__main__':
    data = dataloader()
    infection_data_parser(data)