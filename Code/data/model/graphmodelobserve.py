import pandas as pd


def dataloader():
    return pd.read_csv('graphmodel.csv')

def infection_data_parser(Data: pd.DataFrame):
    graphtypes = set(Data['Graph_Type'])
    #print(list(Data.columns()))
    data_sum = Data[list(Data.columns)].groupby(['Graph_Type','n']).describe()
    #print(data_sum['Days_Taken'])
    #data_sum.to_excel('model_sum.xlsx')
    print(data_sum)
    data_sum.to_excel('graph_model_sum.xlsx')
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