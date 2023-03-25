import pandas as pd


def dataloader():
    return pd.read_csv('graphmodel.csv')

def infection_data_parser(Data: pd.DataFrame):
    graphsizes = sorted(set(Data['n']))
    #print(list(Data.columns()))
    for i in graphsizes:
        data = Data[(Data['n'] == i)]
        data.to_csv(f'graph_model_data\{i}_data.csv')
    #data_sum = Data[list(Data.columns)].groupby(['Graph_Type','n']).describe()
    
    #print(data_sum['Days_Taken'])
    #data_sum.to_excel('model_sum.xlsx')
    #print(data_sum)
    #data_sum.to_csv('model_sum.csv')
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